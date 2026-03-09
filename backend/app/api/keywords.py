from datetime import date, timedelta

from fastapi import APIRouter, HTTPException

from app.models.schemas import KeywordDetail
from app.services import data_store, mock_data
from app.services.naver_datalab import fetch_weekly_summary

router = APIRouter()


def _this_monday() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


async def _get_summary():
    monday = _this_monday()
    cached = data_store.load(monday)
    if cached:
        return cached
    live = await fetch_weekly_summary(monday)
    if live:
        data_store.save(live)
        return live
    return mock_data.get_weekly_summary()


@router.get("/top10")
async def get_top10():
    """미용의료 검색어 TOP 10."""
    summary = await _get_summary()
    return {"report_date": summary.report_date, "items": summary.top10}


@router.get("/rising")
async def get_rising():
    """전주 대비 급상승 키워드."""
    summary = await _get_summary()
    return {"report_date": summary.report_date, "items": summary.rising}


@router.get("/falling")
async def get_falling():
    """전주 대비 급하락 키워드."""
    summary = await _get_summary()
    return {"report_date": summary.report_date, "items": summary.falling}


@router.get("/{keyword}", response_model=KeywordDetail)
async def get_keyword(keyword: str):
    """키워드 상세 (연관어 클라우드용)."""
    # 연관어는 mock_data의 매핑을 우선 사용; 없으면 기본 연관어 반환
    detail = mock_data.get_keyword_detail(keyword)
    if not detail:
        raise HTTPException(status_code=404, detail="Keyword not found")

    # 검색량/변화율은 실데이터(캐시)로 덮어씀
    summary = await _get_summary()
    for kw in summary.top10 + summary.rising + summary.falling:
        kw_word = kw.keyword if hasattr(kw, "keyword") else None
        if kw_word == keyword:
            vol = getattr(kw, "search_volume", None) or getattr(kw, "current_volume", None)
            cr = getattr(kw, "change_rate", detail.change_rate)
            if vol:
                detail = KeywordDetail(
                    keyword=detail.keyword,
                    category=detail.category,
                    search_volume=vol,
                    change_rate=cr,
                    related_terms=detail.related_terms,
                )
            break

    return detail
