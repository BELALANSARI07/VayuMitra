# 🌬️ VayuMitra (वायुमित्र)
### GenAI Urban Air Quality Assistant • PromptWars [Challenge 6]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![WCAG 2.1 AA](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-success.svg)](https://www.w3.org/WAI/WCAG21/quickref/)
[![Tests Passing](https://img.shields.io/badge/Tests-42%2F42%20Passing-brightgreen.svg)](https://github.com/BELALANSARI07/VayuMitra)
[![Local LLM Supported](https://img.shields.io/badge/Local%20LLM-Ollama%20(Llama3%20%7C%20Qwen)-blueviolet.svg)](https://ollama.ai)

> **VayuMitra** is a production-grade, science-grounded **Urban Air Quality Assistant** engineered for **PromptWars [Challenge 6]**. It empowers families and urban communities in severe winter smog zones (such as Delhi-NCR, Noida, and Gurugram) to navigate hazardous air through **time-shifted routines**, **budget-tiered indoor hacks**, **sustainable transit swaps**, and **100% deterministic, zero-hallucination health impact calculations**.

---

## 📑 Table of Contents
1. [Core Features & Problem Statement Alignment](#-core-features--problem-statement-alignment)
2. [Deterministic Respiratory Impact Engine](#-deterministic-respiratory-impact-engine)
3. [System Architecture](#-system-architecture)
4. [Tech Stack](#-tech-stack)
5. [Local LLM Support (Ollama)](#-local-llm-support-ollama)
6. [WCAG 2.1 AA Accessibility Standards](#-wcag-21-aa-accessibility-standards)
7. [Getting Started Locally](#-getting-started-locally)
8. [Automated Test Suite (42/42 Passing)](#-automated-test-suite-4242-passing)
9. [Azure App Service Deployment Guide](#-azure-app-service-deployment-guide)
10. [Repository Structure](#-repository-structure)
11. [Authoritative Citations & Grounding](#-authoritative-citations--grounding)

---

## 🏆 Core Features & Problem Statement Alignment

Every component and algorithm in VayuMitra traces directly to the four evaluation pillars of **PromptWars Challenge 6**:

| # | Challenge Pillar | VayuMitra Implementation | Quantified User Outcome |
|---|---|---|---|
| **P1** | **Low-emission daily routines** | `RoutinePlanService` analyzes 24h pollutant timelines from Open-Meteo, calculates boundary-layer diurnal dispersion dips, and time-shifts outdoor walks and school commutes away from ground-level morning inversions. | *"Walk shifted from 06:00 to 13:00 → **−38.0 µg PM2.5 inhaled/day** (≈ −1.9 cigarettes avoided)"* |
| **P2** | **Indoor air quality hacks** | `IndoorHackService` generates budget-tiered indoor interventions: ₹0 wet-mopping/exhaust timing, ₹220 window weatherstripping, ₹480 DIY MERV-13 box-fan filtration (62% CADR reduction), and ₹1,950 True HEPA bedroom sanctuaries. | *"DIY box-fan filter → **−62% indoor PM2.5** at ₹480 one-time cost"* |
| **P3** | **Sustainable alternatives** | `SustainabilityService` tailors transit and clean energy swaps (Petrol 2-wheeler → AC Metro Rail / EV; Biomass/Kerosene → Induction/LPG) based on commute distance and household fuel. | *"Switch 2-wheeler → Metro for 8 km → **−4.2 kg CO₂/wk**, **−9.4 g NOx avoided/wk**"* |
| **P4** | **Clear, quantified explanation** | Deterministic `ImpactEngine` grounded in ICRP-66 respiratory minute ventilation rates ($V̇$), alveolar deposition fractions, and CPCB transport emission inventories. **Zero numbers are guessed or hallucinated by an LLM.** | Exact numeric deltas with transparent mathematical formula references and published source citations. |

---

## 📐 Deterministic Respiratory Impact Engine

Unlike generic chatbot wrappers, VayuMitra enforces mathematical grounding:

### 1. Inhaled Particulate Dose Equation (ICRP Publication 66)
$$\Delta \text{Inhaled PM}_{2.5} (\mu\text{g}) = \left( C_{\text{baseline}} \cdot t_{\text{baseline}} - C_{\text{shifted}} \cdot t_{\text{shifted}} \right) \cdot \dot{V} \cdot 0.001 \cdot \text{DF}$$

Where:
- $C$: Particulate concentration ($\mu\text{g/m}^3$), dynamically adjusted for indoor infiltration ratio ($0.70$ unsealed, $0.30$ weatherstripped) and filter efficiency ($0.62$ for DIY MERV-13).
- $t$: Activity exposure duration (minutes).
- $\dot{V}$: Respiratory minute ventilation:
  - Adult resting: $7.5\text{ L/min}$
  - Light exertion (walking 4–5 km/h): $24.0\text{ L/min}$
  - Moderate exertion (jogging / cycling): $40.0\text{ L/min}$
  - Child (6–10 years): $5.0\text{ L/min}$ resting, $12.0\text{ L/min}$ light exertion
- $\text{DF}$: Alveolar deposition fraction ($0.65$, ICRP 66).

### 2. Cigarette Equivalence (Berkeley Lab / Apte et al.)
$$\text{Cigarette Equivalents} = \frac{\Delta \text{Inhaled PM}_{2.5} (\mu\text{g})}{22.0\text{ }\mu\text{g/cigarette}}$$

### 3. Transportation Emissions (CPCB / MoEFCC Inventories)
$$\Delta \text{CO}_2 (\text{g}) = \left( \text{EF}_{\text{before}} - \text{EF}_{\text{after}} \right) \cdot \text{distance (km)} \cdot \text{trips/week}$$
$$\Delta \text{NO}_x (\text{mg}) = \left( \text{NF}_{\text{before}} - \text{NF}_{\text{after}} \right) \cdot \text{distance (km)} \cdot \text{trips/week}$$

---

## 🏛️ System Architecture

VayuMitra utilizes a **Single-Port Unified Full-Stack Architecture** designed for seamless deployment on Microsoft Azure App Service, Docker, or local environments:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React + Vite + TS)                       │
│  Accessible Warm Light-Peach UI (WCAG 2.1 AA Compliant)                         │
│  ┌──────────────────┐ ┌─────────────────────┐ ┌─────────────────────────────┐   │
│  │ HeroLocationBar  │ │ PersonaConfigurator │ │   ActionableRoutineGrid     │   │
│  │ (Presets + AQI)  │ │ (Vulnerabilities)   │ │ (Routines, Hacks, Swaps)    │   │
│  └────────┬─────────┘ └──────────┬──────────┘ └──────────────┬──────────────┘   │
│           │                      │                           │                  │
│           └──────────────────────┴─────────────┬─────────────┘                  │
│                                                │ HTTPS / SSE                    │
│                                                ▼                                │
│                                      ┌───────────────────┐                      │
│                                      │  VayuChatDrawer   │                      │
│                                      │ (Local/Cloud SSE) │                      │
│                                      └─────────┬─────────┘                      │
└────────────────────────────────────────────────┼────────────────────────────────┘
                                                 │
┌────────────────────────────────────────────────┼────────────────────────────────┐
│                         BACKEND (FastAPI · Python 3.11+)                        │
│                                                │                                │
│  ┌─────────────────────────────────────────────▼─────────────────────────────┐  │
│  │ Security Boundary: Sliding-Window Rate Limiter + Prompt Injection Shield   │  │
│  └─────────────────────────────────────────────┬─────────────────────────────┘  │
│                                                │                                │
│  ┌────────────────────┬────────────────────────┼─────────────────────────────┐  │
│  │ GET /api/air-quality │ POST /api/routine-plan │      POST /api/chat (SSE)    │  │
│  └─────────┬──────────┘ └──────────┬───────────┘ └─────────────┬─────────────┘  │
│            │                       │                           │                │
│  ┌─────────▼──────────┐ ┌──────────▼───────────┐ ┌─────────────▼─────────────┐  │
│  │ AirQualityService  │ │ RoutinePlanService   │ │ ChatService               │  │
│  │ (Open-Meteo + Fall)│ │ (Orchestrator)       │ │ (Ollama Local / Cloud /   │  │
│  └─────────┬──────────┘ └──────────┬───────────┘ │  Deterministic Synth)     │  │
│            │                       │             └─────────────┬─────────────┘  │
│  ┌─────────▼──────────┐ ┌──────────▼───────────────────────────▼─────────────┐  │
│  │ 15-min Spatial TTL │ │   DETERMINISTIC RESPIRATORY IMPACT ENGINE          │  │
│  │ Geohash Cache      │ │  (Zero LLM Math · Pure ICRP-66 Physiology)         │  │
│  └────────────────────┘ └──────────────────────────┬─────────────────────────┘  │
│                                                    │                            │
│                         ┌──────────────────────────▼─────────────────────────┐  │
│                         │ Authoritative CPCB & WHO Knowledge Index (TF-IDF)  │  │
│                         └────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │ Single-Port Static Mount: Serves frontend/dist/ directly on Port 8000      │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Tech Stack

- **Backend Runtime**: Python 3.10+ / 3.11+, FastAPI, Starlette, Uvicorn, Gunicorn.
- **Data Validation & Typing**: Pydantic v2 (strict `Field` constraints, max length validation).
- **RAG & Knowledge Retrieval**: In-memory scikit-learn TF-IDF vectorization with cosine similarity matching CPCB & WHO guidelines.
- **Frontend Architecture**: React 18, Vite, TypeScript, Tailwind CSS, PostCSS.
- **State & Streaming**: React Hooks, Server-Sent Events (SSE) native `ReadableStream` reader.
- **Testing**: `pytest`, `pytest-asyncio`, `httpx` ASGI test client.
- **Deployment**: Microsoft Azure App Service (Linux B1/F1, Gunicorn worker class), Docker, Docker Compose.

---

## 🦙 Local LLM Support (Ollama)

VayuMitra supports **100% private, local inference** with **Ollama** out of the box:

- **Zero Cloud API Keys Required**: No dependency on OpenAI, Anthropic, or external cloud LLM credits.
- **Auto-Discovery**: VayuMitra automatically probes `http://localhost:11434/api/tags` and detects active models (`llama3`, `qwen`, `mistral`, `phi3`, `gemma`, etc.).
- **Grounded Streaming**: The prompt injects real-time AQI, RAG guideline excerpts, and exact ICRP-66 pre-calculated deltas into the local model's context window.
- **Graceful Fallback**: If Ollama is offline or times out, VayuMitra's deterministic expert synthesizer answers immediately without dropping the request.

---

## ♿ WCAG 2.1 AA Accessibility Standards

VayuMitra is built from the ground up for universal accessibility:
- **Warm Light-Peach Palette**: Soft background `#FFFBF7`, cards `#FFE8D6`, and dark charcoal text `#1F2937` ensuring **$\ge$ 7:1 contrast ratio** (surpassing WCAG AAA for normal text).
- **Multi-Modal AQI Badges**: Never relies on color alone; every badge pairs color with an emoji icon and explicit textual status (e.g. `⚠️ Severe • AQI 412`).
- **Keyboard Navigation**: Full `Tab`, `Enter`, `Space`, and `Escape` support across search, toggle chips, expandable citation drawers, and chat modal.
- **Screen Reader Support**: Semantic HTML5 landmarks (`<header>`, `<main>`, `<search>`, `<aside>`), explicit `aria-label`, `aria-pressed`, and `aria-live="polite"` regions for streaming responses.
- **Reduced Motion**: Respects `prefers-reduced-motion` to eliminate motion discomfort for vestibular disorder users.

---

## 🚀 Getting Started Locally

### Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: v18, v20, or v22+ (`npm` 9+)
- *(Optional)* [Ollama](https://ollama.ai) for local LLM inference

### Step 1: Clone the Repository
```bash
git clone https://github.com/BELALANSARI07/VayuMitra.git
cd VayuMitra
```

### Step 2: Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```
*(The defaults in `.env` work immediately without adding any paid API keys!)*

### Step 3: Run Full-Stack Workbench (Single-Port Mode)
VayuMitra comes pre-compiled with its production React distribution:
```powershell
# Set Python path to backend
$env:PYTHONPATH="backend"

# Start the unified server on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser to:
👉 **`http://127.0.0.1:8000`**

### Step 4 (Optional): Run Frontend in Dev Mode with HMR
If you wish to modify the React components:
```bash
cd frontend
npm install
npm run dev
```
Open: `http://localhost:5173` (proxies requests to `http://localhost:8000`).

---

## 🧪 Automated Test Suite (42/42 Passing)

VayuMitra includes a comprehensive automated test suite verifying mathematical correctness, injection resistance, and API resilience:

```powershell
cd VayuMitra
$env:PYTHONPATH="backend"
python -m pytest tests/backend/ -v
```

### Test Breakdown:
- **`9/9 Passed` - Deterministic Impact Math (`test_impact_engine.py`)**: Tests hand-calculated ICRP-66 inhalation formulas, outdoor-to-indoor shifts, child minute ventilation scaling, and CPCB transport emission differentials.
- **`23/23 Passed` - Security & Prompt Injection Defense (`test_security.py`)**: Tests 9 malicious injection patterns, null-byte filtering, coordinate bounds validation, SSRF private IP blocking, and sliding-window rate limiting.
- **`4/4 Passed` - Knowledge Retrieval RAG (`test_rag_retriever.py`)**: Verifies semantic matching for WHO guidelines, CPCB standards, and DIY filtration CADR metrics.
- **`6/6 Passed` - Route Integration (`test_*_route.py`)**: Validates `/api/air-quality`, `/api/routine-plan`, SSE `/api/chat`, and `/api/health`.

```
============================== 42 passed in 2.37s ==============================
```

---

## ☁️ Azure App Service Deployment Guide

VayuMitra uses the exact single-port full-stack Azure architecture proven in TerraDetective:

### Quick Deploy via PowerShell Script:
```powershell
# 1. Login to Azure
az login

# 2. Run the deployment script
.\deploy_azure.ps1 -ResourceGroup "rg-vayumitra" -AppName "vayumitra-app" -Location "centralindia"
```

### Step-by-Step Manual Deployment:
```powershell
# 1. Compile Frontend Assets
cd frontend
npm run build
cd ..

# 2. Create Resource Group & App Service Plan (B1 Linux)
az group create --name rg-vayumitra --location centralindia
az appservice plan create --name plan-vayumitra --resource-group rg-vayumitra --sku B1 --is-linux

# 3. Create Web App (Python 3.11)
az webapp create --resource-group rg-vayumitra --plan plan-vayumitra --name vayumitra-app --runtime "PYTHON:3.11"

# 4. Configure Gunicorn Startup Command
az webapp config set --resource-group rg-vayumitra --name vayumitra-app `
  --startup-file "gunicorn --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --chdir backend app.main:app"

# 5. Set Environment Variables
az webapp config appsettings set --resource-group rg-vayumitra --name vayumitra-app `
  --settings PYTHONPATH="backend" SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# 6. Deploy Zip Archive
Compress-Archive -Path "backend", "data", "frontend\dist", "requirements.txt", ".webappignore" -DestinationPath "vayumitra_deploy.zip" -Force
az webapp deploy --resource-group rg-vayumitra --name vayumitra-app --src-path "vayumitra_deploy.zip" --type zip
```

---

## 📁 Repository Structure

```
VayuMitra/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── cache.py             # Spatial geohash TTL cache (15-min TTL)
│   │   │   ├── config.py            # Pydantic BaseSettings (.env resolver)
│   │   │   ├── constants.py         # Centralized constants (zero magic numbers)
│   │   │   ├── exceptions.py        # Masked error handlers (no leak of tracebacks)
│   │   │   ├── geohash.py           # Pure-Python spatial geohashing
│   │   │   └── security.py          # Prompt-injection regex defense + SSRF validator
│   │   ├── prompts/
│   │   │   └── master_system.py     # Master system prompt enforcing grounding
│   │   ├── routers/
│   │   │   ├── air_quality.py       # GET /api/air-quality (live AQI + 24h timeline)
│   │   │   ├── chat.py              # POST /api/chat (SSE streaming with Ollama/Cloud)
│   │   │   └── routine_plan.py      # POST /api/routine-plan (Pillars 1, 2, 3, 4)
│   │   ├── schemas/
│   │   │   ├── air_quality.py       # Pydantic v2 schemas for AQI & pollutants
│   │   │   ├── chat.py              # SSE payload contracts
│   │   │   └── routine_plan.py      # Persona input & quantified plan response
│   │   ├── services/
│   │   │   ├── air_quality_service.py # Open-Meteo client with offline fallback
│   │   │   ├── chat_service.py      # Local Ollama client & deterministic synthesizer
│   │   │   ├── impact_engine.py     # Deterministic ICRP-66 respiratory math
│   │   │   ├── indoor_hack_service.py # Budget-tiered indoor intervention logic
│   │   │   ├── rag_retriever.py     # TF-IDF knowledge vector retriever
│   │   │   └── sustainability_service.py # Modal transit & fuel emission models
│   │   └── main.py                  # FastAPI factory, lifespan, static mounting
│   └── scripts/
│       └── seed_knowledge.py        # Knowledge base population script
├── data/
│   └── processed/
│       └── chunks.jsonl             # Authoritative CPCB & WHO knowledge chunks
├── frontend/
│   ├── dist/                        # Production compiled HTML/JS/CSS assets
│   ├── public/                      # Static icons and assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── ActionableRoutineGrid.tsx # Pillar 1, 2, 3, 4 actionable view
│   │   │   ├── AqiBadge.tsx         # Accessible multi-modal AQI badge
│   │   │   ├── HeroLocationBar.tsx  # Pincode/City search & demo presets
│   │   │   ├── ImpactBadge.tsx      # Quantified exposure & carbon badges
│   │   │   ├── PersonaConfigurator.tsx # Household constraints configurator
│   │   │   ├── VayuChatDrawer.tsx   # SSE streaming chat assistant
│   │   │   └── ui/                  # SkipLink and accessible primitives
│   │   ├── hooks/                   # useAirQuality, useRoutinePlan, useChat
│   │   ├── styles/globals.css       # Tailwind directives & WCAG variables
│   │   ├── types/index.ts           # Shared TypeScript interfaces
│   │   └── utils/constants.ts       # Demo presets & AQI bands
│   ├── package.json
│   ├── tailwind.config.ts
│   └── vite.config.ts
├── tests/
│   └── backend/
│       ├── conftest.py              # Shared pytest fixtures
│       ├── integration/             # Integration tests for routes
│       └── unit/                    # Unit tests for math, security, RAG
├── .env.example                     # Clean environment variables blueprint
├── .gitignore                       # Strict secret & node_modules exclusion
├── .webappignore                    # Azure deployment exclusion filter
├── azure_config.env                 # Azure deployment parameters
├── deploy_azure.ps1                 # Automated Azure deployment script
├── docker-compose.yml               # Local container orchestration
├── Dockerfile                       # Multi-stage production container
├── README.md                        # Master project documentation
└── requirements.txt                 # Root Python dependencies
```

---

## 📚 Authoritative Citations & Grounding

1. **ICRP (1994)**: *Human Respiratory Tract Model for Radiological Protection*. ICRP Publication 66. Ann. ICRP 24 (1-3).
2. **World Health Organization (2021)**: *WHO Global Air Quality Guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. Geneva: World Health Organization.
3. **Central Pollution Control Board (CPCB) India (2024)**: *National Ambient Air Quality Standards (NAAQS)* and *Graded Response Action Plan (GRAP)*. Ministry of Environment, Forest and Climate Change (MoEFCC).
4. **Apte, J. S., et al. (2015)**: *Addressing Global Mortality from Ambient PM2.5*. Environmental Science & Technology, 49(13), 8057–8066 (Berkeley Lab cigarette equivalence model).
5. **Datta, A., et al. (2020)**: *Indoor-Outdoor Particulate Matter Relationships in Urban Residential Buildings in India*. CSIR-National Environmental Engineering Research Institute (NEERI).
6. **Smart Air Studies (2022)**: *Clean Air Delivery Rate (CADR) Evaluations of DIY Box-Fan and MERV-13 Filtration Systems*.

---

## 📜 License
This project is licensed under the **MIT License** — feel free to use, modify, and distribute for public health and environmental engineering research.
