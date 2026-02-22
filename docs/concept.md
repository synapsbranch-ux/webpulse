# 🚀 synapsbranch — Plan de Projet Complet

> **Plateforme d'Analyse, de Performance et de Sécurité Web Automatisée avec Génération de Rapports IA**

---

## 📋 Table des Matières

1. [Vue d'ensemble du Projet](#1-vue-densemble-du-projet)
2. [Architecture Technique](#2-architecture-technique)
3. [Stack Technologique](#3-stack-technologique)
4. [Structure du Projet](#4-structure-du-projet)
5. [Module 1 — Authentification & Utilisateurs](#5-module-1--authentification--utilisateurs)
6. [Module 2 — Tests de Performance & Load Testing](#6-module-2--tests-de-performance--load-testing)
7. [Module 3 — Tests de Connectivité & DNS](#7-module-3--tests-de-connectivité--dns)
8. [Module 4 — Analyse SSL/TLS](#8-module-4--analyse-ssltls)
9. [Module 5 — Sécurité DAST](#9-module-5--sécurité-dast)
10. [Module 6 — SEO & Indexation](#10-module-6--seo--indexation)
11. [Module 7 — Live Testing & Visualisation Temps Réel](#11-module-7--live-testing--visualisation-temps-réel)
12. [Module 8 — Génération de Rapport IA](#12-module-8--génération-de-rapport-ia)
13. [Module 9 — Système d'Emails & Notifications](#13-module-9--système-demails--notifications)
14. [Module 10 — Docker & Déploiement](#14-module-10--docker--déploiement)
15. [Base de Données — Schéma Complet](#15-base-de-données--schéma-complet)
16. [API Endpoints](#16-api-endpoints)
17. [Pages & Routes Frontend](#17-pages--routes-frontend)
18. [Pipeline d'Exécution d'un Scan](#18-pipeline-dexécution-dun-scan)
19. [Planning & Phases de Développement](#19-planning--phases-de-développement)
20. [Variables d'Environnement](#20-variables-denvironnement)

---

## 1. Vue d'ensemble du Projet

### Concept

synapsbranch est une plateforme SaaS qui permet à un utilisateur de soumettre l'URL de son site web et de lancer automatiquement une batterie complète de tests couvrant la performance, la sécurité, la connectivité, le SSL et le SEO. Les résultats sont affichés en temps réel dans un dashboard live, puis un rapport complet est généré par une IA, formaté en PDF avec graphiques et envoyé par email.

### Flux Utilisateur Principal

```
┌─────────────────────────────────────────────────────────────────┐
│  1. L'utilisateur se connecte (Email/Google/GitHub)             │
│  2. Il entre l'URL de son site web                              │
│  3. Le scan se lance automatiquement                            │
│  4. Il observe les tests en LIVE sur le dashboard               │
│  5. Chaque module s'exécute séquentiellement :                  │
│     → Connectivité & DNS                                        │
│     → SSL / TLS                                                 │
│     → Performance (1, 50, 100, 500, 1000 users)                 │
│     → Sécurité DAST                                             │
│     → SEO & Indexation                                          │
│  6. L'IA analyse tous les résultats                             │
│  7. Un rapport PDF est généré avec graphiques & recommandations │
│  8. Le rapport est envoyé par email (template + pièce jointe)   │
│  9. L'utilisateur consulte son historique de scans               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture Technique

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
│  │  - Charts (Recharts)│         │  - AI Report Generator   │        │
│  │  - WebSocket Client │         │  - PDF Generator         │        │
│  │                     │         │  - Email Service          │        │
│  └─────────────────────┘         └──────────┬───────────────┘        │
│                                              │                       │
│                                   ┌──────────▼───────────┐           │
│                                   │   PostgreSQL          │           │
│                                   │   Port: 5432          │           │
│                                   └──────────┬───────────┘           │
│                                              │                       │
│                                   ┌──────────▼───────────┐           │
│                                   │   Redis               │           │
│                                   │   Port: 6379          │           │
│                                   │   (Cache + Task Queue)│           │
│                                   └──────────────────────┘           │
└──────────────────────────────────────────────────────────────────────┘

Services externes :
  → Resend (Emails)
  → Google OAuth 2.0
  → GitHub OAuth
  → Claude / OpenAI API (Génération de rapport IA)
```

---

## 3. Stack Technologique

### Frontend

| Technologie | Usage |
|---|---|
| **Next.js 14+** (App Router) | Framework React, SSR, routing |
| **TypeScript** | Typage statique |
| **Tailwind CSS** | Styling utility-first |
| **shadcn/ui** | Composants UI (Dialog, Card, Table, Badge, Toast…) |
| **Recharts** | Graphiques (Line, Bar, Pie, Area, Radar) |
| **Framer Motion** | Animations et transitions |
| **Socket.io-client** | WebSocket pour le live testing |
| **React Hook Form + Zod** | Formulaires et validation |
| **Zustand** | State management global |
| **next-auth** | Authentification côté frontend |

### Backend

| Technologie | Usage |
|---|---|
| **FastAPI** | Framework API Python, async natif |
| **Python 3.11+** | Langage backend |
| **SQLAlchemy + Alembic** | ORM + migrations |
| **PostgreSQL** | Base de données principale |
| **Redis** | Cache, file d'attente des tâches, pub/sub WebSocket |
| **Celery** | Exécution asynchrone des tâches de scan |
| **WebSocket (FastAPI)** | Communication temps réel |
| **Pydantic v2** | Validation des données |
| **PassLib + python-jose** | Hashing mots de passe + JWT |
| **httpx / aiohttp** | Requêtes HTTP async |

### Outils de Scan

| Outil | Usage |
|---|---|
| **Locust** | Load testing (1, 50, 100, 500, 1000 users) |
| **OWASP ZAP** (via API) | Scan DAST de sécurité |
| **sslyze** | Analyse SSL/TLS |
| **dnspython** | Résolution DNS |
| **BeautifulSoup + lxml** | Parsing HTML pour SEO |
| **Lighthouse CLI** (via Puppeteer) | Métriques de performance & SEO |

### Génération de Rapports

| Technologie | Usage |
|---|---|
| **Claude API / OpenAI API** | Analyse IA et rédaction du rapport |
| **WeasyPrint** ou **ReportLab** | Génération PDF |
| **Matplotlib / Plotly** | Graphiques dans le PDF |
| **Jinja2** | Templates HTML pour le PDF |

### Emails

| Technologie | Usage |
|---|---|
| **Resend** | Service d'envoi d'emails |
| **react-email** | Templates d'email modernes (côté build) |
| **Jinja2** | Templates HTML côté backend |

### Infrastructure

| Technologie | Usage |
|---|---|
| **Docker** | Conteneurisation (2 images : frontend + backend) |
| **Docker Compose** | Orchestration locale |
| **Nginx** | Reverse proxy (production) |

---

## 4. Structure du Projet

```
synapsbranch/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── README.md
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── components.json                 # shadcn config
│   │
│   ├── public/
│   │   ├── logo.svg
│   │   └── images/
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx              # Layout global
│   │   │   ├── page.tsx                # Landing page
│   │   │   ├── globals.css
│   │   │   │
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   ├── register/page.tsx
│   │   │   │   ├── verify-email/page.tsx
│   │   │   │   ├── forgot-password/page.tsx
│   │   │   │   └── reset-password/page.tsx
│   │   │   │
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx          # Dashboard layout (sidebar)
│   │   │   │   ├── dashboard/page.tsx  # Vue d'ensemble
│   │   │   │   ├── new-scan/page.tsx   # Lancer un nouveau scan
│   │   │   │   ├── scan/
│   │   │   │   │   └── [id]/
│   │   │   │   │       ├── page.tsx    # Résultats du scan (LIVE)
│   │   │   │   │       └── report/page.tsx  # Rapport IA
│   │   │   │   ├── history/page.tsx    # Historique des scans
│   │   │   │   ├── settings/page.tsx   # Paramètres utilisateur
│   │   │   │   └── billing/page.tsx    # (futur) Facturation
│   │   │   │
│   │   │   └── api/
│   │   │       └── auth/
│   │   │           └── [...nextauth]/route.ts
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                     # shadcn components
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── MobileNav.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   └── SocialButtons.tsx
│   │   │   ├── scan/
│   │   │   │   ├── ScanForm.tsx
│   │   │   │   ├── ScanProgress.tsx
│   │   │   │   ├── LiveTerminal.tsx    # Terminal-like live output
│   │   │   │   └── PhaseIndicator.tsx
│   │   │   ├── results/
│   │   │   │   ├── PerformancePanel.tsx
│   │   │   │   ├── SecurityPanel.tsx
│   │   │   │   ├── SSLPanel.tsx
│   │   │   │   ├── DNSPanel.tsx
│   │   │   │   ├── SEOPanel.tsx
│   │   │   │   ├── ScoreGauge.tsx
│   │   │   │   └── MetricCard.tsx
│   │   │   ├── charts/
│   │   │   │   ├── ResponseTimeChart.tsx
│   │   │   │   ├── LoadTestChart.tsx
│   │   │   │   ├── ErrorRateChart.tsx
│   │   │   │   ├── ThroughputChart.tsx
│   │   │   │   └── RadarScore.tsx
│   │   │   └── report/
│   │   │       ├── ReportViewer.tsx
│   │   │       └── ReportActions.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts                  # Client API (axios/fetch)
│   │   │   ├── auth.ts                 # NextAuth config
│   │   │   ├── socket.ts              # WebSocket client
│   │   │   ├── utils.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useScan.ts
│   │   │   ├── useLiveResults.ts
│   │   │   └── useAuth.ts
│   │   │
│   │   ├── stores/
│   │   │   ├── scanStore.ts
│   │   │   └── authStore.ts
│   │   │
│   │   └── types/
│   │       ├── scan.ts
│   │       ├── auth.ts
│   │       └── report.ts
│   │
│   └── emails/                         # react-email templates
│       ├── VerifyEmail.tsx
│       ├── ResetPassword.tsx
│       ├── ScanComplete.tsx
│       └── ReportEmail.tsx
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── alembic.ini
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app entry
│   │   ├── config.py                   # Settings (pydantic-settings)
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py                 # Dependencies (get_db, get_current_user)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py           # Router principal
│   │   │       ├── auth.py             # Endpoints auth
│   │   │       ├── scans.py            # Endpoints scans
│   │   │       ├── reports.py          # Endpoints rapports
│   │   │       ├── users.py            # Endpoints utilisateurs
│   │   │       └── webhooks.py         # Webhooks OAuth
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py             # JWT, hashing, OAuth
│   │   │   ├── database.py             # SQLAlchemy engine & session
│   │   │   └── redis.py                # Redis client
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── scan.py
│   │   │   ├── scan_result.py
│   │   │   └── report.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── scan.py
│   │   │   ├── result.py
│   │   │   └── report.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── scan_orchestrator.py    # Orchestre tous les modules
│   │   │   ├── email_service.py        # Resend integration
│   │   │   └── report_service.py       # Génération rapport IA + PDF
│   │   │
│   │   ├── scanners/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Classe abstraite BaseScanner
│   │   │   ├── dns_scanner.py          # Tests DNS & Connectivité
│   │   │   ├── ssl_scanner.py          # Tests SSL/TLS
│   │   │   ├── performance_scanner.py  # Load testing (Locust)
│   │   │   ├── security_scanner.py     # DAST (ZAP)
│   │   │   └── seo_scanner.py          # SEO & Indexation
│   │   │
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py           # Config Celery
│   │   │   └── tasks.py                # Tâches async
│   │   │
│   │   ├── websocket/
│   │   │   ├── __init__.py
│   │   │   └── manager.py              # WebSocket connection manager
│   │   │
│   │   ├── templates/
│   │   │   ├── report.html             # Template Jinja2 pour PDF
│   │   │   ├── email_report.html       # Template email rapport
│   │   │   └── email_verify.html       # Template email vérification
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── pdf_generator.py
│   │       └── chart_generator.py
│   │
│   ├── migrations/                     # Alembic
│   │   ├── env.py
│   │   └── versions/
│   │
│   └── tests/
│       ├── test_auth.py
│       ├── test_scanners.py
│       └── test_reports.py
│
└── nginx/
    └── nginx.conf                      # Reverse proxy config
```

---

## 5. Module 1 — Authentification & Utilisateurs

### 5.1 Méthodes d'Authentification

| Méthode | Détails |
|---|---|
| **Email + Mot de passe** | Inscription → Email de vérification → Connexion |
| **Google OAuth 2.0** | Connexion via Google (NextAuth + backend callback) |
| **GitHub OAuth** | Connexion via GitHub (NextAuth + backend callback) |

### 5.2 Flux d'Inscription Email

```
1. POST /api/v1/auth/register
   → Body: { email, password, name }
   → Crée l'utilisateur (is_verified = false)
   → Génère un token de vérification (JWT, expire 24h)
   → Envoie l'email via Resend avec lien de vérification

2. GET /api/v1/auth/verify-email?token=xxx
   → Vérifie le token JWT
   → Met à jour is_verified = true
   → Redirige vers /login?verified=true

3. POST /api/v1/auth/login
   → Vérifie email + mot de passe (bcrypt)
   → Vérifie que is_verified = true
   → Retourne access_token (JWT, 30min) + refresh_token (7 jours)

4. POST /api/v1/auth/refresh
   → Renouvelle l'access_token via le refresh_token
```

### 5.3 Flux OAuth (Google / GitHub)

```
1. Frontend : Bouton "Se connecter avec Google/GitHub"
   → Redirige vers le provider OAuth via NextAuth

2. Callback NextAuth → appelle le backend :
   POST /api/v1/auth/oauth
   → Body: { provider, provider_id, email, name, avatar_url }
   → Crée ou retrouve l'utilisateur
   → is_verified = true automatiquement
   → Retourne access_token + refresh_token

3. Le frontend stocke les tokens et redirige vers /dashboard
```

### 5.4 Mot de passe oublié

```
1. POST /api/v1/auth/forgot-password  → { email }
   → Envoie email avec lien de réinitialisation (token JWT, 1h)

2. POST /api/v1/auth/reset-password   → { token, new_password }
   → Vérifie le token → Met à jour le mot de passe
```

### 5.5 Sécurité

- Mots de passe hashés avec **bcrypt** (cost factor 12)
- JWT signé avec **HS256** (secret dans les env vars)
- Rate limiting : **5 tentatives / minute** sur login
- Protection CSRF avec tokens
- Headers de sécurité (CORS, X-Frame-Options, etc.)

---

## 6. Module 2 — Tests de Performance & Load Testing

### 6.1 Objectif

Simuler un nombre croissant d'utilisateurs concurrents pour mesurer les limites du site cible.

### 6.2 Niveaux de Charge

| Palier | Utilisateurs | Durée | Objectif |
|---|---|---|---|
| 1 | **1 user** | 30 sec | Baseline — temps de réponse nominal |
| 2 | **50 users** | 60 sec | Charge légère — comportement normal |
| 3 | **100 users** | 60 sec | Charge modérée — premiers signes de stress |
| 4 | **500 users** | 90 sec | Charge forte — identifier les goulots |
| 5 | **1000 users** | 120 sec | Charge extrême — point de rupture |

### 6.3 Métriques Collectées (par palier)

| Métrique | Description |
|---|---|
| **Temps de réponse moyen** (ms) | Moyenne de toutes les requêtes |
| **P50 / P95 / P99** (ms) | Percentiles de latence |
| **Throughput** (req/sec) | Nombre de requêtes traitées par seconde |
| **Taux d'erreur** (%) | Pourcentage de requêtes HTTP 4xx/5xx |
| **Taux de succès** (%) | Pourcentage de requêtes HTTP 2xx |
| **Time to First Byte** (TTFB) | Temps avant le premier octet reçu |
| **Débit** (KB/sec) | Volume de données transférées |
| **Connexions actives** | Nombre de connexions TCP maintenues |
| **Erreurs réseau** | Timeouts, connexions refusées |

### 6.4 Implémentation Technique

```python
# backend/app/scanners/performance_scanner.py

class PerformanceScanner(BaseScanner):
    """
    Utilise Locust en mode headless (library mode) pour simuler
    les utilisateurs concurrents.
    """

    LOAD_LEVELS = [
        {"users": 1,    "duration": 30,  "spawn_rate": 1},
        {"users": 50,   "duration": 60,  "spawn_rate": 10},
        {"users": 100,  "duration": 60,  "spawn_rate": 20},
        {"users": 500,  "duration": 90,  "spawn_rate": 50},
        {"users": 1000, "duration": 120, "spawn_rate": 100},
    ]

    async def run(self, url: str, websocket_callback):
        results = []
        for level in self.LOAD_LEVELS:
            # Envoyer le statut en live
            await websocket_callback({
                "phase": "performance",
                "status": f"Testing with {level['users']} users...",
                "current_level": level["users"]
            })

            # Lancer Locust en mode library
            metrics = await self._run_locust(url, level)
            results.append(metrics)

            # Envoyer les résultats en live
            await websocket_callback({
                "phase": "performance",
                "level_complete": level["users"],
                "metrics": metrics
            })

        return self._analyze_results(results)
```

### 6.5 Données Live Envoyées (WebSocket)

Pendant chaque palier, le backend envoie toutes les **2 secondes** :

```json
{
  "type": "performance_live",
  "data": {
    "current_users": 100,
    "elapsed_seconds": 34,
    "live_metrics": {
      "avg_response_time": 245,
      "current_rps": 890,
      "error_count": 2,
      "active_connections": 98
    }
  }
}
```

---

## 7. Module 3 — Tests de Connectivité & DNS

### 7.1 Tests Effectués

| Test | Description | Outils |
|---|---|---|
| **Résolution DNS** | Résoudre A, AAAA, MX, NS, TXT, SOA, CNAME | `dnspython` |
| **Temps de résolution** | Mesurer le temps de résolution DNS | `dnspython` + timing |
| **Propagation DNS** | Vérifier la propagation sur plusieurs serveurs DNS publics | Google (8.8.8.8), Cloudflare (1.1.1.1), OpenDNS |
| **DNSSEC** | Vérifier si DNSSEC est activé et valide | `dnspython` |
| **Ping / Latence** | Temps de réponse ICMP | `ping3` ou subprocess |
| **Traceroute** | Chemin réseau vers le serveur | subprocess |
| **Port scan basique** | Vérifier les ports 80, 443, 8080, 8443 | `socket` |
| **HTTP/HTTPS redirect** | Vérifier les redirections HTTP → HTTPS | `httpx` |
| **IPv4 / IPv6** | Vérifier la double-stack IP | `dnspython` |
| **Géolocalisation IP** | Localiser le serveur | Base GeoIP |

### 7.2 Structure du Résultat

```json
{
  "dns": {
    "resolution_time_ms": 23,
    "records": {
      "A": ["104.21.35.12", "172.67.180.45"],
      "AAAA": ["2606:4700:3030::6815:230c"],
      "MX": [{"priority": 1, "host": "aspmx.l.google.com"}],
      "NS": ["ns1.example.com", "ns2.example.com"],
      "TXT": ["v=spf1 include:_spf.google.com ~all"],
      "SOA": { "primary_ns": "ns1.example.com", "serial": 2024010101 }
    },
    "dnssec_enabled": true,
    "propagation": {
      "google": true,
      "cloudflare": true,
      "opendns": true
    }
  },
  "connectivity": {
    "ping_ms": 12,
    "ports": { "80": "open", "443": "open", "8080": "closed" },
    "http_to_https_redirect": true,
    "ipv6_supported": true,
    "server_location": { "country": "US", "city": "San Francisco" }
  }
}
```

---

## 8. Module 4 — Analyse SSL/TLS

### 8.1 Tests Effectués

| Test | Description |
|---|---|
| **Validité du certificat** | Dates de début/fin, jours restants |
| **Chaîne de certificats** | Vérifier la chaîne complète jusqu'au CA racine |
| **Protocoles supportés** | TLS 1.0, 1.1, 1.2, 1.3 (identifier les obsolètes) |
| **Cipher suites** | Lister et classer les suites cryptographiques |
| **Vulnérabilités connues** | Heartbleed, POODLE, BEAST, CRIME, ROBOT |
| **HSTS** | Vérifier le header Strict-Transport-Security |
| **OCSP Stapling** | Vérifier si activé |
| **Certificate Transparency** | Vérifier les CT Logs |
| **Key size** | Taille de clé RSA/ECDSA |
| **Signature algorithm** | SHA-256, SHA-384, etc. |

### 8.2 Scoring SSL

| Grade | Critères |
|---|---|
| **A+** | TLS 1.2+, HSTS activé, pas de vulnérabilités, clé ≥ 2048 bits |
| **A** | TLS 1.2+, pas de vulnérabilités |
| **B** | TLS 1.1 accepté ou cipher suites faibles |
| **C** | TLS 1.0 accepté |
| **D** | Vulnérabilités détectées |
| **F** | Certificat expiré ou invalide |

### 8.3 Implémentation

```python
# backend/app/scanners/ssl_scanner.py

from sslyze import Scanner, ServerScanRequest, ScanCommand

class SSLScanner(BaseScanner):
    SCAN_COMMANDS = [
        ScanCommand.CERTIFICATE_INFO,
        ScanCommand.SSL_2_0_CIPHER_SUITES,
        ScanCommand.SSL_3_0_CIPHER_SUITES,
        ScanCommand.TLS_1_0_CIPHER_SUITES,
        ScanCommand.TLS_1_1_CIPHER_SUITES,
        ScanCommand.TLS_1_2_CIPHER_SUITES,
        ScanCommand.TLS_1_3_CIPHER_SUITES,
        ScanCommand.HEARTBLEED,
        ScanCommand.OPENSSL_CCS_INJECTION,
        ScanCommand.TLS_COMPRESSION,
    ]
```

---

## 9. Module 5 — Sécurité DAST

### 9.1 Tests de Vulnérabilité

| Catégorie | Tests |
|---|---|
| **Injection** | SQL Injection, XSS (Reflected, Stored, DOM), Command Injection |
| **Headers de sécurité** | CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy |
| **Cookies** | Flags Secure, HttpOnly, SameSite |
| **Information Disclosure** | Server header, X-Powered-By, stack traces, directory listing |
| **CORS** | Vérifier la politique CORS |
| **Clickjacking** | Test d'iframe |
| **Open Redirect** | Détection de redirections non sécurisées |
| **Subresource Integrity** | Vérifier les SRI sur les scripts/CSS externes |
| **Mixed Content** | Détecter le contenu HTTP chargé en HTTPS |
| **Rate Limiting** | Vérifier si les endpoints sont protégés |

### 9.2 Classification des Vulnérabilités

| Sévérité | Exemples | CVSS |
|---|---|---|
| **Critique** | SQL Injection, RCE | 9.0 – 10.0 |
| **Haute** | XSS Stored, CSRF sans protection | 7.0 – 8.9 |
| **Moyenne** | Headers manquants, cookies non sécurisés | 4.0 – 6.9 |
| **Basse** | Information disclosure, server banner | 0.1 – 3.9 |
| **Info** | Recommandations, bonnes pratiques | 0.0 |

### 9.3 Implémentation (2 approches)

**Approche 1 — OWASP ZAP (Docker)** :

```python
class DastSecurityScanner(BaseScanner):
    """Utilise l'API OWASP ZAP pour le scan DAST"""

    async def run(self, url: str, websocket_callback):
        # 1. Spider le site
        await self.zap.spider.scan(url)

        # 2. Scan actif
        scan_id = await self.zap.ascan.scan(url)

        # 3. Poll le statut et envoyer en live
        while self.zap.ascan.status(scan_id) < 100:
            progress = self.zap.ascan.status(scan_id)
            await websocket_callback({
                "phase": "security",
                "progress": progress,
                "alerts_found": len(self.zap.core.alerts())
            })
            await asyncio.sleep(2)

        # 4. Récupérer les alertes
        return self._format_alerts(self.zap.core.alerts())
```

**Approche 2 — Scanner custom (léger, sans ZAP)** :

```python
class LightSecurityScanner(BaseScanner):
    """Scanner custom qui vérifie headers, cookies, XSS basique"""

    async def check_security_headers(self, response):
        headers_to_check = {
            "Content-Security-Policy": "CSP",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY/SAMEORIGIN",
            "Strict-Transport-Security": "HSTS",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "Permissions",
        }
        # ...
```

---

## 10. Module 6 — SEO & Indexation

### 10.1 Tests Effectués

| Catégorie | Tests |
|---|---|
| **Balises Meta** | title, description, viewport, robots, canonical, og:*, twitter:* |
| **Structure HTML** | H1 unique, hiérarchie H1-H6, attributs alt sur images |
| **Performance** | Core Web Vitals (LCP, FID, CLS), taille de page, nombre de requêtes |
| **Mobile** | Responsive, viewport meta, tap targets |
| **Indexation** | robots.txt, sitemap.xml, meta robots, noindex/nofollow |
| **Liens** | Liens cassés (404), liens internes/externes, redirections |
| **Contenu** | Ratio texte/HTML, longueur du contenu, mots-clés dans les titres |
| **Technique** | Minification CSS/JS, compression Gzip/Brotli, cache headers |
| **Structured Data** | JSON-LD, schema.org |
| **Accessibilité** | Contraste, ARIA, lang attribute |

### 10.2 Score SEO (sur 100)

| Catégorie | Poids | Critères |
|---|---|---|
| **Meta tags** | 20% | Title (60 chars), description (160 chars), canonical |
| **Contenu** | 25% | H1 unique, hiérarchie, ratio texte, alt images |
| **Technique** | 25% | Core Web Vitals, compression, minification |
| **Mobile** | 15% | Responsive, viewport, tap targets |
| **Indexation** | 15% | robots.txt, sitemap, structured data |

---

## 11. Module 7 — Live Testing & Visualisation Temps Réel

### 11.1 Architecture WebSocket

```
┌──────────┐    WebSocket     ┌──────────┐     Redis PubSub    ┌──────────┐
│ Frontend │◄────────────────►│ FastAPI  │◄────────────────────►│ Celery   │
│ (Browser)│  scan:{scan_id}  │ WS Server│   scan_channel:{id}  │ Worker   │
└──────────┘                  └──────────┘                      └──────────┘
```

### 11.2 Messages WebSocket (Backend → Frontend)

**Changement de phase :**

```json
{
  "type": "phase_change",
  "data": {
    "phase": "ssl",
    "phase_index": 2,
    "total_phases": 5,
    "status": "running"
  }
}
```

**Progression en temps réel :**

```json
{
  "type": "progress",
  "data": {
    "phase": "performance",
    "progress_percent": 45,
    "message": "Testing with 100 users — 34s elapsed",
    "live_metrics": { ... }
  }
}
```

**Log live (style terminal) :**

```json
{
  "type": "log",
  "data": {
    "timestamp": "2025-01-15T14:32:05Z",
    "level": "info",
    "message": "✓ DNS resolution successful: 23ms",
    "phase": "dns"
  }
}
```

**Résultat d'un module :**

```json
{
  "type": "module_complete",
  "data": {
    "phase": "ssl",
    "score": 95,
    "grade": "A+",
    "summary": "SSL configuration is excellent",
    "issues_count": { "critical": 0, "high": 0, "medium": 1, "low": 2 }
  }
}
```

**Scan terminé :**

```json
{
  "type": "scan_complete",
  "data": {
    "overall_score": 82,
    "duration_seconds": 340,
    "report_generating": true
  }
}
```

### 11.3 Interface Live Dashboard

Le dashboard de scan en live affiche :

```
┌──────────────────────────────────────────────────────────────┐
│  synapsbranch — Scanning https://example.com                     │
│  ══════════════════════════════════════════                   │
│                                                              │
│  Progress: ████████████░░░░░░░░ 62%   Phase 3/5             │
│                                                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │ DNS  │ │ SSL  │ │ PERF │ │ DAST │ │ SEO  │              │
│  │  ✓   │ │  ✓   │ │  ⟳   │ │  ○   │ │  ○   │              │
│  │  A+  │ │  A   │ │ ...  │ │ wait │ │ wait │              │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘              │
│                                                              │
│  ┌─ LIVE METRICS ──────────────────────────────────────┐     │
│  │                                                      │     │
│  │  Current Test: 100 Users  |  Elapsed: 34s            │     │
│  │                                                      │     │
│  │  Avg Response: 245ms  ▲   Throughput: 890 req/s  ▲   │     │
│  │  Error Rate:   0.2%   ▼   Active Conn: 98        ─   │     │
│  │                                                      │     │
│  │  [====== Live Response Time Chart ======]            │     │
│  │  [====== Live Throughput Chart    ======]            │     │
│  │                                                      │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌─ LIVE TERMINAL ─────────────────────────────────────┐     │
│  │  14:32:01 [DNS]  ✓ A record: 104.21.35.12 (23ms)   │     │
│  │  14:32:01 [DNS]  ✓ AAAA record found                │     │
│  │  14:32:02 [DNS]  ✓ DNSSEC validated                 │     │
│  │  14:32:05 [SSL]  ✓ Certificate valid (298 days)     │     │
│  │  14:32:06 [SSL]  ✓ TLS 1.3 supported                │     │
│  │  14:32:06 [SSL]  ⚠ TLS 1.0 still enabled            │     │
│  │  14:32:10 [PERF] → Starting load test: 1 user       │     │
│  │  14:32:42 [PERF] ✓ 1 user: avg 120ms, 0% errors    │     │
│  │  14:32:43 [PERF] → Starting load test: 50 users     │     │
│  │  14:33:45 [PERF] ✓ 50 users: avg 180ms, 0% errors  │     │
│  │  14:33:46 [PERF] → Starting load test: 100 users    │     │
│  │  14:34:20 [PERF] ◌ 100 users: avg 245ms, 34s...    │     │
│  └──────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

---

## 12. Module 8 — Génération de Rapport IA

### 12.1 Pipeline de Génération

```
1. Collecte de tous les résultats (JSON)
2. Envoi à l'API Claude / OpenAI avec un prompt structuré
3. L'IA génère :
   → Résumé exécutif
   → Analyse détaillée par module
   → Classification des problèmes (Critique → Info)
   → Solutions concrètes pour chaque problème
   → Score global et scores par catégorie
4. Génération des graphiques (Matplotlib/Plotly)
5. Assemblage du PDF (Jinja2 + WeasyPrint)
6. Sauvegarde en BDD + envoi par email
```

### 12.2 Prompt IA (Template)

```
Tu es un expert en analyse de performance, sécurité et SEO web.
Voici les résultats complets d'un scan du site {url} :

{json_results}

Génère un rapport d'analyse structuré en JSON avec :

1. "executive_summary": Résumé de 3-5 phrases
2. "overall_score": Score global sur 100
3. "scores_by_category": { "performance": X, "security": X, "ssl": X, "dns": X, "seo": X }
4. "critical_issues": [ { "title", "description", "category", "severity", "solution" } ]
5. "warnings": [ ... ]
6. "passed_checks": [ ... ]
7. "recommendations": [ { "priority", "title", "description", "impact", "effort" } ]
8. "performance_analysis": Analyse détaillée des résultats de charge
9. "security_analysis": Analyse des vulnérabilités
10. "seo_analysis": Analyse SEO avec quick wins
```

### 12.3 Structure du Rapport PDF

```
┌─────────────────────────────────────────┐
│  synapsbranch — RAPPORT D'ANALYSE           │
│  https://example.com                     │
│  Généré le 15 janvier 2025              │
├─────────────────────────────────────────┤
│                                         │
│  1. RÉSUMÉ EXÉCUTIF                     │
│     Score Global: 82/100                │
│     [Graphique radar des 5 catégories]  │
│                                         │
│  2. SCORES PAR CATÉGORIE                │
│     [Barres horizontales colorées]      │
│     Performance: 78/100                 │
│     Sécurité:    85/100                 │
│     SSL/TLS:     95/100                 │
│     DNS:         90/100                 │
│     SEO:         72/100                 │
│                                         │
│  3. PROBLÈMES CRITIQUES (2)             │
│     🔴 SQL Injection potentielle        │
│     🔴 TLS 1.0 encore actif            │
│                                         │
│  4. AVERTISSEMENTS (5)                  │
│     🟡 Temps de réponse > 500ms à 500u │
│     🟡 CSP header manquant             │
│     ...                                 │
│                                         │
│  5. ANALYSE DE PERFORMANCE              │
│     [Graphique: Response Time vs Users] │
│     [Graphique: Throughput vs Users]    │
│     [Graphique: Error Rate vs Users]    │
│                                         │
│  6. ANALYSE DE SÉCURITÉ                 │
│     [Liste des vulnérabilités]          │
│     [Graphique: répartition sévérités]  │
│                                         │
│  7. ANALYSE SEO                         │
│     [Score breakdown]                   │
│     [Quick wins identifiés]             │
│                                         │
│  8. RECOMMANDATIONS PRIORITAIRES        │
│     [Tableau: priorité, impact, effort] │
│                                         │
└─────────────────────────────────────────┘
```

---

## 13. Module 9 — Système d'Emails & Notifications

### 13.1 Templates d'Email

| Template | Trigger | Contenu |
|---|---|---|
| **Vérification d'email** | Inscription | Lien de vérification, expire 24h |
| **Réinitialisation MDP** | Forgot password | Lien de reset, expire 1h |
| **Bienvenue** | Première connexion | Guide de démarrage |
| **Scan terminé** | Fin de scan | Résumé rapide + lien vers le rapport |
| **Rapport complet** | Rapport IA prêt | Template formaté + PDF en pièce jointe |

### 13.2 Service d'Email (Resend)

```python
# backend/app/services/email_service.py

import resend
from pathlib import Path

class EmailService:
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY

    async def send_report_email(self, user, scan, pdf_path: Path):
        """Envoie le rapport par email avec le PDF en pièce jointe"""
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()

        html = self._render_template("email_report.html", {
            "user_name": user.name,
            "site_url": scan.url,
            "overall_score": scan.overall_score,
            "scores": scan.scores_by_category,
            "critical_count": scan.critical_count,
            "scan_date": scan.created_at.strftime("%d/%m/%Y"),
        })

        resend.Emails.send({
            "from": "synapsbranch <reports@synapsbranch.app>",
            "to": [user.email],
            "subject": f"Rapport synapsbranch — {scan.url} ({scan.overall_score}/100)",
            "html": html,
            "attachments": [{
                "filename": f"synapsbranch-report-{scan.id}.pdf",
                "content": list(pdf_content),
            }]
        })
```

### 13.3 Template Email du Rapport

L'email contient :
- Header avec le logo synapsbranch
- Score global en grand avec code couleur (vert/jaune/rouge)
- Mini-barres pour chaque catégorie
- Nombre de problèmes critiques / warnings
- Top 3 des recommandations
- Bouton CTA "Voir le rapport complet"
- PDF en pièce jointe

---

## 14. Module 10 — Docker & Déploiement

### 14.1 Dockerfile Frontend

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

### 14.2 Dockerfile Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps pour sslyze, ZAP, etc.
RUN apt-get update && apt-get install -y \
    gcc libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 14.3 Docker Compose

```yaml
# docker-compose.yml
version: "3.9"

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_WS_URL=ws://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/synapsbranch
      - REDIS_URL=redis://redis:6379/0
      - RESEND_API_KEY=${RESEND_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID}
      - GITHUB_CLIENT_SECRET=${GITHUB_CLIENT_SECRET}
      - AI_API_KEY=${AI_API_KEY}
    depends_on:
      - db
      - redis

  celery_worker:
    build: ./backend
    command: celery -A app.workers.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/synapsbranch
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=synapsbranch
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend

volumes:
  pgdata:
```

---

## 15. Base de Données — Schéma Complet

### 15.1 Table `users`

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Identifiant unique |
| `email` | VARCHAR(255) UNIQUE | Email |
| `password_hash` | VARCHAR(255) NULL | Hash bcrypt (NULL si OAuth only) |
| `name` | VARCHAR(100) | Nom complet |
| `avatar_url` | TEXT NULL | URL de l'avatar |
| `is_verified` | BOOLEAN | Email vérifié |
| `is_active` | BOOLEAN | Compte actif |
| `auth_provider` | ENUM('email','google','github') | Méthode d'auth |
| `provider_id` | VARCHAR(255) NULL | ID du provider OAuth |
| `created_at` | TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | Dernière modification |

### 15.2 Table `scans`

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Identifiant unique |
| `user_id` | UUID (FK → users) | Propriétaire |
| `url` | TEXT | URL scannée |
| `status` | ENUM('pending','running','completed','failed') | Statut |
| `current_phase` | VARCHAR(50) | Phase en cours |
| `overall_score` | INTEGER NULL | Score global (0-100) |
| `started_at` | TIMESTAMP | Début du scan |
| `completed_at` | TIMESTAMP NULL | Fin du scan |
| `duration_seconds` | INTEGER NULL | Durée totale |
| `created_at` | TIMESTAMP | Date de création |

### 15.3 Table `scan_results`

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Identifiant unique |
| `scan_id` | UUID (FK → scans) | Scan parent |
| `module` | ENUM('dns','ssl','performance','security','seo') | Module |
| `score` | INTEGER | Score du module (0-100) |
| `grade` | VARCHAR(5) | Note (A+, A, B, C, D, F) |
| `data` | JSONB | Résultats complets (JSON) |
| `issues_critical` | INTEGER | Nombre de problèmes critiques |
| `issues_high` | INTEGER | Nombre de problèmes hauts |
| `issues_medium` | INTEGER | Nombre de problèmes moyens |
| `issues_low` | INTEGER | Nombre de problèmes bas |
| `created_at` | TIMESTAMP | Date de création |

### 15.4 Table `reports`

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Identifiant unique |
| `scan_id` | UUID (FK → scans) | Scan associé |
| `ai_analysis` | JSONB | Analyse IA complète (JSON) |
| `pdf_path` | TEXT | Chemin du fichier PDF |
| `email_sent` | BOOLEAN | Email envoyé |
| `email_sent_at` | TIMESTAMP NULL | Date d'envoi |
| `created_at` | TIMESTAMP | Date de création |

### 15.5 Table `refresh_tokens`

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Identifiant unique |
| `user_id` | UUID (FK → users) | Utilisateur |
| `token` | VARCHAR(500) | Token hashé |
| `expires_at` | TIMESTAMP | Date d'expiration |
| `is_revoked` | BOOLEAN | Révoqué |
| `created_at` | TIMESTAMP | Date de création |

---

## 16. API Endpoints

### Auth

| Méthode | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Inscription email |
| POST | `/api/v1/auth/login` | Connexion email |
| POST | `/api/v1/auth/refresh` | Renouveler le token |
| POST | `/api/v1/auth/logout` | Déconnexion (révoquer refresh) |
| GET | `/api/v1/auth/verify-email` | Vérifier l'email |
| POST | `/api/v1/auth/forgot-password` | Demander un reset |
| POST | `/api/v1/auth/reset-password` | Réinitialiser le MDP |
| POST | `/api/v1/auth/oauth/google` | Callback Google |
| POST | `/api/v1/auth/oauth/github` | Callback GitHub |

### Users

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/users/me` | Profil utilisateur |
| PUT | `/api/v1/users/me` | Modifier le profil |
| PUT | `/api/v1/users/me/password` | Changer le MDP |
| DELETE | `/api/v1/users/me` | Supprimer le compte |

### Scans

| Méthode | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/scans` | Lancer un nouveau scan |
| GET | `/api/v1/scans` | Historique des scans |
| GET | `/api/v1/scans/{id}` | Détails d'un scan |
| GET | `/api/v1/scans/{id}/results` | Résultats par module |
| DELETE | `/api/v1/scans/{id}` | Supprimer un scan |
| WS | `/ws/scan/{id}` | WebSocket live |

### Reports

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/reports/{scan_id}` | Rapport IA d'un scan |
| GET | `/api/v1/reports/{scan_id}/pdf` | Télécharger le PDF |
| POST | `/api/v1/reports/{scan_id}/email` | (R)envoyer par email |

---

## 17. Pages & Routes Frontend

| Route | Page | Description |
|---|---|---|
| `/` | Landing Page | Présentation de synapsbranch, CTA |
| `/login` | Connexion | Email/MDP + Google + GitHub |
| `/register` | Inscription | Formulaire + OAuth |
| `/verify-email` | Vérification | Confirmation de l'email |
| `/forgot-password` | MDP oublié | Formulaire de demande |
| `/reset-password` | Reset MDP | Nouveau mot de passe |
| `/dashboard` | Dashboard | Vue d'ensemble, derniers scans |
| `/new-scan` | Nouveau Scan | Formulaire URL + lancement |
| `/scan/[id]` | Scan Live | Dashboard temps réel |
| `/scan/[id]/report` | Rapport | Rapport IA complet |
| `/history` | Historique | Liste de tous les scans |
| `/settings` | Paramètres | Profil, MDP, préférences |

---

## 18. Pipeline d'Exécution d'un Scan

```
POST /api/v1/scans { "url": "https://example.com" }
│
├─► Validation de l'URL (format, accessible, pas d'IP privée)
├─► Création du scan en BDD (status: "pending")
├─► Envoi de la tâche Celery
├─► Retourne scan_id au frontend
│
│   Le frontend ouvre WebSocket: ws://api/ws/scan/{scan_id}
│
└─► CELERY WORKER démarre :
    │
    ├─► PHASE 1: DNS & Connectivité
    │   ├─ Résolution DNS (A, AAAA, MX, NS, TXT, SOA)
    │   ├─ DNSSEC validation
    │   ├─ Ping + latence
    │   ├─ Port scan (80, 443)
    │   ├─ HTTP → HTTPS redirect check
    │   ├─ → WebSocket: logs + résultat
    │   └─ → Sauvegarde scan_results
    │
    ├─► PHASE 2: SSL / TLS
    │   ├─ Certificate info (validité, chaîne)
    │   ├─ Protocoles (TLS 1.0/1.1/1.2/1.3)
    │   ├─ Cipher suites
    │   ├─ Vulnérabilités (Heartbleed, POODLE…)
    │   ├─ HSTS check
    │   ├─ → WebSocket: logs + résultat
    │   └─ → Sauvegarde scan_results
    │
    ├─► PHASE 3: Performance / Load Testing
    │   ├─ Palier 1: 1 user (30s)
    │   │   └─ → WebSocket: métriques live toutes les 2s
    │   ├─ Palier 2: 50 users (60s)
    │   │   └─ → WebSocket: métriques live
    │   ├─ Palier 3: 100 users (60s)
    │   │   └─ → WebSocket: métriques live
    │   ├─ Palier 4: 500 users (90s)
    │   │   └─ → WebSocket: métriques live
    │   ├─ Palier 5: 1000 users (120s)
    │   │   └─ → WebSocket: métriques live
    │   ├─ → WebSocket: résultat final performance
    │   └─ → Sauvegarde scan_results
    │
    ├─► PHASE 4: Sécurité DAST
    │   ├─ Security headers check
    │   ├─ Cookie security check
    │   ├─ CORS check
    │   ├─ Information disclosure
    │   ├─ XSS basique
    │   ├─ Mixed content
    │   ├─ → WebSocket: logs + vulnérabilités trouvées
    │   └─ → Sauvegarde scan_results
    │
    ├─► PHASE 5: SEO & Indexation
    │   ├─ Meta tags analysis
    │   ├─ HTML structure (H1, alt, etc.)
    │   ├─ robots.txt + sitemap.xml
    │   ├─ Core Web Vitals (Lighthouse)
    │   ├─ Structured data
    │   ├─ → WebSocket: logs + résultat
    │   └─ → Sauvegarde scan_results
    │
    ├─► PHASE 6: Génération du Rapport IA
    │   ├─ Collecte de tous les résultats
    │   ├─ Appel API Claude/OpenAI
    │   ├─ Génération des graphiques
    │   ├─ Assemblage du PDF
    │   ├─ → WebSocket: "report_ready"
    │   └─ → Sauvegarde report
    │
    └─► PHASE 7: Envoi Email
        ├─ Rendu du template email
        ├─ Envoi via Resend (HTML + PDF attaché)
        └─ → Mise à jour report.email_sent = true
```

---

## 19. Planning & Phases de Développement

### Phase 1 — Fondations (Semaines 1-2)

- [ ] Setup du monorepo (frontend + backend)
- [ ] Docker Compose (PostgreSQL, Redis, Frontend, Backend)
- [ ] Configuration Next.js + Tailwind + shadcn/ui
- [ ] Configuration FastAPI + SQLAlchemy + Alembic
- [ ] Modèles de données et migrations
- [ ] Système d'authentification complet (email + OAuth)
- [ ] Envoi d'emails avec Resend (vérification + reset)
- [ ] Middleware JWT + protection des routes

### Phase 2 — Scanners Backend (Semaines 3-4)

- [ ] Classe abstraite `BaseScanner`
- [ ] DNS & Connectivité Scanner
- [ ] SSL/TLS Scanner (sslyze)
- [ ] Performance Scanner (Locust)
- [ ] Security Scanner (DAST basique)
- [ ] SEO Scanner
- [ ] Orchestrateur de scan (`scan_orchestrator.py`)
- [ ] Celery worker + tâches async
- [ ] WebSocket server pour le live

### Phase 3 — Interface Frontend (Semaines 5-6)

- [ ] Landing page
- [ ] Pages d'authentification (login, register, verify, reset)
- [ ] Layout dashboard (sidebar, header)
- [ ] Page "Nouveau Scan" (formulaire URL)
- [ ] Page "Scan Live" avec WebSocket
- [ ] Composants de résultats par module
- [ ] Graphiques (Recharts) — response time, throughput, radar
- [ ] Terminal live (logs en temps réel)
- [ ] Page historique des scans

### Phase 4 — Rapport IA & Email (Semaines 7-8)

- [ ] Intégration API IA (Claude/OpenAI)
- [ ] Prompt engineering pour le rapport
- [ ] Génération de graphiques (Matplotlib)
- [ ] Génération PDF (WeasyPrint + Jinja2)
- [ ] Template email rapport (react-email)
- [ ] Envoi du rapport par email avec PDF
- [ ] Page de visualisation du rapport

### Phase 5 — Polish & Déploiement (Semaine 9-10)

- [ ] Tests unitaires et d'intégration
- [ ] Gestion d'erreurs complète
- [ ] Rate limiting et sécurité
- [ ] Optimisation des performances
- [ ] Docker production build
- [ ] Configuration Nginx
- [ ] Documentation API (OpenAPI/Swagger)
- [ ] README et guide de déploiement

---

## 20. Variables d'Environnement

```env
# ──── Database ────
DATABASE_URL=postgresql://user:password@db:5432/synapsbranch

# ──── Redis ────
REDIS_URL=redis://redis:6379/0

# ──── JWT ────
JWT_SECRET=your-super-secret-key-change-in-production
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
EMAIL_FROM=synapsbranch <reports@synapsbranch.app>

# ──── AI ────
AI_PROVIDER=claude    # ou "openai"
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx

# ──── Frontend ────
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000

# ──── App ────
APP_NAME=synapsbranch
APP_ENV=development     # development | production
CORS_ORIGINS=http://localhost:3000
```

---

> **Ce plan couvre l'ensemble de l'architecture, des modules, de la base de données, des API, du frontend, du déploiement Docker et du planning de développement. Chaque module est détaillé avec ses spécifications techniques, ses métriques collectées et son implémentation recommandée.**