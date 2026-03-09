"""
주별 트렌드 데이터를 JSON 파일로 저장/조회하는 간단한 저장소.
경로: {DATA_DIR}/weekly/YYYY-Www.json  (예: 2025-W10.json)
"""
from __future__ import annotations

import json
import logging
from datetime import date, timedelta
from pathlib import Path

from app.core.config import settings
from app.models.schemas import ReportMeta, WeeklySummary

logger = logging.getLogger(__name__)


def _data_dir() -> Path:
    d = Path(settings.DATA_DIR) / "weekly"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _filename(monday: date) -> Path:
    iso = monday.isocalendar()
    key = f"{iso.year}-W{iso.week:02d}"
    return _data_dir() / f"{key}.json"


def save(summary: WeeklySummary) -> None:
    path = _filename(summary.report_date)
    path.write_text(summary.model_dump_json(indent=2), encoding="utf-8")
    logger.info("저장 완료: %s", path)


def load(monday: date) -> WeeklySummary | None:
    path = _filename(monday)
    if not path.exists():
        return None
    try:
        return WeeklySummary.model_validate_json(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("파일 로드 실패 %s: %s", path, exc)
        return None


def load_latest() -> WeeklySummary | None:
    """가장 최근 저장된 주간 데이터 반환."""
    files = sorted(_data_dir().glob("*.json"), reverse=True)
    for f in files:
        try:
            return WeeklySummary.model_validate_json(f.read_text(encoding="utf-8"))
        except Exception:
            continue
    return None


def list_reports(limit: int = 12) -> list[ReportMeta]:
    """보관된 리포트 목록 (최신순)."""
    files = sorted(_data_dir().glob("*.json"), reverse=True)[:limit]
    result: list[ReportMeta] = []
    for f in files:
        try:
            summary = WeeklySummary.model_validate_json(f.read_text(encoding="utf-8"))
            hot_kws = ", ".join(h.keyword for h in summary.hot_treatments[:3])
            result.append(
                ReportMeta(
                    id=f.stem,
                    report_date=summary.report_date,
                    title=f"{summary.report_date} 위클리 리포트",
                    summary=f"HOT: {hot_kws}",
                )
            )
        except Exception:
            continue
    return result
