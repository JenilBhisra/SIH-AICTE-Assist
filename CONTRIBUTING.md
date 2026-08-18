# Contributing Guide

This repository is worked on simultaneously by **3 developers**, and often
by **multiple LLM sessions** acting on their behalf. These rules exist so
independent sessions don't collide, duplicate work, or silently break each
other's modules. Read [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) and
[docs/TEAM_STATUS.md](docs/TEAM_STATUS.md) before starting anything.

## Ownership (do not cross these lines without discussion)

### Person 1 — Core Backend + Database
Owns: FastAPI foundation, PostgreSQL, SQLAlchemy models, Alembic migrations,
authentication, JWT, RBAC, users, institutes, document metadata, policies,
curricula/semesters/courses/modules/outcomes/assessments schema, review
workflow business logic, API contracts.
**Does not** implement AI logic.

### Person 2 — AI / RAG
Owns: PDF extraction, chunking, embeddings, pgvector retrieval, RAG pipeline,
LLM provider integration, AICTE Assistant, Resource Assistant, Anonymous
Comparison Assistant, Curriculum Analyzer, AI Curriculum Screener, structured
AI Pydantic schemas, AI tests.
Works **inside the same FastAPI backend** as Person 1 — not a separate service.
**Does not** duplicate curriculum database logic; calls into Person 1's
repositories/services for data.

### Person 3 — Frontend + Integration
Owns: React app, TypeScript, Vite, Tailwind, shadcn/ui, routing, login UI,
all dashboards (Admin/Designer/Reviewer), curriculum builder UI, chatbot UI,
Analyzer UI, Screener UI, TanStack Query, forms, frontend validation, API
integration.
**Never** accesses the database directly — only through the FastAPI backend,
and only through contracts defined in
[docs/API_CONTRACTS.md](docs/API_CONTRACTS.md).

Avoid unnecessary edits to another person's modules. If a change must cross
boundaries (e.g. Person 3 needs a new field in an API response), update
`docs/API_CONTRACTS.md` and coordinate — don't silently invent a response
shape or reach into someone else's model.

## Engineering rules

**Backend flow:** Router → Service → Repository → Database. No business logic
directly inside FastAPI routers.

**AI flow:** Router → AI Service → Domain Query Service → Retriever / LLM.
AI modules do not re-implement curriculum DB logic; they call Person 1's
services/repositories.

**Frontend flow:** Components → API Service / TanStack Query → FastAPI.
Never call Neon directly from the frontend.

General:
- Use environment variables for configuration; never hardcode secrets.
- All schema changes go through SQLAlchemy models + Alembic migrations —
  never hand-edit the shared Neon database.
- Keep API contracts stable; don't rename shared endpoints/schemas without
  updating `docs/API_CONTRACTS.md` first.
- Avoid giant files and duplicated logic. Don't over-engineer for
  hypothetical future requirements.

## Git workflow

Branches:
- `main` — stable, protected
- `develop` — integration branch
- `feature/*` — actual work, e.g. `feature/p1-backend-foundation`,
  `feature/p2-ai-foundation`, `feature/p3-frontend-foundation`

Never commit directly to `main`. Prefer not to commit directly to `develop`
either — use a feature branch and a PR.

Workflow:
1. Pull latest `develop` before starting work (especially before any schema
   change).
2. Create/switch to your `feature/*` branch.
3. Do the work.
4. Update the relevant docs (see below) in the **same commit/PR** as the code.
5. Commit, push your feature branch.
6. Open a PR into `develop`.
7. Merge after integration review.

## Database changes (all developers)

- Schema changes are made **only** through SQLAlchemy models + an Alembic
  migration. Never manually alter tables in the shared Neon project.
- Before changing schema: pull latest `develop`.
- After adding a migration: commit the migration together with the model
  change, and update [docs/DATABASE_NOTES.md](docs/DATABASE_NOTES.md).
- Everyone else then runs `alembic upgrade head` after pulling.
- Never commit real database credentials. Use `.env` locally (gitignored)
  and keep `.env.example` updated with variable **names** only.

## Documentation is part of the work, not optional cleanup

Before writing or modifying any code:
1. Read `docs/PROJECT_CONTEXT.md`.
2. Read `docs/TEAM_STATUS.md`.
3. Read `docs/API_CONTRACTS.md` if the work touches any API.
4. Read `docs/DATABASE_NOTES.md` if the work touches the schema.
5. Read `docs/AI_NOTES.md` if the work touches AI/RAG behavior.
6. Look through the existing repo for related code before creating anything
   new — don't duplicate what already exists.
7. Respect the ownership boundaries above.

After completing meaningful work:
1. Update `docs/TEAM_STATUS.md` (your section: current/completed work,
   branch, files owned, blockers, next task, last updated date).
2. Update `docs/API_CONTRACTS.md` if you added/changed an API.
3. Update `docs/DATABASE_NOTES.md` if you changed the schema.
4. Update `docs/AI_NOTES.md` if you changed AI behavior.
5. Update setup docs (README/.env.example) if dependencies/config changed.
6. Commit documentation together with the corresponding feature — not as a
   separate, later, easy-to-forget commit.

**This applies equally to human developers and LLM coding sessions.** Never
assume your session is the only one working on this repository — another
developer or another LLM may have changed things since you last looked.
