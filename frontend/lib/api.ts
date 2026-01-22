import axios from 'axios'
import type {
  ETFSearchResponse,
  ETFDetail,
  ETFHistory,
  SimulationRequest,
  SimulationResponse,
  ComparisonRequest,
  ComparisonResponse,
} from '@/types/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ETF endpoints
export const etfApi = {
  search: async (query: string): Promise<ETFSearchResponse> => {
    const response = await api.get(`/etf/search`, { params: { q: query } })
    return response.data
  },

  getDetail: async (ticker: string): Promise<ETFDetail> => {
    const response = await api.get(`/etf/${ticker}`)
    return response.data
  },

  getHistory: async (
    ticker: string,
    startDate: string,
    endDate: string
  ): Promise<ETFHistory> => {
    const response = await api.get(`/etf/${ticker}/history`, {
      params: {
        start: startDate,
        end: endDate,
      },
    })
    return response.data
  },
}

// Simulation endpoints
export const simulationApi = {
  run: async (request: SimulationRequest): Promise<SimulationResponse> => {
    const response = await api.post('/simulation/run', request)
    return response.data
  },

  compare: async (request: ComparisonRequest): Promise<ComparisonResponse> => {
    const response = await api.post('/simulation/compare', request)
    return response.data
  },
}
