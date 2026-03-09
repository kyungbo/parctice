import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import KeywordDetail from './pages/KeywordDetail'
import Reports from './pages/Reports'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/keyword/:keyword" element={<KeywordDetail />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Layout>
  )
}
