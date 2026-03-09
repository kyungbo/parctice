"""
MVP용 목업 데이터. 실제 서비스에서는 네이버 데이터랩 API 등으로 교체.
"""
from datetime import date, timedelta
from app.models.schemas import (
    HotTreatment,
    KeywordRank,
    RisingKeyword,
    CategoryTrend,
    WeeklySummary,
    KeywordDetail,
    ReportMeta,
)


def _this_week() -> date:
    # 이번 주 월요일
    today = date.today()
    return today - timedelta(days=today.weekday())


def get_weekly_summary() -> WeeklySummary:
    report_date = _this_week()
    hot_treatments = [
        HotTreatment(keyword="쥬베룩", search_volume=125000, change_rate=32.5, category="리프팅", rank=1),
        HotTreatment(keyword="인모드", search_volume=98000, change_rate=28.1, category="체형관리", rank=2),
        HotTreatment(keyword="보톡스", search_volume=87600, change_rate=18.4, category="필러/톡신", rank=3),
    ]
    top10 = [
        KeywordRank(rank=1, keyword="쥬베룩", search_volume=125000, change_rate=32.5, category="리프팅"),
        KeywordRank(rank=2, keyword="인모드", search_volume=98000, change_rate=28.1, category="체형관리"),
        KeywordRank(rank=3, keyword="보톡스", search_volume=87600, change_rate=18.4, category="필러/톡신"),
        KeywordRank(rank=4, keyword="스킨부스터", search_volume=82100, change_rate=12.3, category="스킨부스터"),
        KeywordRank(rank=5, keyword="레이저토닝", search_volume=78500, change_rate=-2.1, category="레이저"),
        KeywordRank(rank=6, keyword="필러", search_volume=72100, change_rate=8.7, category="필러/톡신"),
        KeywordRank(rank=7, keyword="리프팅", search_volume=68900, change_rate=15.2, category="리프팅"),
        KeywordRank(rank=8, keyword="쁘띠성형", search_volume=65400, change_rate=5.4, category="시수술"),
        KeywordRank(rank=9, keyword="울쎄라", search_volume=61200, change_rate=22.0, category="리프팅"),
        KeywordRank(rank=10, keyword="보타락스", search_volume=58900, change_rate=11.1, category="필러/톡신"),
    ]
    rising = [
        RisingKeyword(keyword="쥬베룩", change_rate=32.5, prev_volume=94500, current_volume=125000, category="리프팅"),
        RisingKeyword(keyword="울쎄라", change_rate=22.0, prev_volume=50200, current_volume=61200, category="리프팅"),
        RisingKeyword(keyword="인모드", change_rate=28.1, prev_volume=76400, current_volume=98000, category="체형관리"),
        RisingKeyword(keyword="슈링크", change_rate=45.2, prev_volume=21000, current_volume=30500, category="리프팅"),
        RisingKeyword(keyword="하이퍼포먼스", change_rate=38.0, prev_volume=18000, current_volume=24800, category="체형관리"),
    ]
    falling = [
        RisingKeyword(keyword="레이저토닝", change_rate=-2.1, prev_volume=80200, current_volume=78500, category="레이저"),
        RisingKeyword(keyword="피코레이저", change_rate=-8.5, prev_volume=42000, current_volume=38400, category="레이저"),
        RisingKeyword(keyword="보툴린", change_rate=-5.2, prev_volume=35000, current_volume=33200, category="필러/톡신"),
    ]
    by_category = [
        CategoryTrend(
            category="리프팅",
            keywords=[
                KeywordRank(rank=1, keyword="쥬베룩", search_volume=125000, change_rate=32.5, category="리프팅"),
                KeywordRank(rank=2, keyword="울쎄라", search_volume=61200, change_rate=22.0, category="리프팅"),
                KeywordRank(rank=3, keyword="리프팅", search_volume=68900, change_rate=15.2, category="리프팅"),
            ],
            total_volume=255100,
        ),
        CategoryTrend(
            category="필러/톡신",
            keywords=[
                KeywordRank(rank=1, keyword="보톡스", search_volume=87600, change_rate=18.4, category="필러/톡신"),
                KeywordRank(rank=2, keyword="필러", search_volume=72100, change_rate=8.7, category="필러/톡신"),
                KeywordRank(rank=3, keyword="보타락스", search_volume=58900, change_rate=11.1, category="필러/톡신"),
            ],
            total_volume=218600,
        ),
        CategoryTrend(
            category="체형관리",
            keywords=[
                KeywordRank(rank=1, keyword="인모드", search_volume=98000, change_rate=28.1, category="체형관리"),
                KeywordRank(rank=2, keyword="하이퍼포먼스", search_volume=24800, change_rate=38.0, category="체형관리"),
            ],
            total_volume=122800,
        ),
        CategoryTrend(
            category="스킨부스터",
            keywords=[
                KeywordRank(rank=1, keyword="스킨부스터", search_volume=82100, change_rate=12.3, category="스킨부스터"),
            ],
            total_volume=82100,
        ),
        CategoryTrend(
            category="레이저",
            keywords=[
                KeywordRank(rank=1, keyword="레이저토닝", search_volume=78500, change_rate=-2.1, category="레이저"),
            ],
            total_volume=78500,
        ),
        CategoryTrend(
            category="시수술",
            keywords=[
                KeywordRank(rank=1, keyword="쁘띠성형", search_volume=65400, change_rate=5.4, category="시수술"),
            ],
            total_volume=65400,
        ),
    ]
    return WeeklySummary(
        report_date=report_date,
        hot_treatments=hot_treatments,
        top10=top10,
        rising=rising,
        falling=falling,
        by_category=by_category,
    )


def get_keyword_detail(keyword: str) -> KeywordDetail:
    # 샘플 연관어 (실제로는 검색 연관어 API 또는 LLM 분류 활용)
    related_map = {
        "쥬베룩": [
            {"term": "효과", "weight": 92},
            {"term": "부작용", "weight": 88},
            {"term": "가격", "weight": 85},
            {"term": "후기", "weight": 78},
            {"term": "연령", "weight": 65},
            {"term": "유지기간", "weight": 72},
        ],
        "인모드": [
            {"term": "다이어트", "weight": 90},
            {"term": "복부", "weight": 87},
            {"term": "가격", "weight": 82},
            {"term": "후기", "weight": 75},
            {"term": "부작용", "weight": 68},
        ],
        "보톡스": [
            {"term": "가격", "weight": 91},
            {"term": "부위", "weight": 85},
            {"term": "효과", "weight": 80},
            {"term": "유지기간", "weight": 76},
        ],
    }
    related = related_map.get(keyword)
    if not related:
        related = [{"term": "효과", "weight": 70}, {"term": "가격", "weight": 65}, {"term": "후기", "weight": 60}]
    summary = get_weekly_summary()
    for x in summary.top10:
        if x.keyword == keyword:
            return KeywordDetail(keyword=keyword, category=x.category or "기타", search_volume=x.search_volume, change_rate=x.change_rate, related_terms=related)
    for r in summary.rising:
        if r.keyword == keyword:
            return KeywordDetail(keyword=keyword, category=r.category or "기타", search_volume=r.current_volume, change_rate=r.change_rate, related_terms=related)
    for f in summary.falling:
        if f.keyword == keyword:
            return KeywordDetail(keyword=keyword, category=f.category or "기타", search_volume=f.current_volume, change_rate=f.change_rate, related_terms=related)
    return KeywordDetail(
        keyword=keyword,
        category="기타",
        search_volume=30000,
        change_rate=0.0,
        related_terms=related,
    )


def get_report_list() -> list[ReportMeta]:
    base = _this_week()
    return [
        ReportMeta(id=f"r-{i}", report_date=base - timedelta(weeks=i), title=f"{base - timedelta(weeks=i)} 위클리 리포트", summary=None)
        for i in range(5)
    ]
