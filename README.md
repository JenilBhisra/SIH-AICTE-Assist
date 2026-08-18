# AICTE Model Curriculum Intelligence & Governance Portal

A unified portal for developing, submitting, and governing model curricula for
AICTE-approved institutes — connecting AICTE rules/regulations/circulars,
curriculum designers, reviewers/experts, and AI-assisted analysis into one
coherent workflow instead of disconnected documents and emails.

## What this project does

```
AICTE official knowledge → Curriculum creation → AI assistance →
Curriculum submission → AI analysis → AI screening →
Human reviewer decision → Changes / approval / rejection
```

MVP has exactly three user roles:

1. **AICTE Admin** — manages AICTE documents (the future RAG knowledge base),
   institutes, users/roles.
2. **Curriculum Designer** — builds structured curricula (Curriculum → Semester
   → Course → Module → Topic) and uses one AI chatbot with three modes
   (AICTE/Curriculum Assistant, Resource Assistant, Anonymous Comparison
   Assistant).
3. **Reviewer / Expert** — reviews submitted curricula, runs the Curriculum
   Analyzer and AI Curriculum Screener for decision support, and makes the
   final approve/reject/request-changes call. **AI never decides; a human
   always does.**

Full problem statement, architecture, and scope are in
[docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md).

## Repository structure

```
SIH-AICTE-Assist/
├── frontend/        React + TypeScript + Vite (Person 3)
├── backend/          FastAPI + SQLAlchemy + Alembic (Person 1 core, Person 2 AI)
├── docs/             Shared source of truth for all 3 developers + LLMs
├── README.md
├── CONTRIBUTING.md
└── .gitignore
```

## Tech stack

- **Frontend:** React, TypeScript, Vite, React Router, Tailwind CSS,
  shadcn/ui, TanStack Query, React Hook Form, Zod
- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy, Alembic
- **Database:** PostgreSQL hosted on Neon (shared, single project)
- **Vector storage:** pgvector inside the same Neon Postgres instance
- **AI:** external LLM API, sentence-transformers, LangChain where useful
- **PDF processing:** PyMuPDF
- **File storage (MVP):** local filesystem

No Docker, Redis, Celery, Kafka, Kubernetes, microservices, OpenSearch,
Elasticsearch, or MinIO in MVP.

## Team ownership

| Person | Owns |
|---|---|
| Person 1 | Backend foundation, database, auth/RBAC, curricula/review business logic, API contracts |
| Person 2 | AI/RAG: PDF extraction, embeddings, pgvector retrieval, AICTE/Resource/Comparison assistants, Analyzer, Screener |
| Person 3 | Frontend: React app, all dashboards/UI, chatbot UI, API integration via TanStack Query |

See [docs/TEAM_STATUS.md](docs/TEAM_STATUS.md) for live status and
[CONTRIBUTING.md](CONTRIBUTING.md) for collaboration rules.

## Getting started

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your own DATABASE_URL, never commit .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Both are skeletons at this stage — no auth, curriculum, or AI features exist
yet. See [docs/TEAM_STATUS.md](docs/TEAM_STATUS.md) for what's next.

## Required reading before you (human or LLM) touch this codebase

1. [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) — problem, solution, scope, architecture
2. [docs/TEAM_STATUS.md](docs/TEAM_STATUS.md) — who is doing what right now
3. [docs/API_CONTRACTS.md](docs/API_CONTRACTS.md) — if you touch any API
4. [docs/DATABASE_NOTES.md](docs/DATABASE_NOTES.md) — if you touch the schema
5. [docs/AI_NOTES.md](docs/AI_NOTES.md) — if you touch AI/RAG behavior

After meaningful work, update the relevant doc(s) above and commit them
together with the code change. See [CONTRIBUTING.md](CONTRIBUTING.md).
