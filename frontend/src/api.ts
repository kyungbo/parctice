// 로컬: Vite proxy(/api → localhost:8000)
// 프로덕션: VITE_API_URL 환경변수 (예: https://hi-touch-trend-api.onrender.com/api)
const API_BASE = import.meta.env.VITE_API_URL ?? '/api'

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export const api = {
  getWeeklyTrends: () => fetchApi<import('./types').WeeklySummary>('/trends/weekly'),
  getHotTreatments: () => fetchApi<{ report_date: string; items: import('./types').HotTreatment[] }>('/trends/hot'),
  getTop10: () => fetchApi<{ report_date: string; items: import('./types').KeywordRank[] }>('/keywords/top10'),
  getRising: () => fetchApi<{ report_date: string; items: import('./types').RisingKeyword[] }>('/keywords/rising'),
  getFalling: () => fetchApi<{ report_date: string; items: import('./types').RisingKeyword[] }>('/keywords/falling'),
  getKeywordDetail: (keyword: string) => fetchApi<import('./types').KeywordDetail>(`/keywords/${encodeURIComponent(keyword)}`),
  getReports: () => fetchApi<{ items: import('./types').ReportMeta[] }>('/reports/'),
}
