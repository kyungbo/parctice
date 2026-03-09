import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api'
import type { KeywordDetail as KeywordDetailType } from '../types'

const formatVolume = (n: number) => (n >= 10000 ? `${(n / 10000).toFixed(1)}만` : String(n))
const changeColor = (r: number) => (r >= 0 ? 'text-emerald-400' : 'text-red-400')

export default function KeywordDetail() {
  const { keyword } = useParams<{ keyword: string }>()
  const [data, setData] = useState<KeywordDetailType | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!keyword) return
    api
      .getKeywordDetail(keyword)
      .then(setData)
      .finally(() => setLoading(false))
  }, [keyword])

  if (!keyword) {
    return (
      <div className="text-slate-500">키워드가 지정되지 않았습니다.</div>
    )
  }
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[40vh] text-slate-500 animate-pulse">
        로딩 중...
      </div>
    )
  }
  if (!data) {
    return (
      <div className="text-slate-500">키워드 정보를 불러올 수 없습니다.</div>
    )
  }

  const maxWeight = Math.max(...data.related_terms.map((t) => t.weight), 1)
  const minSize = 14
  const sizeRange = 20

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <Link to="/" className="inline-flex items-center gap-1 text-slate-500 hover:text-slate-300 text-sm mb-6">
        ← 대시보드
      </Link>
      <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6 sm:p-8">
        <h1 className="font-display font-bold text-2xl text-white mb-2">{data.keyword}</h1>
        <p className="text-slate-500 text-sm mb-6">
          {data.category} · 검색량 {formatVolume(data.search_volume)}
          <span className={`ml-2 font-medium ${changeColor(data.change_rate)}`}>
            전주 대비 {data.change_rate >= 0 ? '+' : ''}{data.change_rate.toFixed(1)}%
          </span>
        </p>
        <div className="border-t border-slate-700 pt-6">
          <h2 className="font-display font-semibold text-lg text-white mb-4">연관 검색어</h2>
          <div className="flex flex-wrap gap-3">
            {data.related_terms.map((t) => {
              const size = minSize + (sizeRange * (t.weight / maxWeight))
              return (
                <span
                  key={t.term}
                  className="inline-block px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-slate-300 hover:border-brand-500/50 hover:text-brand-300 transition"
                  style={{ fontSize: `${Math.round(size)}px` }}
                >
                  {t.term}
                </span>
              )
            })}
          </div>
          <p className="text-slate-500 text-xs mt-4">
            효과, 부작용, 가격 등 사용자 관심 키워드입니다. (실제 서비스에서는 검색 연관어 API로 제공)
          </p>
        </div>
      </div>
    </div>
  )
}
