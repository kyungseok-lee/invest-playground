// ETF types
export interface ETFSearchResult {
  ticker: string
  name: string
  category: string | null
}

export interface ETFSearchResponse {
  results: ETFSearchResult[]
}

export interface ETFDetail {
  ticker: string
  name: string
  category: string | null
  expense_ratio: number | null
  dividend_yield: number | null
  inception_date: string | null
  aum: number | null
  description: string | null
}

export interface PriceData {
  date: string
  close: number
  adj_close: number
  dividend: number
}

export interface ETFHistory {
  ticker: string
  prices: PriceData[]
}

// Simulation types
export type InvestmentType = 'lump_sum' | 'dca'
export type RebalancingFrequency = 'none' | 'quarterly' | 'yearly'

export interface PortfolioItem {
  ticker: string
  weight: number
}

export interface SimulationRequest {
  portfolio: PortfolioItem[]
  investment_type: InvestmentType
  initial_amount: number
  monthly_contribution: number
  start_date: string
  end_date: string
  rebalancing: RebalancingFrequency
}

export interface MonthlySnapshot {
  date: string
  portfolio_value: number
  invested_amount: number
  dividends_received: number
}

export interface SimulationSummary {
  total_invested: number
  final_value: number
  total_return_pct: number
  cagr: number
  mdd: number
  total_dividends: number
}

export interface SimulationResponse {
  summary: SimulationSummary
  monthly_data: MonthlySnapshot[]
}

// Comparison types
export interface ComparisonScenario {
  name: string
  portfolio: PortfolioItem[]
  investment_type: InvestmentType
  initial_amount: number
  monthly_contribution: number
}

export interface ComparisonRequest {
  scenarios: ComparisonScenario[]
  start_date: string
  end_date: string
  rebalancing: RebalancingFrequency
}

export interface ScenarioResult {
  name: string
  final_value: number
  total_invested: number
  total_return_pct: number
  cagr: number
  mdd: number
}

export interface ComparisonResponse {
  scenarios: ScenarioResult[]
}
