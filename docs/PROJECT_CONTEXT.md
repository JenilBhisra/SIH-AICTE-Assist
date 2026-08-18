# Project Context

> **For every LLM/developer:** read this file first, before writing or
> changing any code. Also read [TEAM_STATUS.md](TEAM_STATUS.md), and
> [API_CONTRACTS.md](API_CONTRACTS.md) / [DATABASE_NOTES.md](DATABASE_NOTES.md)
> / [AI_NOTES.md](AI_NOTES.md) if the work touches those areas. After doing
> meaningful work, update the relevant doc(s) so other developers and LLMs
> understand the latest repository state.
>
> This file describes project-level scope and architecture. Do not rewrite it
> casually — only when an actual project-level decision changes. Day-to-day
> status belongs in `TEAM_STATUS.md`.

## 1. Original problem

AICTE needs a unified portal for developing model curricula for
AICTE-approved institutes, supporting user authentication, role-based
dashboards, curriculum design, educational resource management,
collaboration/review, analytics/reporting, notifications/updates, and
scalability/security.

The deeper problem: curriculum creation and governance involve many
disconnected things — AICTE rules, regulations, policies, circulars, model
curriculum documents, curriculum designers, reviewers/experts, approved
institutes, course structures, learning outcomes, assessments, resources,
and review decisions — with no single intelligent system connecting them.

## 2. Our solution

Not a curriculum CRUD website. A portal that supports this flow:

```
AICTE official knowledge
  → Curriculum creation
  → AI assistance
  → Curriculum submission
  → AI analysis
  → AI screening
  → Human reviewer decision
  → Changes / approval / rejection
```

## 3. MVP scope — exactly 3 users

### User 1 — AICTE Admin (authoritative administrative user)
- Login securely; admin dashboard.
- Manage AICTE documents: upload PDFs, manage rules/regulations/policies/
  guidelines/circulars and their metadata. These documents become the RAG
  knowledge base for the AI system.
- Manage AICTE-approved institutes.
- View/manage users and roles.
- View basic curriculum/review counts.
- Admin data is the authoritative source of truth.

### User 2 — Curriculum Designer
- Login; dashboard.
- Create/edit curriculum, save draft.
- Build structured hierarchy: **Curriculum → Semester → Course → Module →
  Topic**. Curriculum is structured data, not one uploaded PDF.
- Course also contains: objectives, learning outcomes, credits,
  prerequisites, assessments, resources.
- Submit curriculum for review; receive reviewer-requested changes; revise
  and resubmit.

### User 3 — Reviewer / Expert
- Login; reviewer dashboard.
- View submitted curricula; inspect complete curriculum; view relevant
  AICTE policies/documents.
- Add comments, request changes, approve, or reject.
- Run Curriculum Analyzer and AI Curriculum Screener as decision support.
- **AI never makes the final approve/reject decision — that authority
  belongs solely to the human Reviewer.**

## 4. Designer AI features — one chatbot, three modes

Person 2 builds **one** chatbot interface with three modes, all sharing one
RAG foundation (no three disconnected chatbot systems):

1. **AICTE / Curriculum Assistant** — answers designer questions about
   curriculum creation and AICTE requirements (credit structure, learning
   outcomes, prerequisites, applicable AICTE rules, assessment methods,
   course improvement). Uses RAG over AICTE documents + curriculum context;
   shows source document/page where possible; never invents AICTE rules.
2. **AI Resource Assistant** — recommends educational resources (textbooks,
   papers, articles, videos, lecture/practical/lab material, references) for
   a selected curriculum/course/module/topic. Each recommendation explains
   resource, type, relevant topic/module, and why it's useful. No live
   internet crawling in MVP.
3. **Anonymous Curriculum Comparison Assistant** — compares the designer's
   curriculum against strong approved benchmark curricula **without ever
   exposing** institute name/ID/address or curriculum owner identity. Shows
   only "Anonymous Benchmark" / aggregated comparison, e.g. per-topic
   Strong/Partial/Missing/Good, followed by problem → evidence →
   recommended improvement → suggested addition. Goal is to improve the
   curriculum, not copy another institute's.

Full design details belong in [AI_NOTES.md](AI_NOTES.md), kept current by
Person 2.

## 5. Curriculum Analyzer (Reviewer-side)

Conceptually like a resume analyzer, but for curricula. Input: a submitted
curriculum. Output: overall score, category scores (e.g. AICTE compliance,
curriculum structure, course coverage, learning outcomes, assessment
alignment, practical exposure, resource coverage, industry relevance, skill
coverage), and for every issue found:

```
PROBLEM → EVIDENCE → WHY IT MATTERS → SOLUTION → SUGGESTED REVISION
```

Must provide actionable solutions, not only criticism.

## 6. AI Curriculum Screener (Reviewer-side)

Conceptually like a resume screener for companies — decision support, not a
decision-maker. Analyzes AICTE compliance, structure, credits, course/topic
coverage, learning outcomes, assessments, practical component, resources,
prerequisites, completeness. Produces a screening score, category
sub-scores, and issues tagged HIGH/MEDIUM/LOW, plus one AI recommendation
label: `LIKELY_READY_FOR_REVIEW`, `CHANGES_RECOMMENDED`, or
`MAJOR_ISSUES_DETECTED`.

The Reviewer alone chooses: **APPROVE**, **REJECT**, or **REQUEST CHANGES**.

## 7. Curriculum workflow (status machine)

```
DRAFT → SUBMITTED → UNDER_REVIEW → CHANGES_REQUESTED → RESUBMITTED → APPROVED
UNDER_REVIEW → REJECTED
```

No arbitrary status changes — transitions are controlled by backend
service/business logic (Person 1), not left to routers or the frontend.

## 8. Shared AI architecture

One shared AI infrastructure, not five unrelated systems:

```
AICTE Documents + Curriculum Data + Resources + Anonymous Benchmark Data
  → Document Processing → Embeddings → pgvector → Retriever
  → Context Builder → LLM
  → { AICTE Assistant, Resource Assistant, Comparison Assistant,
      Curriculum Analyzer, Curriculum Screener }
```

Analyzer and Screener use structured Pydantic outputs, not unrestricted raw
LLM text.

## 9. Team ownership

| Person | Scope |
|---|---|
| **Person 1** — Core Backend + DB | FastAPI foundation, PostgreSQL, SQLAlchemy, Alembic, auth, JWT, RBAC, users, institutes, document metadata, policies, curricula/semesters/courses/modules/outcomes/assessments, review workflow, business logic, API contracts. **No AI logic.** |
| **Person 2** — AI / RAG | PDF extraction, chunking, embeddings, pgvector retrieval, RAG, LLM provider, AICTE Assistant, Resource Assistant, Anonymous Comparison, Curriculum Analyzer, Curriculum Screener, structured AI schemas, AI tests. Works inside the same FastAPI backend. |
| **Person 3** — Frontend + Integration | React, TypeScript, Vite, Tailwind, shadcn/ui, routing, login UI, dashboards (Admin/Designer/Reviewer), curriculum builder, chatbot UI, Analyzer UI, Screener UI, TanStack Query, forms, validation, API integration. Never touches the DB directly. |

## 10. Technology stack

**Frontend:** React, TypeScript, Vite, React Router, Tailwind CSS, shadcn/ui,
TanStack Query, React Hook Form, Zod.

**Backend:** Python, FastAPI, Pydantic, SQLAlchemy, Alembic.

**Database:** PostgreSQL hosted on Neon (one shared project).

**Vector storage:** pgvector inside the same Neon Postgres.

**AI:** external LLM API, sentence-transformers, LangChain where useful.

**PDF:** PyMuPDF.

**File storage (MVP):** local filesystem.

**Collaboration:** Git + GitHub.

**Explicitly excluded from MVP:** Docker, Redis, Celery, Kafka, Kubernetes,
microservices, OpenSearch, Elasticsearch, MinIO.

## 11. Shared database

One Neon PostgreSQL project for the whole team. Everyone connects via
`DATABASE_URL` from their own local `.env` (never committed — use
`.env.example` for variable names only). Schema changes only via SQLAlchemy
models + Alembic migrations; never hand-edit shared tables. Pull latest
branch before changing schema; commit the migration with the related model
change; everyone else runs `alembic upgrade head` after pulling.

Architecture: `React → FastAPI → SQLAlchemy → Neon PostgreSQL`. Frontend
never accesses Neon directly.

## 12. Repository layout

Monorepo, `SIH-AICTE-Assist`:

```
SIH-AICTE-Assist/
├── frontend/
├── backend/
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── TEAM_STATUS.md
│   ├── API_CONTRACTS.md
│   ├── DATABASE_NOTES.md
│   └── AI_NOTES.md
├── README.md
├── CONTRIBUTING.md
├── .gitignore
└── .env.example (frontend/ and backend/ each have their own)
```

## 13. Engineering flow rules

- Backend: `Router → Service → Repository → Database`. No business logic in
  routers.
- AI: `Router → AI Service → Domain Query Service → Retriever / LLM`. AI
  modules must not duplicate curriculum DB logic — they call into Person 1's
  services/repositories.
- Frontend: `Components → API Service / TanStack Query → FastAPI`.
- Stable API contracts; document any rename in `API_CONTRACTS.md`.
- Config via environment variables; no hardcoded secrets; migrations for all
  schema changes; avoid giant files and duplicated logic.

## 14. Current stage

**Foundation stage.** Only the monorepo scaffold, shared documentation, and
minimal backend/frontend skeletons exist. No auth, admin functionality,
curriculum functionality, AI/RAG, Analyzer, Screener, or dashboards have been
implemented yet — see [TEAM_STATUS.md](TEAM_STATUS.md) for what's next for
each person.
