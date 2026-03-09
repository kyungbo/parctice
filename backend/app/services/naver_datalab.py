"""
네이버 데이터랩 검색어 트렌드 API 클라이언트.
API 키가 없을 경우 mock_data로 자동 폴백.
"""
from __future__ import annotations

import logging
from datetime import date, timedelta

import httpx

from app.core.config import settings
from app.core.keywords import KEYWORD_GROUPS, KEYWORD_TO_CATEGORY
from app.models.schemas import (
    CategoryTrend,
    HotTreatment,
    KeywordRank,
    RisingKeyword,
    WeeklySummary,
)

logger = logging.getLogger(__name__)

DATALAB_URL = "https://openapi.naver.com/v1/datalab/search"


def _week_range(monday: date) -> tuple[str, str]:
    """월요일 기준 1주일 범위 반환 (YYYY-MM-DD 포맷)."""
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def _this_monday() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


async def _call_datalab(start: str, end: str) -> dict:
    """데이터랩 API 호출. ratio 기반 결과 반환."""
    keyword_groups = [
        {"groupName": cat, "keywords": kws} for cat, kws in KEYWORD_GROUPS.items()
    ]
    payload = {
        "startDate": start,
        "endDate": end,
        "timeUnit": "week",
        "keywordGroups": keyword_groups,
    }
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(DATALAB_URL, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()


def _parse_ratio(api_result: dict, week_start: str) -> dict[str, float]:
    """API 응답에서 카테고리별 ratio 추출 (해당 주 데이터)."""
    ratios: dict[str, float] = {}
    for item in api_result.get("results", []):
        cat = item["title"]
        for d in item.get("data", []):
            if d["period"] == week_start:
                ratios[cat] = d["ratio"]
                break
    return ratios


def _build_summary(
    this_ratios: dict[str, float],
    prev_ratios: dict[str, float],
    report_date: date,
) -> WeeklySummary:
    """ratio 데이터로 WeeklySummary 구성."""
    # 카테고리 → 대표 ratio를 search_volume 단위로 스케일링 (×1000 근사치)
    SCALE = 1000

    keyword_ranks: list[KeywordRank] = []
    category_trends: list[CategoryTrend] = []

    for cat, kws in KEYWORD_GROUPS.items():
        ratio = this_ratios.get(cat, 0.0)
        prev = prev_ratios.get(cat, ratio)
        change = round((ratio - prev) / prev * 100, 1) if prev else 0.0
        vol = int(ratio * SCALE)

        # 카테고리 내 키워드는 동일 비중으로 분배 (MVP 근사)
        per_kw_vol = vol // len(kws) if kws else 0
        cat_kws: list[KeywordRank] = []
        for i, kw in enumerate(kws):
            cat_kws.append(
                KeywordRank(
                    rank=i + 1,
                    keyword=kw,
                    search_volume=per_kw_vol,
                    change_rate=change,
                    category=cat,
                )
            )
        keyword_ranks.extend(cat_kws)
        category_trends.append(
            CategoryTrend(category=cat, keywords=cat_kws, total_volume=vol)
        )

    # 전체 검색량 기준 TOP 10
    keyword_ranks.sort(key=lambda x: x.search_volume, reverse=True)
    top10 = [KeywordRank(rank=i + 1, **{**r.model_dump(), "rank": i + 1}) for i, r in enumerate(keyword_ranks[:10])]

    # HOT 시술 (change_rate 상위 3)
    by_change = sorted(top10, key=lambda x: x.change_rate, reverse=True)
    hot = [
        HotTreatment(
            keyword=r.keyword,
            search_volume=r.search_volume,
            change_rate=r.change_rate,
            category=r.category or "기타",
            rank=i + 1,
        )
        for i, r in enumerate(by_change[:3])
    ]

    # 급상승 / 급하락
    rising = [
        RisingKeyword(
            keyword=r.keyword,
            change_rate=r.change_rate,
            prev_volume=int(r.search_volume / (1 + r.change_rate / 100)) if r.change_rate != -100 else 0,
            current_volume=r.search_volume,
            category=r.category,
        )
        for r in sorted(top10, key=lambda x: x.change_rate, reverse=True)
        if r.change_rate > 0
    ][:5]
    falling = [
        RisingKeyword(
            keyword=r.keyword,
            change_rate=r.change_rate,
            prev_volume=int(r.search_volume / (1 + r.change_rate / 100)),
            current_volume=r.search_volume,
            category=r.category,
        )
        for r in sorted(top10, key=lambda x: x.change_rate)
        if r.change_rate < 0
    ][:3]

    return WeeklySummary(
        report_date=report_date,
        hot_treatments=hot,
        top10=top10,
        rising=rising,
        falling=falling,
        by_category=category_trends,
    )


async def fetch_weekly_summary(monday: date | None = None) -> WeeklySummary | None:
    """
    네이버 데이터랩으로부터 주간 트렌드 수집.
    API 키 미설정 또는 오류 시 None 반환 → 호출측에서 mock 폴백.
    """
    if not settings.NAVER_CLIENT_ID or not settings.NAVER_CLIENT_SECRET:
        logger.info("Naver API 키 미설정 — mock 데이터 사용")
        return None

    monday = monday or _this_monday()
    prev_monday = monday - timedelta(weeks=1)

    this_start, this_end = _week_range(monday)
    prev_start, prev_end = _week_range(prev_monday)

    try:
        this_result = await _call_datalab(this_start, this_end)
        prev_result = await _call_datalab(prev_start, prev_end)
    except Exception as exc:
        logger.warning("데이터랩 API 호출 실패: %s", exc)
        return None

    this_ratios = _parse_ratio(this_result, this_start)
    prev_ratios = _parse_ratio(prev_result, prev_start)

    return _build_summary(this_ratios, prev_ratios, monday)
