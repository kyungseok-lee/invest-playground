# ETF 장기 투자 시뮬레이터 PRD

## 1. 프로젝트 개요

### 1.1 프로젝트명
**ETF Investment Playground** - ETF 장기 투자 시뮬레이터

### 1.2 목적
투자 초보자가 미국 ETF를 중심으로 10~30년 장기 투자의 효과를 직접 시뮬레이션하고 학습할 수 있는 웹 애플리케이션

### 1.3 배경
- 투자 초보자들이 장기 투자의 복리 효과를 체감하기 어려움
- 실제 투자 전 다양한 시나리오를 테스트해볼 필요성
- 과거 데이터를 기반으로 한 백테스팅의 교육적 가치

---

## 2. 목표 사용자

### 2.1 주요 타겟
- 투자를 처음 시작하는 20~40대 직장인
- 장기 투자에 관심 있는 초보 투자자
- 적립식 투자(DCA)의 효과를 확인하고 싶은 사용자

### 2.2 사용자 요구사항
- 쉬운 UI/UX로 복잡한 투자 개념 이해
- 시각적인 그래프로 투자 성과 확인
- 다양한 ETF 비교 분석

---

## 3. 핵심 기능

### 3.1 ETF 검색 및 정보 조회
| 기능 | 설명 |
|------|------|
| ETF 검색 | 티커 심볼 또는 이름으로 ETF 검색 |
| ETF 상세 정보 | 운용사, 운용보수, 배당률, 설정일 등 기본 정보 표시 |
| 과거 수익률 | 1년/3년/5년/10년 수익률 표시 |

### 3.2 투자 시뮬레이션
| 기능 | 설명 |
|------|------|
| 일시불 투자 | 특정 금액을 한 번에 투자했을 때의 결과 시뮬레이션 |
| 적립식 투자 (DCA) | 매월/매주 정기 투자 시뮬레이션 |
| 투자 기간 설정 | 10년, 15년, 20년, 25년, 30년 선택 |
| 시작 시점 선택 | 과거 특정 날짜부터 시뮬레이션 시작 |

### 3.3 포트폴리오 구성
| 기능 | 설명 |
|------|------|
| 다중 ETF 선택 | 최대 5개 ETF로 포트폴리오 구성 |
| 비중 설정 | 각 ETF별 투자 비중(%) 설정 |
| 리밸런싱 | 연 1회/분기별 리밸런싱 옵션 |

### 3.4 결과 분석 및 시각화
| 기능 | 설명 |
|------|------|
| 자산 성장 그래프 | 시간에 따른 자산 가치 변화 라인 차트 |
| 투자 원금 vs 수익 | 원금과 수익을 구분한 스택 차트 |
| 연평균 수익률 (CAGR) | 복리 기준 연평균 수익률 계산 |
| 최대 낙폭 (MDD) | 최고점 대비 최대 하락률 표시 |
| 배당 수익 | 배당금 재투자 포함 총 수익 계산 |

### 3.5 비교 분석
| 기능 | 설명 |
|------|------|
| ETF 간 비교 | 여러 ETF의 과거 성과 비교 |
| 전략 비교 | 일시불 vs 적립식 투자 비교 |
| 벤치마크 비교 | S&P 500 등 벤치마크 대비 성과 비교 |

---

## 4. 기술 스택

### 4.1 Frontend
```
Framework: Next.js 14+ (App Router)
Language: TypeScript
Styling: Tailwind CSS
차트: Recharts 또는 Chart.js
상태관리: Zustand 또는 React Query
HTTP Client: Axios 또는 fetch
```

### 4.2 Backend
```
Framework: FastAPI (Python 3.11+)
데이터베이스: PostgreSQL (ETF 메타데이터 캐싱)
캐싱: Redis (API 응답 캐싱)
금융 데이터: yfinance 라이브러리
```

### 4.3 인프라 (선택사항)
```
컨테이너: Docker, Docker Compose
배포: Vercel (Frontend) + Railway/Render (Backend)
```

---

## 5. API 설계

### 5.1 ETF 관련 API

#### ETF 검색
```
GET /api/v1/etf/search?q={query}

Response:
{
  "results": [
    {
      "ticker": "VOO",
      "name": "Vanguard S&P 500 ETF",
      "category": "Large Cap Blend"
    }
  ]
}
```

#### ETF 상세 정보
```
GET /api/v1/etf/{ticker}

Response:
{
  "ticker": "VOO",
  "name": "Vanguard S&P 500 ETF",
  "expense_ratio": 0.03,
  "dividend_yield": 1.5,
  "inception_date": "2010-09-07",
  "aum": 350000000000,
  "category": "Large Cap Blend"
}
```

#### ETF 가격 히스토리
```
GET /api/v1/etf/{ticker}/history?start={date}&end={date}

Response:
{
  "ticker": "VOO",
  "prices": [
    {"date": "2020-01-01", "close": 302.5, "adj_close": 295.2, "dividend": 0},
    ...
  ]
}
```

### 5.2 시뮬레이션 API

#### 투자 시뮬레이션 실행
```
POST /api/v1/simulation/run

Request:
{
  "portfolio": [
    {"ticker": "VOO", "weight": 60},
    {"ticker": "QQQ", "weight": 40}
  ],
  "investment_type": "dca",  // "lump_sum" | "dca"
  "initial_amount": 1000000,
  "monthly_contribution": 500000,  // DCA인 경우
  "start_date": "2010-01-01",
  "end_date": "2024-01-01",
  "rebalancing": "yearly"  // "none" | "quarterly" | "yearly"
}

Response:
{
  "summary": {
    "total_invested": 85000000,
    "final_value": 250000000,
    "total_return_pct": 194.12,
    "cagr": 8.5,
    "mdd": -33.7,
    "total_dividends": 12000000
  },
  "monthly_data": [
    {
      "date": "2010-01-31",
      "portfolio_value": 1050000,
      "invested_amount": 1000000,
      "dividends_received": 0
    },
    ...
  ]
}
```

### 5.3 비교 분석 API

#### 전략 비교
```
POST /api/v1/simulation/compare

Request:
{
  "scenarios": [
    {
      "name": "일시불 투자",
      "portfolio": [{"ticker": "VOO", "weight": 100}],
      "investment_type": "lump_sum",
      "initial_amount": 50000000
    },
    {
      "name": "적립식 투자",
      "portfolio": [{"ticker": "VOO", "weight": 100}],
      "investment_type": "dca",
      "initial_amount": 0,
      "monthly_contribution": 500000
    }
  ],
  "start_date": "2014-01-01",
  "end_date": "2024-01-01"
}

Response:
{
  "scenarios": [
    {
      "name": "일시불 투자",
      "final_value": 150000000,
      "cagr": 11.6,
      ...
    },
    ...
  ]
}
```

---

## 6. 데이터 모델

### 6.1 ETF 메타데이터
```python
class ETF(BaseModel):
    ticker: str          # 티커 심볼 (PK)
    name: str            # ETF 이름
    category: str        # 카테고리
    expense_ratio: float # 운용보수 (%)
    dividend_yield: float # 배당률 (%)
    inception_date: date # 설정일
    aum: int             # 운용자산 (USD)
    description: str     # 설명
```

### 6.2 가격 데이터
```python
class PriceHistory(BaseModel):
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float    # 배당/분할 조정 종가
    volume: int
    dividend: float     # 배당금
```

### 6.3 시뮬레이션 결과
```python
class SimulationResult(BaseModel):
    total_invested: int       # 총 투자 원금
    final_value: int          # 최종 평가액
    total_return: float       # 총 수익률 (%)
    cagr: float               # 연평균 수익률 (%)
    mdd: float                # 최대 낙폭 (%)
    sharpe_ratio: float       # 샤프 비율
    total_dividends: int      # 총 배당금
    monthly_data: List[MonthlySnapshot]
```

---

## 7. 화면 구성

### 7.1 메인 페이지 (`/`)
- 서비스 소개
- 빠른 시뮬레이션 시작 버튼
- 인기 ETF 목록

### 7.2 ETF 탐색 페이지 (`/explore`)
- ETF 검색 바
- 카테고리별 필터 (주식형, 채권형, 섹터별 등)
- ETF 카드 리스트

### 7.3 ETF 상세 페이지 (`/etf/[ticker]`)
- ETF 기본 정보
- 과거 가격 차트
- 연도별 수익률 테이블
- "시뮬레이션에 추가" 버튼

### 7.4 시뮬레이션 페이지 (`/simulate`)
- 포트폴리오 구성 패널
  - ETF 선택 및 비중 설정
  - 투자 방식 선택 (일시불/적립식)
  - 투자 금액 입력
  - 투자 기간 설정
  - 리밸런싱 옵션
- 시뮬레이션 결과 패널
  - 자산 성장 그래프
  - 주요 지표 카드 (CAGR, MDD, 총 수익률)
  - 상세 데이터 테이블

### 7.5 비교 페이지 (`/compare`)
- 시나리오 추가/편집
- 비교 결과 그래프
- 시나리오별 지표 비교 테이블

### 7.6 학습 페이지 (`/learn`)
- 투자 용어 사전
- ETF 기초 가이드
- 장기 투자 전략 설명

---

## 8. UI/UX 요구사항

### 8.1 디자인 원칙
- **심플함**: 투자 초보자도 쉽게 이해할 수 있는 직관적 UI
- **시각화 중심**: 복잡한 데이터를 그래프로 표현
- **반응형**: 모바일/태블릿/데스크톱 지원
- **다크모드**: 라이트/다크 테마 지원

### 8.2 컬러 팔레트
```
Primary: #2563EB (Blue)
Success: #10B981 (Green) - 수익
Danger: #EF4444 (Red) - 손실
Background: #F8FAFC (Light) / #0F172A (Dark)
```

### 8.3 핵심 UX 요소
- 슬라이더로 투자 비중 조절
- 실시간 결과 미리보기
- 툴팁으로 용어 설명 제공
- 로딩 상태 스켈레톤 UI

---

## 9. 비기능적 요구사항

### 9.1 성능
- 시뮬레이션 API 응답: 3초 이내
- 페이지 로딩: LCP 2.5초 이내
- ETF 가격 데이터 캐싱 (1일 단위)

### 9.2 보안
- HTTPS 필수
- API Rate Limiting (분당 60회)
- 입력값 검증 및 Sanitization

### 9.3 확장성
- 미국 ETF → 향후 한국 ETF 지원 확장 고려
- 다국어 지원 구조 (i18n ready)

---

## 10. 프로젝트 구조

### 10.1 Frontend (Next.js)
```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # 메인 페이지
│   │   ├── explore/
│   │   │   └── page.tsx          # ETF 탐색
│   │   ├── etf/
│   │   │   └── [ticker]/
│   │   │       └── page.tsx      # ETF 상세
│   │   ├── simulate/
│   │   │   └── page.tsx          # 시뮬레이션
│   │   ├── compare/
│   │   │   └── page.tsx          # 비교
│   │   └── learn/
│   │       └── page.tsx          # 학습
│   ├── components/
│   │   ├── ui/                   # 공통 UI 컴포넌트
│   │   ├── charts/               # 차트 컴포넌트
│   │   ├── etf/                  # ETF 관련 컴포넌트
│   │   └── simulation/           # 시뮬레이션 컴포넌트
│   ├── lib/
│   │   ├── api.ts                # API 클라이언트
│   │   └── utils.ts              # 유틸 함수
│   ├── hooks/                    # Custom Hooks
│   ├── types/                    # TypeScript 타입
│   └── store/                    # 상태 관리
├── public/
├── tailwind.config.ts
├── next.config.js
└── package.json
```

### 10.2 Backend (FastAPI)
```
backend/
├── app/
│   ├── main.py                   # FastAPI 앱 진입점
│   ├── api/
│   │   ├── v1/
│   │   │   ├── etf.py            # ETF 라우터
│   │   │   ├── simulation.py     # 시뮬레이션 라우터
│   │   │   └── compare.py        # 비교 라우터
│   │   └── deps.py               # 의존성 주입
│   ├── core/
│   │   ├── config.py             # 설정
│   │   └── security.py           # 보안
│   ├── models/                   # Pydantic 모델
│   ├── services/
│   │   ├── etf_service.py        # ETF 데이터 서비스
│   │   ├── simulation_service.py # 시뮬레이션 로직
│   │   └── price_service.py      # 가격 데이터 서비스
│   ├── utils/
│   │   └── finance.py            # 금융 계산 유틸
│   └── db/
│       └── database.py           # DB 연결
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 11. 마일스톤

### Phase 1: MVP
- ETF 검색 및 기본 정보 조회
- 단일 ETF 일시불 투자 시뮬레이션
- 기본 자산 성장 그래프

### Phase 2: 핵심 기능
- 적립식 투자 (DCA) 시뮬레이션
- 포트폴리오 구성 (다중 ETF)
- 리밸런싱 옵션
- 주요 지표 (CAGR, MDD) 계산

### Phase 3: 고급 기능
- 시나리오 비교 기능
- 배당금 재투자 시뮬레이션
- 학습 콘텐츠 페이지

### Phase 4: 확장
- 사용자 계정 및 시뮬레이션 저장
- 한국 ETF 지원
- 모바일 앱 (PWA)

---

## 12. 참고 자료

### 12.1 대표 ETF 목록 (초기 지원)
| 티커 | 이름 | 카테고리 |
|------|------|----------|
| VOO | Vanguard S&P 500 ETF | 미국 대형주 |
| VTI | Vanguard Total Stock Market ETF | 미국 전체 시장 |
| QQQ | Invesco QQQ Trust | 나스닥 100 |
| VEA | Vanguard FTSE Developed Markets ETF | 선진국 |
| VWO | Vanguard FTSE Emerging Markets ETF | 신흥국 |
| BND | Vanguard Total Bond Market ETF | 미국 채권 |
| VNQ | Vanguard Real Estate ETF | 리츠 |
| GLD | SPDR Gold Shares | 금 |
| SCHD | Schwab US Dividend Equity ETF | 배당 |
| ARKK | ARK Innovation ETF | 혁신 기술 |

### 12.2 데이터 소스
- **yfinance**: Yahoo Finance API 래퍼 (무료, 과거 데이터)
- **Alpha Vantage**: 대안 API (일일 한도 있음)
- **ETF.com / ETFdb.com**: ETF 메타데이터 참고

---

## 13. 용어 정의

| 용어 | 설명 |
|------|------|
| DCA (Dollar Cost Averaging) | 정기적으로 일정 금액을 투자하는 적립식 투자 방법 |
| CAGR (Compound Annual Growth Rate) | 복리 기준 연평균 성장률 |
| MDD (Maximum Drawdown) | 최고점 대비 최대 하락률 |
| Expense Ratio | 운용 보수 (연간 %) |
| Rebalancing | 목표 비중에 맞게 포트폴리오 재조정 |
| Adj Close | 배당, 주식 분할 등을 반영한 조정 종가 |
