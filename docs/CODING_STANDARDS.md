# Coding Standards

## Principles

- Keep feature boundaries clear between frontend, backend, shared contracts, infrastructure, and scripts.
- Prefer small services, typed schemas, and explicit interfaces over large files with mixed responsibilities.
- Keep demo mode reliable by supporting mock AI and search providers before requiring external API keys.
- Add tests with each meaningful backend behavior and document frontend test gaps until the test stack is initialized.

## TypeScript

- Use strict TypeScript once the Next.js app is initialized.
- Keep reusable UI in `apps/web/components` and domain workflows in `apps/web/features`.
- Validate form inputs with Zod and React Hook Form.
- Keep API clients in `apps/web/lib` and shared types in `packages/api-contracts` when contracts stabilize.
- Include loading, empty, and error states for user-facing pages.

## Python

- Use typed Pydantic schemas at API boundaries.
- Keep FastAPI routers thin; put business behavior in services and persistence in repositories.
- Prefer dependency-injected providers for LLMs, embeddings, search, retrieval, and token accounting.
- Record structured logs for workflow transitions, errors, latency, and token usage.
- Add Pytest coverage for auth, quotas, research runs, token usage, vector search, and source validation as those modules land.

## API Design

- Version public routes under `/api/v1`.
- Return stable JSON response shapes with explicit status fields for asynchronous workflows.
- Do not run long research workflows directly inside request handlers.
- Use background jobs first, then upgrade to a Redis-backed worker where planned.

## Data And Migrations

- Use migrations for schema changes after Alembic is introduced.
- Store agent step inputs, outputs, latency, status, token usage, and errors for observability.
- Treat prompt files and prompt version metadata as versioned product assets.

## Security

- Keep secrets out of Git.
- Use HTTP-only auth cookies and secure cookie settings outside local development.
- Enforce user/admin role checks on backend routes, not only in the frontend.
- Never log raw secrets, JWTs, passwords, or provider API keys.

## Git Hygiene

- Keep each day as a meaningful commit.
- Avoid broad refactors that are not part of the current day.
- Update documentation when architecture, commands, or environment variables change.

