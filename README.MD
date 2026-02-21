<div align="center">

<img src="docs/assets/logoisteah.jpg" alt="ISTEAH Logo" height="90" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="docs/assets/synapsbranch.png" alt="SynapsBranch Logo" height="90" />

<br/>

# SynapsBranch

### 🌐 Plateforme d'Analyse, de Performance et de Sécurité Web Automatisée avec Génération de Rapports IA

<br/>

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Cache-Redis-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE.txt)

<br/>

---

**University:** Institut des Sciences, des Technologies et des Études Avancées d'Haïti (ISTEAH)
**Course:** LOG2000 — Software Engineering
**Instructor:** Prof. Dupuy Rony Charles
**Assignment:** Assignment 1 | **Author:** JOSEPH Samuel Jonathan

---

</div>

<br/>

## 📖 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Architecture](#-architecture)
4. [Tech Stack](#-tech-stack)
5. [Project Structure](#-project-structure)
6. [Prerequisites](#-prerequisites)
7. [Installation & Setup](#-installation--setup)
8. [Environment Variables](#-environment-variables)
9. [Scan Modules](#-scan-modules)
10. [API Endpoints](#-api-endpoints)
11. [Database](#-database)
12. [Docker Deployment](#-docker-deployment)
13. [Authors](#-authors)

---

## 🚀 Overview

**SynapsBranch** is a complete web analysis platform that allows any user to submit a website URL and automatically run a **comprehensive suite of tests** covering:

- 🔌 **Connectivity & DNS** — Resolution, propagation, DNSSEC, geolocation
- 🔒 **SSL/TLS** — Certificates, protocols, known vulnerabilities
- ⚡ **Performance** — Load testing up to 1000 concurrent users (Locust)
- 🛡️ **DAST Security** — XSS, injections, security headers, CORS
- 📈 **SEO & Indexing** — Meta tags, Core Web Vitals, sitemap, accessibility

Results are displayed **in real time** on a live dashboard via WebSocket, then a **custom AI-generated PDF report** (Claude / OpenAI) is automatically sent by email.

### User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. User logs in (Email / Google / GitHub)                      │
│  2. Submits the target website URL                              │
│  3. Scan launches automatically                                 │
│  4. Watches tests run LIVE on the dashboard                     │
│  5. Modules execute in sequence:                                │
│     → Connectivity & DNS  →  SSL/TLS  →  Performance           │
│     → DAST Security       →  SEO & Indexing                     │
│  6. AI analyzes all results                                     │
│  7. A PDF report is generated with charts & recommendations     │
│  8. Report is sent by email (HTML + PDF attachment)             │
│  9. User browses their scan history                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 **Multi-method Auth** | Email/Password, Google OAuth, GitHub OAuth, email verification |
| 📡 **Live WebSocket Dashboard** | Real-time scan visualization, terminal-style logs |
| ⚡ **Advanced Load Testing** | 5 tiers: 1 → 50 → 100 → 500 → 1000 concurrent users |
| 🛡️ **DAST Scan** | Vulnerability detection (XSS, missing headers, insecure cookies) |
| 🔒 **SSL/TLS Analysis** | Grade A+ to F, Heartbleed, POODLE, BEAST detection |
| 🌐 **Full DNS Testing** | A, AAAA, MX, NS, TXT, SOA, DNSSEC, multi-server propagation |
| 📊 **AI Report** | Structured analysis by Claude/OpenAI, prioritized recommendations |
| 📄 **PDF Generation** | Full report with Matplotlib charts, sent via Resend |
| 📧 **Automated Emails** | Verification, password reset, scan report, welcome |
| 🐳 **Full Docker** | Multi-stage builds, Nginx reverse proxy, full Compose setup |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          DOCKER COMPOSE                              │
│                                                                      │
│  ┌─────────────────────┐         ┌──────────────────────────┐        │
│  │   FRONTEND (Next.js)│         │   BACKEND (FastAPI)      │        │
│  │   Port: 3000        │◄───────►│   Port: 8000             │        │
│  │                     │  REST   │                          │        │
│  │  - Pages & UI       │  + WSS  │  - Auth (JWT)            │        │
│  │  - shadcn/ui        │         │  - Scan Engine           │        │
│  │  - Tailwind CSS     │         │  - WebSocket Server      │        │
│  │  - Recharts         │         │  - AI Report Generator   │        │
│  │  - WebSocket Client │         │  - PDF Generator         │        │
│  └─────────────────────┘         └──────────┬───────────────┘        │
│                                              │                       │
│                                   ┌──────────▼───────────┐           │
│                                   │   PostgreSQL 16       │           │
│                                   │   Port: 5432          │           │
│                                   └──────────┬───────────┘           │
│                                              │                       │
│                                   ┌──────────▼───────────┐           │
│                                   │   Redis 7             │           │
│                                   │   Port: 6379          │           │
│                                   │   Cache + Task Queue  │           │
│                                   └──────────────────────┘           │
└──────────────────────────────────────────────────────────────────────┘

Services externes :  Resend  │  Google OAuth  │  GitHub OAuth  │  Claude/OpenAI
```

### Pipeline WebSocket (Live Testing)

```
┌──────────┐    WebSocket     ┌──────────┐    Redis PubSub    ┌──────────┐
│ Frontend │◄────────────────►│ FastAPI  │◄──────────────────►│  Celery  │
│ (Browser)│  scan:{scan_id}  │ WS Server│  scan_channel:{id} │  Worker  │
└──────────┘                  └──────────┘                    └──────────┘
```

---

## 🛠️ Tech Stack

### Frontend

| Technology | Usage |
|---|---|
| **Next.js 14+** (App Router) | React framework, SSR, routing |
| **TypeScript 5** | Static typing |
| **Tailwind CSS** | Utility-first styling |
| **shadcn/ui** | UI components (Dialog, Card, Table, Badge, Toast…) |
| **Recharts** | Charts (Line, Bar, Pie, Area, Radar) |
| **Framer Motion** | Animations & transitions |
| **Socket.io-client** | Real-time WebSocket |
| **React Hook Form + Zod** | Forms & validation |
| **Zustand** | State management |
| **next-auth** | Frontend authentication |

### Backend

| Technology | Usage |
|---|---|
| **FastAPI** | Python API framework, native async |
| **Python 3.11+** | Backend language |
| **SQLAlchemy + Alembic** | ORM + migrations |
| **PostgreSQL 16** | Primary database |
| **Redis 7** | Cache, task queue, WebSocket pub/sub |
| **Celery** | Async scan execution |
| **Pydantic v2** | Data validation |
| **PassLib + python-jose** | bcrypt hashing + JWT |
| **httpx / aiohttp** | Async HTTP requests |

### Scan Tools

| Tool | Usage |
|---|---|
| **Locust** | Load testing (1 → 1000 users) |
| **OWASP ZAP** (via API) | DAST security scanning |
| **sslyze** | SSL/TLS analysis |
| **dnspython** | DNS resolution & validation |
| **BeautifulSoup + lxml** | HTML parsing for SEO |

### Report Generation

| Technology | Usage |
|---|---|
| **Claude API / OpenAI API** | AI analysis & report writing |
| **WeasyPrint** | PDF generation |
| **Matplotlib** | Charts inside the PDF |
| **Jinja2** | HTML templates for PDF & emails |
| **Resend** | Email delivery service |

---

## 📁 Project Structure

```
synapsbranch/
├── 📄 docker-compose.yml
├── 📄 docker-compose.prod.yml
├── 📄 .env.example
├── 📄 README.md
│
├── 📂 frontend/                        # Next.js Application
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── components.json                 # shadcn config
│   │
│   └── src/
│       ├── app/
│       │   ├── (auth)/                 # Login, Register, Verify, Reset
│       │   ├── (dashboard)/            # Dashboard, Live Scan, History
│       │   └── api/auth/               # NextAuth routes
│       │
│       ├── components/
│       │   ├── ui/                     # shadcn components
│       │   ├── layout/                 # Sidebar, Header, Footer
│       │   ├── scan/                   # ScanForm, ScanProgress, LiveTerminal
│       │   ├── results/                # SSL, DNS, SEO, Security Panels
│       │   ├── charts/                 # ResponseTime, LoadTest, RadarScore
│       │   └── report/                 # ReportViewer, ReportActions
│       │
│       ├── hooks/                      # useScan, useLiveResults, useAuth
│       ├── stores/                     # Zustand (scanStore, authStore)
│       └── types/                      # TypeScript interfaces
│
├── 📂 backend/                         # FastAPI Application
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   │
│   └── app/
│       ├── main.py                     # FastAPI entry point
│       ├── config.py                   # Settings via pydantic-settings
│       ├── api/v1/                     # REST Routers (auth, scans, reports)
│       ├── core/                       # Database, Redis, Security (JWT)
│       ├── models/                     # SQLAlchemy (User, Scan, Report)
│       ├── schemas/                    # Pydantic v2 schemas
│       ├── services/                   # Auth, Email (Resend), AI Report
│       ├── scanners/                   # DNS, SSL, Performance, Security, SEO
│       ├── workers/                    # Celery app & tasks
│       ├── websocket/                  # WebSocket manager
│       └── templates/                  # Jinja2 (PDF, emails)
│
├── 📂 docs/                            # Documentation & assets
│   ├── concept.md
│   └── assets/
│       ├── logoisteah.jpg
│       └── synapsbranch.png
│
└── 📂 nginx/
    └── nginx.conf                      # Production reverse proxy
```

---

## 📦 Prerequisites

Make sure you have the following tools installed:

| Tool | Min. Version | Check |
|---|---|---|
| **Docker** | 24+ | `docker --version` |
| **Docker Compose** | 2.x | `docker compose version` |
| **Python** | 3.11+ | `python --version` |
| **Node.js** | 20+ | `node --version` |
| **Git** | 2.x | `git --version` |

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/synapsbranch.git
cd synapsbranch
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your keys (see [Environment Variables](#-environment-variables)).

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The application will be available at:

| Service | URL |
|---|---|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |
| **PostgreSQL** | localhost:5432 |
| **Redis** | localhost:6379 |

### 4. Local development (without Docker)

#### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows (PowerShell)
# source venv/bin/activate          # Linux/macOS
pip install -r requirements.txt
alembic upgrade head                # Apply migrations
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in each value:

```env
# ──── Database ────
DATABASE_URL=postgresql://user:password@db:5432/synapsbranch

# ──── Redis ────
REDIS_URL=redis://redis:6379/0

# ──── JWT ────
JWT_SECRET=change-this-secret-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ──── OAuth ────
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx

# ──── Email (Resend) ────
RESEND_API_KEY=re_xxxxxxxxxxxx
EMAIL_FROM=SynapsBranch <reports@synapsbranch.app>

# ──── AI ────
AI_PROVIDER=claude                  # or "openai"
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# ──── Frontend ────
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000

# ──── App ────
APP_NAME=SynapsBranch
APP_ENV=development
CORS_ORIGINS=http://localhost:3000
```

---

## 🔬 Scan Modules

### Module 1 — Connectivity & DNS

| Test | Tool |
|---|---|
| A, AAAA, MX, NS, TXT, SOA resolution | `dnspython` |
| DNSSEC validation | `dnspython` |
| Propagation (Google, Cloudflare, OpenDNS) | `dnspython` |
| Ping, latency, traceroute | `ping3` / subprocess |
| Port scan (80, 443, 8080) | `socket` |
| HTTP → HTTPS redirect check | `httpx` |
| IP Geolocation | GeoIP database |

### Module 2 — SSL/TLS Analysis

Each scan produces a **grade from A+ to F**:

| Grade | Criteria |
|---|---|
| **A+** | TLS 1.2+, HSTS, no vulnerabilities, key ≥ 2048 bits |
| **A** | TLS 1.2+, no vulnerabilities |
| **B** | TLS 1.1 accepted or weak cipher suites |
| **C** | TLS 1.0 accepted |
| **D** | Vulnerabilities detected |
| **F** | Expired or invalid certificate |

Tests: Heartbleed, POODLE, BEAST, CRIME, ROBOT, OCSP Stapling, CT Logs.

### Module 3 — Performance (Load Testing)

| Tier | Users | Duration |
|---|---|---|
| 1 | **1 user** | 30 s |
| 2 | **50 users** | 60 s |
| 3 | **100 users** | 60 s |
| 4 | **500 users** | 90 s |
| 5 | **1000 users** | 120 s |

Metrics: response time (avg, P50, P95, P99), throughput (req/s), error rate, TTFB, active connections.

### Module 4 — DAST Security

Severities: **Critical** → **High** → **Medium** → **Low** → **Info**

Tests: SQL Injection, XSS (Reflected, Stored, DOM), security headers (CSP, HSTS, X-Frame-Options), cookies (Secure, HttpOnly, SameSite), CORS, Clickjacking, Open Redirect, Mixed Content.

### Module 5 — SEO & Indexing

Score out of 100 across 5 categories:

| Category | Weight |
|---|---|
| Meta tags (title, description, canonical) | 20% |
| Content (H1, alt texts, text ratio) | 25% |
| Technical (Core Web Vitals, compression) | 25% |
| Mobile (responsive, tap targets) | 15% |
| Indexing (robots.txt, sitemap, JSON-LD) | 15% |

---

## 🌐 API Endpoints

### Authentication

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register with email |
| `POST` | `/api/v1/auth/login` | Login |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |
| `POST` | `/api/v1/auth/logout` | Logout |
| `GET` | `/api/v1/auth/verify-email` | Email verification |
| `POST` | `/api/v1/auth/forgot-password` | Request password reset |
| `POST` | `/api/v1/auth/reset-password` | Reset password |
| `POST` | `/api/v1/auth/oauth/google` | Google OAuth callback |
| `POST` | `/api/v1/auth/oauth/github` | GitHub OAuth callback |

### Scans

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/v1/scans` | Launch a scan |
| `GET` | `/api/v1/scans` | Scan history |
| `GET` | `/api/v1/scans/{id}` | Scan details |
| `GET` | `/api/v1/scans/{id}/results` | Results by module |
| `DELETE` | `/api/v1/scans/{id}` | Delete a scan |
| `WS` | `/ws/scan/{id}` | Live WebSocket |

### Reports

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/v1/reports/{scan_id}` | AI report |
| `GET` | `/api/v1/reports/{scan_id}/pdf` | Download PDF |
| `POST` | `/api/v1/reports/{scan_id}/email` | Resend by email |

---

## 🗄️ Database

### Simplified Schema

```
users ─────────────────────────────────┐
│ id (UUID PK)                         │
│ email, password_hash, name           │
│ auth_provider, is_verified           │
└──────────────────────────────────────┘
              │ 1:N
scans ─────────────────────────────────┐
│ id (UUID PK)                         │
│ user_id (FK), url, status            │
│ overall_score, current_phase         │
│ started_at, completed_at             │
└──────────────────────────────────────┘
    │ 1:N                    │ 1:1
scan_results                reports
│ module                    │ ai_analysis (JSONB)
│ score, grade              │ pdf_path
│ data (JSONB)              │ email_sent
│ issues_critical/high/med  └──────────────────
└──────────────────────────
```

Main tables: `users`, `scans`, `scan_results`, `reports`, `refresh_tokens`

---

## 🐳 Docker Deployment

### Docker Compose Services

| Service | Image | Port |
|---|---|---|
| `frontend` | Node.js 20 Alpine (multi-stage) | 3000 |
| `backend` | Python 3.11 Slim | 8000 |
| `celery_worker` | Python 3.11 Slim | — |
| `db` | PostgreSQL 16 Alpine | 5432 |
| `redis` | Redis 7 Alpine | 6379 |
| `nginx` | Nginx Alpine | 80, 443 |

### Run in production

```bash
docker compose -f docker-compose.prod.yml up -d
```

---

## 👥 Authors

<div align="center">

| Role | Name |
|---|---|
| **Lead Developer** | JOSEPH Samuel Jonathan |
| **Supervising Instructor** | Prof. Dupuy Rony Charles |
| **Institution** | Institut des Sciences, des Technologies et des Études Avancées d'Haïti (ISTEAH) |
| **Course** | LOG2000 — Software Engineering |

</div>

---

<div align="center">

Made with ❤️ for **LOG2000 — Software Engineering**
**ISTEAH** | Assignment 1 | 2025–2026

<img src="docs/assets/logoisteah.jpg" alt="ISTEAH" height="50" />

</div>
