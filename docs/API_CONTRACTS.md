# API Contracts

> **Read before touching any API.** This is the single source of truth for
> backend/frontend API agreements. Frontend (Person 3) must build against
> what's documented here, not invent response shapes. Backend (Person 1,
> Person 2) must update this file the same commit/PR an API is added or
> changed. Don't rename a shared endpoint or schema without updating this
> file first.
>
> Status values: `PLANNED` (agreed shape, not built) · `IN_PROGRESS`
> (being implemented) · `IMPLEMENTED` (live and matches this doc).
>
> No APIs exist yet — this file currently contains only the template and
> section placeholders for MVP scope. Fill in real entries as endpoints are
> built; do not pre-build speculative endpoints beyond MVP scope.

---

## How to add an entry

Copy this block per endpoint:

```
### METHOD /path/to/endpoint

- **Owner:** Person 1 | Person 2 | Person 3
- **Status:** PLANNED | IN_PROGRESS | IMPLEMENTED
- **Authorization:** e.g. "Bearer JWT, role: admin" or "public"
- **Request schema:**
  ```json
  { "field": "type" }
  ```
- **Response schema:**
  ```json
  { "field": "type" }
  ```
- **Notes:** edge cases, pagination, error shapes, etc.
```

---

## Auth

_(none yet — planned: `POST /auth/login`, `POST /auth/refresh`,
`GET /auth/me`, owner: Person 1)_

## Admin — Documents / Institutes / Users

_(none yet — planned: AICTE document upload + metadata CRUD, institute CRUD,
user/role management, owner: Person 1)_

## Curriculum Designer — Curriculum CRUD

_(none yet — planned: Curriculum/Semester/Course/Module/Topic CRUD, draft
save, submit-for-review, owner: Person 1)_

## Designer AI Chatbot (3 modes)

_(none yet — planned: single chat endpoint parameterized by mode
[`aicte_assistant` | `resource_assistant` | `comparison_assistant`], owner:
Person 2 — see [AI_NOTES.md](AI_NOTES.md) for shared schema shape)_

## Reviewer — Review Workflow

_(none yet — planned: list submitted curricula, get curriculum detail,
comment, request-changes, approve, reject, owner: Person 1)_

## Reviewer — Curriculum Analyzer / AI Screener

_(none yet — planned: run analyzer, run screener, both returning structured
Pydantic-backed JSON, owner: Person 2 — see [AI_NOTES.md](AI_NOTES.md))_

---

## Common conventions (apply to all future endpoints)

- All authenticated endpoints expect `Authorization: Bearer <JWT>`.
- Error responses use a consistent shape (to be fixed by Person 1 when auth
  lands and documented here — do not let each endpoint invent its own error
  format).
- Pagination (when needed) should use a consistent `limit`/`offset` or
  cursor convention — to be decided by Person 1 and documented here before
  the first paginated list endpoint ships.
- Curriculum status values are restricted to the workflow enum defined in
  [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §7 / [DATABASE_NOTES.md](DATABASE_NOTES.md).
