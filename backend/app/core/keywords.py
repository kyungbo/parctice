"""
미용의료 카테고리별 키워드 그룹 정의.
네이버 데이터랩 API의 keywordGroups 파라미터로 그대로 사용됨.
"""

KEYWORD_GROUPS: dict[str, list[str]] = {
    "리프팅": ["울쎄라", "써마지", "인모드", "리프팅", "슈링크", "쥬베룩"],
    "필러/톡신": ["보톡스", "필러", "보타락스", "보툴리눔", "보툴린", "제오민"],
    "스킨부스터": ["스킨부스터", "물광주사", "리쥬란", "엑소좀", "비비크림주사"],
    "레이저": ["레이저토닝", "피코레이저", "IPL", "브이빔", "프락셀", "클라리티"],
    "체형관리": ["지방흡입", "냉동지방분해", "인모드바디", "하이퍼포먼스", "고강도집속초음파"],
    "시수술": ["쁘띠성형", "눈밑지방재배치", "팔자주름", "애플힙주사"],
}

# 전체 플랫 키워드 목록 (중복 없이)
ALL_KEYWORDS: list[str] = list({kw for kws in KEYWORD_GROUPS.values() for kw in kws})

# 키워드 → 카테고리 역매핑
KEYWORD_TO_CATEGORY: dict[str, str] = {
    kw: cat for cat, kws in KEYWORD_GROUPS.items() for kw in kws
}
