from datetime import date, timedelta

from fastapi import APIRouter

from app.models.schemas import WeeklySummary
from app.services import data_store, mock_data
from app.services.naver_datalab import fetch_weekly_summary

router = APIRouter()


def _this_monday() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


async def _get_summary() -> WeeklySummary:
    """
    데이터 조회 우선순위:
    1. 이번 주 JSON 캐시 파일
    2. 네이버 데이터랩 API (API 키 있을 때)
    3. mock_data 폴백
    """
    monday = _this_monday()
    cached = data_store.load(monday)
    if cached:
        return cached

    live = await fetch_weekly_summary(monday)
    if live:
        data_store.save(live)
        return live

    return mock_data.get_weekly_summary()


@router.get("/weekly", response_model=WeeklySummary)
async def get_weekly_trends():
    """이번 주 검색 트렌드 요약 (HOT 시술, TOP10, 급상승/급하락, 카테고리별)."""
    return await _get_summary()


@router.get("/hot")
async def get_hot_treatments():
    """이번 주 HOT 시술 상위 3개."""
    summary = await _get_summary()
    return {"report_date": summary.report_date, "items": summary.hot_treatments}
