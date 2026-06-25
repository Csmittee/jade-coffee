# CLAUDE.md — jade-coffee
> Version 1.0 — 2026-06-25
> Changes: Initial creation — governance seed
> Previous: NONE

Project: Jade Coffee — Premium coffee capsule mini-site (BUS03)
Domain: jade.janishammer.com
BUS ID: BUS03

Governance: ALL rules at janishammer-central/RULES.md + .claude/rules/
Read janishammer-central CLAUDE.md before reading anything in this repo.

Injector:
  injector-config.js — YES — sync from assets.janishammer.com
  injector-core.js   — YES — sync from assets.janishammer.com

Local key files:
  index.html                    — EN homepage (463L) — products in "coming soon" state
  scripts/generate-products.py  — Airtable → product HTML (not yet active)
  products.json                 — product data placeholder

Critical constraint: No Thai homepage (th/index.html) exists — this is structural
debt. TH users land on EN-only site. See RETROFIT_QUEUE item #10.
og:type, canonical, twitter cards, and schema.org all missing. See items #1–#4.

Tech: Vanilla HTML/CSS/JS · Airtable · Python build · GitHub Actions · Cloudflare Pages
