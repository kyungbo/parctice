import { useEffect, useState } from 'react'
import { api } from '../api'
import type { ReportMeta } from '../types'

const formatDate = (s: string) => {
  const d = new Date(s)
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
}

export default function Reports() {
  const [items, setItems] = useState<ReportMeta[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .getReports()
      .then((res) => setItems(res.items))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[40vh] text-slate-500 animate-pulse">
        리포트 목록 불러오는 중...
      </div>
    )
  }

  return (
    <div className="animate-fade-in">
      <h1 className="font-display font-bold text-2xl text-white mb-2">리포트 보관함</h1>
      <p className="text-slate-500 text-sm mb-8">
        과거 위클리 리포트를 날짜별로 조회할 수 있습니다. (Phase 2에서 PDF 다운로드 연동 예정)
      </p>
      <ul className="space-y-3">
        {items.map((r) => (
          <li
            key={r.id}
            className="flex items-center justify-between p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition"
          >
            <div>
              <p className="font-medium text-white">{r.title}</p>
              <p className="text-slate-500 text-sm">{formatDate(r.report_date)}</p>
            </div>
            <span className="text-slate-500 text-sm">다운로드 준비 중</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
