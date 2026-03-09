#!/usr/bin/env python
"""
주간 트렌드 데이터 수집 배치 스크립트.
매주 월요일 GitHub Actions 또는 cron으로 실행.

사용법:
  cd backend
  python scripts/collect_weekly.py

환경변수 (backend/.env):
  NAVER_CLIENT_ID=xxx
  NAVER_CLIENT_SECRET=xxx
"""
import asyncio
import logging
import sys
from pathlib import Path

# 프로젝트 루트(backend/)를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    from app.services import data_store
    from app.services.naver_datalab import _this_monday, fetch_weekly_summary

    monday = _this_monday()
    logger.info("수집 시작: %s", monday)

    # 이미 캐시 있으면 스킵
    if data_store.load(monday):
        logger.info("이미 저장된 데이터 존재. 스킵.")
        return

    summary = await fetch_weekly_summary(monday)
    if summary:
        data_store.save(summary)
        logger.info("저장 완료 — HOT: %s", [h.keyword for h in summary.hot_treatments])
    else:
        logger.warning("API 수집 실패. 네이버 API 키를 확인하세요.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
