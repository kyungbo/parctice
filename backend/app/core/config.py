from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "미용의료 마켓 트렌드"
    # 쉼표 구분 origin 목록 (예: CORS_ORIGINS=https://foo.vercel.app,http://localhost:5173)
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    # 네이버 데이터랩 API (실서비스 시 환경변수로 설정)
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    # 주별 JSON 스냅샷 저장 경로
    DATA_DIR: str = "data"

    class Config:
        env_file = ".env"


settings = Settings()
