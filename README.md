# 미용의료 마켓 트렌드 (Treatment Market Trend)

PRD 기반 Phase 1 MVP: 네이버 검색 트렌드 기반 **TOP 10 · 급상승 키워드** 웹 대시보드.

## 기능

- **대시보드**: 이번 주 HOT 시술 3가지, 전주 대비 상승률 차트, TOP 10 랭킹, 급상승/급하락 키워드, 카테고리별 트렌드
- **키워드 상세**: 키워드 클릭 시 연관 검색어(효과, 부작용, 가격 등) 노출
- **리포트 보관함**: 과거 위클리 리포트 목록 (Phase 2에서 PDF 다운로드 연동 예정)

## 기술 스택

- **Backend**: FastAPI (Python)
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts
- **Data**: 목업 데이터 (실서비스 시 네이버 데이터랩 API 연동)

## 실행 방법

### 1. 백엔드

```bash
cd treatment-market-trend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 프론트엔드

```bash
cd treatment-market-trend/frontend
npm install
npm run dev
```

브라우저에서 **http://localhost:5173** 접속. API는 프록시로 `http://localhost:8000`에 연결됩니다.

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/trends/weekly` | 이번 주 트렌드 요약 (HOT, TOP10, 급상승/급하락, 카테고리별) |
| GET | `/api/trends/hot` | HOT 시술 상위 3개 |
| GET | `/api/keywords/top10` | 검색어 TOP 10 |
| GET | `/api/keywords/rising` | 급상승 키워드 |
| GET | `/api/keywords/falling` | 급하락 키워드 |
| GET | `/api/keywords/{keyword}` | 키워드 상세(연관어) |
| GET | `/api/reports/` | 리포트 보관함 목록 |

## 실서비스 연동 시

- `backend/app/services/` 에 네이버 데이터랩 API 호출 모듈 추가 후, `mock_data` 대신 해당 서비스를 사용하도록 라우터에서 교체
- 환경변수: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` (`.env` 또는 배포 환경에 설정)
- 의료 광고법 준수: 특정 병원명·금지 키워드 필터링 로직 추가 권장
- 리포트에 **검색량은 관심도 지표이며 실제 시술 횟수와 다를 수 있음** 디스클레이머 유지 (현재 푸터에 반영)

## 로드맵

- **Phase 1 (현재)**: 목업 기반 웹 대시보드 ✅
- **Phase 2**: 카카오톡 알림톡, PDF 리포트 자동 생성
- **Phase 3**: AI 인사이트, 지역별 트렌드
