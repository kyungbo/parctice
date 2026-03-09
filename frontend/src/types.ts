export interface KeywordRank {
  rank: number
  keyword: string
  search_volume: number
  change_rate: number
  category?: string
}

export interface HotTreatment {
  keyword: string
  search_volume: number
  change_rate: number
  category: string
  rank: number
}

export interface RisingKeyword {
  keyword: string
  change_rate: number
  prev_volume: number
  current_volume: number
  category?: string
}

export interface CategoryTrend {
  category: string
  keywords: KeywordRank[]
  total_volume: number
}

export interface WeeklySummary {
  report_date: string
  hot_treatments: HotTreatment[]
  top10: KeywordRank[]
  rising: RisingKeyword[]
  falling: RisingKeyword[]
  by_category: CategoryTrend[]
}

export interface KeywordDetail {
  keyword: string
  category: string
  search_volume: number
  change_rate: number
  related_terms: { term: string; weight: number }[]
}

export interface ReportMeta {
  id: string
  report_date: string
  title: string
  summary?: string
}
