# Team Status (Live)

> **Read this before starting work. Update this after finishing meaningful
> work.** This file is the live coordination point for 3 developers and
> multiple LLM sessions working on this repo at the same time. If you
> haven't read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) yet, read that first.
>
> When updating your section: keep it accurate and current, don't leave
> stale "current work" entries once something is done, and always set
> **Last updated**. Convert relative dates ("today", "tomorrow") to absolute
> dates when writing entries.

---

## Person 1 — Core Backend + Database

- **Current work:** _(none yet — foundation stage)_
- **Completed work:**
  - 2026-08-18: Repository foundation created (monorepo structure, shared
    docs, backend/frontend skeletons). Not backend-logic work specifically,
    but the scaffold all backend work will build on.
- **Current branch:** _(not yet created — start from `develop` off `main`)_
- **Modules/files owned:** `backend/app/` (core, models, auth, RBAC, users,
  institutes, documents metadata, policies, curricula, semesters, courses,
  modules, outcomes, assessments, review workflow), `backend/alembic/`
- **Dependencies:** None blocking yet.
- **Blockers:** None.
- **Next task:** Set up FastAPI app skeleton details (config/settings via
  env vars), SQLAlchemy engine/session, Alembic initialized against the
  shared Neon `DATABASE_URL`, then User/Role/Institute models + first
  migration + JWT auth. Fill in `docs/DATABASE_NOTES.md` as models land, and
  `docs/API_CONTRACTS.md` for auth endpoints.
- **Last updated:** 2026-08-18

---

## Person 2 — AI / RAG

- **Current work:** _(none yet — foundation stage)_
- **Completed work:** None yet.
- **Current branch:** _(not yet created — suggested: `feature/p2-ai-foundation`)_
- **Modules/files owned:** AI/RAG modules inside `backend/app/` (to be
  created under e.g. `backend/app/ai/` — coordinate naming with Person 1
  before creating, to avoid clashing with their package layout)
- **Dependencies:** Needs Person 1's document-metadata model and curriculum
  models to exist (at least in draft form) before wiring retrieval context
  builders end-to-end; can start PDF extraction/chunking/embedding
  utilities independently in the meantime.
- **Blockers:** None yet.
- **Next task:** Decide embedding model (sentence-transformers) and LLM
  provider, confirm pgvector extension usage on the shared Neon project,
  and start PDF extraction (PyMuPDF) + chunking utilities. Document choices
  in `docs/AI_NOTES.md` as they're made — that file is currently only a
  template.
- **Last updated:** 2026-08-18

---

## Person 3 — Frontend + Integration

- **Current work:** _(none yet — foundation stage)_
- **Completed work:** None yet.
- **Current branch:** _(not yet created — suggested: `feature/p3-frontend-foundation`)_
- **Modules/files owned:** `frontend/` (entire app)
- **Dependencies:** Needs `docs/API_CONTRACTS.md` entries from Person 1
  (auth endpoints) before building real login/dashboard integration; can
  start routing/layout/shadcn setup independently in the meantime.
- **Blockers:** None yet.
- **Next task:** Initialize the Vite + React + TypeScript app for real
  (currently only a minimal placeholder skeleton exists), add Tailwind +
  shadcn/ui + React Router + TanStack Query + React Hook Form + Zod, and
  set up the base route structure (login page placeholder, 3 dashboard
  shells) once Person 1 publishes the auth contract.
- **Last updated:** 2026-08-18

---

## Repository-wide notes

- Foundation created 2026-08-18: monorepo layout, `README.md`,
  `CONTRIBUTING.md`, `docs/` (this file + `PROJECT_CONTEXT.md` +
  `API_CONTRACTS.md` + `DATABASE_NOTES.md` + `AI_NOTES.md`), `.gitignore`,
  `.env.example` for both `backend/` and `frontend/`, and minimal
  `backend/`/`frontend/` skeletons. No feature code yet.
- Git remote/history: repository was empty at foundation time — no commits
  yet. First commit should be this foundation scaffold.
- Suggested branch names going forward: `feature/p1-...`,
  `feature/p2-...`, `feature/p3-...` off `develop`.
