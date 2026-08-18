# AI Notes

> **Read before touching AI/RAG behavior.** Owned and kept current by
> Person 2. Person 1 and Person 3 should read this before integrating with
> or depending on AI endpoints. Update this file whenever RAG architecture,
> embedding/LLM choices, retrieval strategy, or AI response schemas change.

## Principle: one shared AI foundation, not five systems

All AI features — the Designer's 3 chatbot modes, the Curriculum Analyzer,
and the AI Curriculum Screener — reuse the **same** pipeline:

```
AICTE Documents + Curriculum Data + Resources + Anonymous Benchmark Data
  → Document Processing (PyMuPDF extraction, chunking)
  → Embeddings (sentence-transformers)
  → pgvector (inside shared Neon Postgres)
  → Retriever
  → Context Builder
  → LLM (external API)
  → { AICTE Assistant | Resource Assistant | Comparison Assistant |
      Curriculum Analyzer | Curriculum Screener }
```

Do not build a separate vector store, separate backend, or per-feature
one-off retrieval logic. Do not duplicate curriculum database logic inside
AI modules — call into Person 1's services/repositories for curriculum
data (flow: `Router → AI Service → Domain Query Service → Retriever/LLM`).

## Status

Foundation stage — **no AI code exists yet**. This file is a template to be
filled in as Person 2 makes real decisions.

## Embedding model

_(not yet chosen — to be filled in by Person 2, e.g. a specific
sentence-transformers model name/dimension)_

## LLM provider

_(not yet chosen — to be filled in by Person 2: provider, model name, and
how the API key is configured via environment variable)_

## Retrieval strategy

_(not yet designed — to be filled in: chunk size/overlap, top-k, filtering by
document type/curriculum scope, re-ranking if any)_

## Designer chatbot — one interface, three modes

Single chat endpoint/UI, parameterized by mode. Do not build three
disconnected chatbots.

1. **AICTE / Curriculum Assistant**
   - Answers designer questions about curriculum creation and AICTE
     requirements (credit structure, learning outcomes, prerequisites,
     applicable rules, assessment methods, course improvement suggestions).
   - Retrieval source: AICTE documents/policies/regulations + the
     designer's currently selected curriculum context.
   - Must show source document/page where possible.
   - **Must never invent AICTE rules** — if retrieval finds nothing
     relevant, say so rather than fabricating a rule.

2. **AI Resource Assistant**
   - Recommends educational resources (textbooks, papers, articles, videos,
     lecture/practical/lab material, references) for a selected
     curriculum/course/module/topic.
   - Each recommendation must state: what resource, resource type, relevant
     topic/module, and why it's useful.
   - No live internet crawling in MVP — resources come from a
     pre-populated/managed resource set.

3. **Anonymous Curriculum Comparison Assistant**
   - Compares the designer's curriculum against strong approved benchmark
     curricula.
   - **Hard privacy requirement:** never expose institute name, institute
     ID, institute address, or curriculum owner identity — in the response
     text, in any metadata field, or via retrieval leakage. Only "Anonymous
     Benchmark" / aggregated comparison labels are shown.
   - Output shape: per-topic/area rating (e.g. Strong / Partial / Missing /
     Good) followed by problem → evidence → recommended improvement →
     suggested addition.
   - Goal is improving the curriculum, not copying another institute's.

## Curriculum Analyzer (Reviewer-side)

Structured (Pydantic) output, not raw free text. Includes:
- Overall score
- Category scores (AICTE compliance, curriculum structure, course
  coverage, learning outcomes, assessment alignment, practical exposure,
  resource coverage, industry relevance, skill coverage)
- Per-issue: `PROBLEM → EVIDENCE → WHY IT MATTERS → SOLUTION → SUGGESTED
  REVISION`

Must always provide actionable solutions, not just criticism.

## AI Curriculum Screener (Reviewer-side)

Decision support only — **never** makes the final approve/reject call.
Structured output includes:
- Overall screening score (0–100)
- Category sub-scores (AICTE compliance, structure, credits, course/topic
  coverage, learning outcomes, assessments, practical component, resources,
  prerequisites, completeness)
- Issues tagged `HIGH` / `MEDIUM` / `LOW`
- One recommendation label: `LIKELY_READY_FOR_REVIEW` |
  `CHANGES_RECOMMENDED` | `MAJOR_ISSUES_DETECTED`

The Reviewer alone chooses APPROVE / REJECT / REQUEST CHANGES via Person 1's
review workflow — the Screener's output is informational input to that
decision, never a substitute for it.

## AI response schemas

_(none defined yet — to be filled in with actual Pydantic model shapes once
Person 2 builds them; mirror the shapes into
[API_CONTRACTS.md](API_CONTRACTS.md) for the corresponding endpoints)_

## AI-related API contracts / assumptions

- AI endpoints live inside the same FastAPI backend as everything else —
  see [API_CONTRACTS.md](API_CONTRACTS.md) "Designer AI Chatbot" and
  "Reviewer — Curriculum Analyzer / AI Screener" sections, to be filled in
  as built.
- AI modules read curriculum data through Person 1's domain services, not
  direct ad-hoc queries against curriculum tables.
