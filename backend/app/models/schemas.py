from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum


class Category(str, Enum):
    LIFTING = "리프팅"
    FILLER = "필러/톡신"
    SKIN_BOOSTER = "스킨부스터"
    BODY = "체형관리"
    LASER = "레이저"
    SURGERY = "시수술"
    ETC = "기타"


class KeywordRank(BaseModel):
    rank: int
    keyword: str
    search_volume: int
    change_rate: float  # 전주 대비 변화율 (%)
    category: Optional[str] = None


class HotTreatment(BaseModel):
    keyword: str
    search_volume: int
    change_rate: float
    category: str
    rank: int


class RisingKeyword(BaseModel):
    keyword: str
    change_rate: float
    prev_volume: int
    current_volume: int
    category: Optional[str] = None


class CategoryTrend(BaseModel):
    category: str
    keywords: List[KeywordRank]
    total_volume: int


class WeeklySummary(BaseModel):
    report_date: date
    hot_treatments: List[HotTreatment]
    top10: List[KeywordRank]
    rising: List[RisingKeyword]
    falling: List[RisingKeyword]
    by_category: List[CategoryTrend]


class KeywordDetail(BaseModel):
    keyword: str
    category: str
    search_volume: int
    change_rate: float
    related_terms: List[dict]  # [{ "term": "효과", "weight": 85 }, ...]


class ReportMeta(BaseModel):
    id: str
    report_date: date
    title: str
    summary: Optional[str] = None
