import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import { api } from '../api'
import type { WeeklySummary } from '../types'

const formatDate = (s: string) => {
  const d = new Date(s)
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
}

const formatVolume = (n: number) => (n >= 10000 ? `${(n / 10000).toFixed(1)}만` : String(n))
const changeColor = (r: number) => (r >= 0 ? 'text-emerald-400' : 'text-red-400')

export default function Dashboard() {
  const [data, setData] = useState<WeeklySummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .getWeeklyTrends()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-pulse text-slate-500">트렌드 데이터 불러오는 중...</div>
      </div>
    )
  }
  if (error || !data) {
    return (
      <div className="rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3">
        데이터를 불러올 수 없습니다. 백엔드가 실행 중인지 확인해 주세요. (오류: {error})
      </div>
    )
  }

  const hotChartData = data.hot_treatments.map((h) => ({
    name: h.keyword,
    검색량: h.search_volume,
    상승률: h.change_rate,
    category: h.category,
  }))
  const COLORS = ['#ec4899', '#f472b6', '#fb7185']

  return (
    <div className="space-y-10 animate-fade-in">
      <div>
        <h1 className="font-display font-bold text-2xl sm:text-3xl text-white mb-1">
          이번 주 검색 트렌드
        </h1>
        <p className="text-slate-500 text-sm">
          리포트 기준일: {formatDate(data.report_date)} · 네이버 검색 트렌드 기반
        </p>
      </div>

      {/* HOT 시술 3 */}
      <section className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6 sm:p-8">
        <h2 className="font-display font-semibold text-lg text-white mb-6 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-brand-500 animate-pulse" />
          이번 주 HOT 시술 TOP 3
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="h-64 sm:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={hotChartData} layout="vertical" margin={{ left: 20, right: 20 }}>
                <XAxis type="number" tickFormatter={formatVolume} stroke="#64748b" fontSize={12} />
                <YAxis type="category" dataKey="name" width={80} stroke="#64748b" fontSize={13} />
                <Tooltip
                  contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                  labelStyle={{ color: '#f1f5f9' }}
                  formatter={(value: number, name: string, props: { payload: { 상승률: number } }) =>
                    name === '검색량' ? [formatVolume(value), '검색량'] : [`${props.payload.상승률.toFixed(1)}%`, '전주 대비']
                  }
                />
                <Bar dataKey="검색량" radius={[0, 6, 6, 0]} maxBarSize={48}>
                  {hotChartData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-col justify-center gap-4">
            {data.hot_treatments.map((h, i) => (
              <Link
                key={h.keyword}
                to={`/keyword/${encodeURIComponent(h.keyword)}`}
                className="flex items-center gap-4 p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 hover:border-brand-500/50 hover:bg-slate-800/80 transition"
              >
                <span className="flex items-center justify-center w-10 h-10 rounded-lg bg-brand-500/20 text-brand-400 font-bold">
                  {i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-white truncate">{h.keyword}</p>
                  <p className="text-slate-500 text-sm">{h.category} · 검색량 {formatVolume(h.search_volume)}</p>
                </div>
                <span className={`font-semibold tabular-nums ${changeColor(h.change_rate)}`}>
                  +{h.change_rate.toFixed(1)}%
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* TOP 10 & 급상승/급하락 */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <section className="xl:col-span-2 rounded-2xl bg-slate-900/60 border border-slate-800 p-6">
          <h2 className="font-display font-semibold text-lg text-white mb-4">검색어 TOP 10</h2>
          <ul className="space-y-2">
            {data.top10.map((k) => (
              <li key={k.keyword}>
                <Link
                  to={`/keyword/${encodeURIComponent(k.keyword)}`}
                  className="flex items-center gap-3 py-2.5 px-3 rounded-lg hover:bg-slate-800/60 transition"
                >
                  <span className="w-6 text-slate-500 text-sm font-medium">{k.rank}</span>
                  <span className="flex-1 font-medium text-white">{k.keyword}</span>
                  {k.category && (
                    <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
                      {k.category}
                    </span>
                  )}
                  <span className="text-slate-400 text-sm tabular-nums">{formatVolume(k.search_volume)}</span>
                  <span className={`text-sm font-medium tabular-nums w-14 text-right ${changeColor(k.change_rate)}`}>
                    {k.change_rate >= 0 ? '+' : ''}{k.change_rate.toFixed(1)}%
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
        <section className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6">
          <h2 className="font-display font-semibold text-lg text-white mb-4">급상승 · 급하락</h2>
          <div className="space-y-6">
            <div>
              <p className="text-slate-500 text-xs font-medium mb-2">급상승 키워드</p>
              <ul className="space-y-1.5">
                {data.rising.slice(0, 5).map((r) => (
                  <li key={r.keyword}>
                    <Link
                      to={`/keyword/${encodeURIComponent(r.keyword)}`}
                      className="flex justify-between items-center py-1.5 text-sm hover:text-brand-400 transition"
                    >
                      <span className="text-white font-medium truncate">{r.keyword}</span>
                      <span className="text-emerald-400 font-medium tabular-nums shrink-0 ml-2">
                        +{r.change_rate.toFixed(1)}%
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-slate-500 text-xs font-medium mb-2">급하락 키워드</p>
              <ul className="space-y-1.5">
                {data.falling.map((f) => (
                  <li key={f.keyword}>
                    <Link
                      to={`/keyword/${encodeURIComponent(f.keyword)}`}
                      className="flex justify-between items-center py-1.5 text-sm hover:text-brand-400 transition"
                    >
                      <span className="text-white font-medium truncate">{f.keyword}</span>
                      <span className="text-red-400 font-medium tabular-nums shrink-0 ml-2">
                        {f.change_rate.toFixed(1)}%
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      </div>

      {/* 카테고리별 */}
      <section className="rounded-2xl bg-slate-900/60 border border-slate-800 p-6">
        <h2 className="font-display font-semibold text-lg text-white mb-4">카테고리별 트렌드</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.by_category.map((cat) => (
            <div
              key={cat.category}
              className="rounded-xl bg-slate-800/50 border border-slate-700/60 p-4"
            >
              <div className="flex justify-between items-center mb-3">
                <span className="font-medium text-white">{cat.category}</span>
                <span className="text-slate-500 text-sm">{formatVolume(cat.total_volume)}</span>
              </div>
              <ul className="space-y-1.5">
                {cat.keywords.map((k) => (
                  <li key={k.keyword}>
                    <Link
                      to={`/keyword/${encodeURIComponent(k.keyword)}`}
                      className="flex justify-between text-sm hover:text-brand-400 transition"
                    >
                      <span className="text-slate-300 truncate">{k.keyword}</span>
                      <span className={`tabular-nums shrink-0 ml-2 ${changeColor(k.change_rate)}`}>
                        {k.change_rate >= 0 ? '+' : ''}{k.change_rate.toFixed(1)}%
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
