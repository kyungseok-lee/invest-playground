# ETF Investment Simulator

ETF 장기 투자 시뮬레이터 - 과거 데이터를 기반으로 미국 ETF의 장기 투자 성과를 시뮬레이션하는 웹 애플리케이션입니다.

## 기술 스택

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Charts**: Recharts
- **State Management**: Zustand
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Package Manager**: uv
- **Database**: PostgreSQL
- **Data Source**: yfinance
- **ORM**: SQLAlchemy

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL 16

## 주요 기능

- 🔍 **ETF 검색 및 정보 조회**: 티커 심볼이나 이름으로 ETF 검색
- 📊 **투자 시뮬레이션**: 일시불 투자와 적립식 투자(DCA) 시뮬레이션
- 📈 **포트폴리오 구성**: 최대 5개 ETF로 포트폴리오 구성 및 비중 설정
- 🔄 **리밸런싱**: 분기별/연간 리밸런싱 옵션
- 📉 **성과 분석**: CAGR, MDD, 총 수익률 등 주요 지표 계산
- ⚖️ **전략 비교**: 여러 투자 전략을 동시에 비교

## 시작하기

### 사전 요구사항

로컬 개발을 위해 다음이 설치되어 있어야 합니다:

- Docker & Docker Compose
- Node.js 20+ (로컬 개발 시)
- Python 3.12+ (로컬 개발 시)
- uv (Python 패키지 매니저)

### Docker로 전체 애플리케이션 실행

```bash
# 1. 저장소 클론
git clone <repository-url>
cd invest-playground

# 2. Docker Compose로 모든 서비스 실행
docker-compose up --build

# 서비스 접속:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 로컬 개발 환경 설정

로컬에서 개발할 때는 PostgreSQL만 Docker로 실행하고, Backend와 Frontend는 로컬에서 실행합니다.

#### 1. PostgreSQL 실행

```bash
# PostgreSQL만 실행
docker-compose -f docker-compose.dev.yml up -d
```

#### 2. Backend 개발 서버 실행

```bash
cd backend

# 환경 변수 설정
cp .env.example .env

# 의존성 설치 (uv 사용)
uv sync

# 개발 서버 실행
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API는 http://localhost:8000에서 실행됩니다.
API 문서는 http://localhost:8000/docs에서 확인할 수 있습니다.

#### 3. Frontend 개발 서버 실행

```bash
cd frontend

# 환경 변수 설정
cp .env.local.example .env.local

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

Frontend는 http://localhost:3000에서 실행됩니다.

## 프로젝트 구조

```
invest-playground/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API 라우터
│   │   │   └── v1/
│   │   │       ├── etf.py
│   │   │       └── simulation.py
│   │   ├── core/           # 설정
│   │   │   └── config.py
│   │   ├── db/             # 데이터베이스
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── models/         # Pydantic 모델
│   │   │   ├── etf.py
│   │   │   └── simulation.py
│   │   ├── services/       # 비즈니스 로직
│   │   │   ├── etf_service.py
│   │   │   └── simulation_service.py
│   │   ├── utils/          # 유틸리티
│   │   │   └── finance.py
│   │   └── main.py         # FastAPI 앱
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/               # Next.js Frontend
│   ├── app/               # App Router 페이지
│   │   ├── simulate/
│   │   ├── explore/
│   │   ├── compare/
│   │   └── page.tsx
│   ├── components/        # React 컴포넌트
│   │   ├── ui/           # 공통 UI 컴포넌트
│   │   └── layout/       # 레이아웃 컴포넌트
│   ├── lib/              # 유틸리티
│   │   ├── api.ts        # API 클라이언트
│   │   └── utils.ts
│   ├── types/            # TypeScript 타입
│   │   └── api.ts
│   ├── Dockerfile
│   └── package.json
│
├── docs/                  # 문서
│   └── PRD.md
│
├── docker-compose.yml         # 프로덕션 Docker Compose
├── docker-compose.dev.yml     # 개발용 Docker Compose (PostgreSQL만)
└── README.md
```

## API 엔드포인트

### ETF 관련

- `GET /api/v1/etf/search?q={query}` - ETF 검색
- `GET /api/v1/etf/{ticker}` - ETF 상세 정보
- `GET /api/v1/etf/{ticker}/history` - ETF 가격 히스토리

### 시뮬레이션

- `POST /api/v1/simulation/run` - 투자 시뮬레이션 실행
- `POST /api/v1/simulation/compare` - 전략 비교

자세한 API 문서는 http://localhost:8000/docs에서 확인하세요.

## 환경 변수

### Backend (.env)

```env
DEBUG=false
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/etf_simulator
CORS_ORIGINS=["http://localhost:3000"]
CACHE_TTL_SECONDS=86400
RATE_LIMIT_PER_MINUTE=60
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 개발 가이드

### Backend 개발

```bash
# 테스트 실행
cd backend
uv run pytest

# 코드 포맷팅
uv run ruff format .

# 린팅
uv run ruff check .
```

### Frontend 개발

```bash
# 테스트 실행
cd frontend
npm test

# 린팅
npm run lint

# 빌드
npm run build
```

## 배포

### Docker를 사용한 배포

```bash
# 이미지 빌드
docker-compose build

# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### 개별 배포

각 서비스(Backend, Frontend)는 독립적으로 배포 가능합니다.
Dockerfile을 사용하여 컨테이너 이미지를 빌드하고 배포하세요.

## 트러블슈팅

### PostgreSQL 연결 오류

```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose ps

# PostgreSQL 로그 확인
docker-compose logs postgres

# PostgreSQL 재시작
docker-compose restart postgres
```

### Backend API 오류

```bash
# Backend 로그 확인
docker-compose logs backend

# Backend 재시작
docker-compose restart backend
```

### Frontend 빌드 오류

```bash
# node_modules 재설치
cd frontend
rm -rf node_modules .next
npm install
npm run build
```

## 라이선스

MIT

## 참고 자료

- [PRD 문서](./docs/PRD.md)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Next.js 문서](https://nextjs.org/docs)
- [shadcn/ui 문서](https://ui.shadcn.com/)
