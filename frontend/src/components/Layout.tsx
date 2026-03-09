import { Link, useLocation } from 'react-router-dom'

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const nav = [
    { to: '/', label: '대시보드' },
    { to: '/reports', label: '리포트 보관함' },
  ]
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="font-display font-bold text-xl tracking-tight text-white">
            미용의료 마켓 트렌드
          </Link>
          <nav className="flex gap-6">
            {nav.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={`text-sm font-medium transition ${
                  location.pathname === to ? 'text-brand-400' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <footer className="border-t border-slate-800 py-4 text-center text-slate-500 text-xs">
        검색량은 관심도 지표이며, 실제 시술 횟수와 차이가 있을 수 있습니다.
      </footer>
    </div>
  )
}
