# SaaS MVP — 3 micro-produits

## Structure

```
~/saas-mvp/
├── api-finance/          # 1. API données financières curatées (XAUUSD SMC/CVD)
├── boilerplate-saas/     # 2. Boilerplate Next.js + Supabase + IA (Stripe billing)
├── reddit-validator/     # 3. Outil validation Reddit → idée SaaS
```

## Specs (semaine 1-2)

| # | Projet | Stack | Validation |
|---|--------|-------|------------|
| 1 | API données financières curatées | Python/FastAPI, PostgreSQL, Docker, n8n | Landing 1 page + waitlist email → 50+ inscriptions |
| 2 | Boilerplate SaaS Next.js + Supabase + IA | Next.js 14, Supabase, Stripe, Tailwind, TypeScript | Page waitlist + pré-ventes 50€ → 10+ |
| 3 | Outil validation Reddit → idée SaaS | n8n, Python LLM, PostgreSQL, React | Démo live sur 3 niches → 3 feedbacks positifs |

## Convention de travail

- TDD obligatoire (pytest backend, vitest frontend)
- `docker compose up` en local avant tout
- Secrets via `openclaw secrets set` — JAMAIS en chat
- Docs : README + ARCHITECTURE.md + DEPLOY.md par projet

## Status global

- ✅ Repo initialisé
- 🔄 Projet 1 (API finance) en cours — priorite absolue (réutilise la stack QuantLive)
- ⏳ Projets 2 et 3 — backlog
