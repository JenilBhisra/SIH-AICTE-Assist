# Database Notes

> **Read before touching the schema.** Owned primarily by Person 1 (core
> entities) with Person 2 adding AI-specific tables (embeddings/chunks) that
> reference — but don't duplicate — Person 1's entities. Any schema change
> must update this file in the same commit/PR as the migration.

## Database

- Single shared **Neon PostgreSQL** project for the whole team.
- Every developer uses their own local `.env` with `DATABASE_URL` pointing
  at the shared Neon project. Never commit real credentials — only
  `.env.example` with variable names.
- **pgvector** extension is enabled on this same database for embeddings —
  there is no separate vector store.

## Schema change process (mandatory)

1. Pull latest `develop` before starting any schema change.
2. Change/add SQLAlchemy models under `backend/app/`.
3. Generate an Alembic migration (`alembic revision --autogenerate -m "..."`),
   review the generated SQL by hand before committing.
4. Commit the model change and the migration **together**.
5. Update this file (models/relationships/enums section below) in the same
   commit.
6. Push, open PR into `develop`.
7. After merge, every other developer pulls and runs `alembic upgrade head`
   locally.

**Never** hand-edit tables directly on the shared Neon project outside of a
migration — that breaks everyone else's `alembic upgrade head`.

## Models

_(none yet — foundation stage, no models created)_

Planned core entities (Person 1), per [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md):

- `User` (with role: admin / designer / reviewer)
- `Institute` (AICTE-approved institutes)
- `Document` (AICTE PDFs: rules/regulations/policies/guidelines/circulars +
  metadata)
- `Curriculum` → `Semester` → `Course` → `Module` → `Topic`
- `Course` associations: objectives, learning outcomes, credits,
  prerequisites, assessments, resources
- Review workflow entities: review comments, change requests, decisions

Planned AI-side entities (Person 2), additive only — must reference
Person 1's entities via foreign key, not duplicate their fields:

- Document/curriculum chunk + embedding tables (pgvector column)
- Anonymized benchmark curriculum representation (must not store/expose
  institute identity in any field reachable by the Designer-facing API —
  see [AI_NOTES.md](AI_NOTES.md))
- Analyzer/Screener run results (structured, versioned by curriculum
  revision)

## Enums

_(none yet)_ — planned: curriculum workflow status enum matching
[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) §7:

```
DRAFT, SUBMITTED, UNDER_REVIEW, CHANGES_REQUESTED, RESUBMITTED, APPROVED, REJECTED
```

Transitions between these are enforced in backend service logic, not left
open at the database or API layer.

## Migrations

_(none yet — `backend/alembic/` not yet initialized)_

## Ownership notes

- Person 1 owns core schema (users, institutes, documents metadata,
  curricula and children, review workflow).
- Person 2 owns AI-specific tables (chunks, embeddings, benchmark data,
  analyzer/screener results) and must coordinate with Person 1 before
  adding foreign keys into core tables.
- Person 3 never touches this file's subject matter directly — frontend has
  no direct DB access.
