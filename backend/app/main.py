"""
미용의료 마켓 트렌드 - FastAPI 메인 앱
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import trends, keywords, reports
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="미용의료 검색 트렌드 위클리 리포트 API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(keywords.router, prefix="/api/keywords", tags=["keywords"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


@app.get("/")
def root():
    return {"service": "Treatment Market Trend", "version": "0.1.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
