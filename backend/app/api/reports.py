from fastapi import APIRouter

from app.services import data_store, mock_data

router = APIRouter()


@router.get("/")
def list_reports():
    """과거 위클리 리포트 목록 (보관함). JSON 파일 기반, 없으면 mock."""
    reports = data_store.list_reports()
    if not reports:
        reports = mock_data.get_report_list()
    return {"items": reports}
