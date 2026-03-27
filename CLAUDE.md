# AI Literacy Assessment App

## What This Is

A live event tool for measuring AI literacy of round-table participants. Participants scan a QR code, answer 12 quick questions (~3 min), get a personal score, and aggregated results display live on a projector screen. Built for Yango Tech events.

## Tech Stack

- **Backend**: Python 3.12 + FastAPI (single monolith)
- **Database**: PostgreSQL on Railway (falls back to SQLite locally)
- **Frontend**: Static HTML/CSS/JS served by FastAPI via Jinja2 templates — NO React, NO build step
- **Real-time**: Server-Sent Events (SSE) for live dashboard updates (3s polling)
- **PDF**: ReportLab for post-test infographic generation
- **QR**: `qrcode` library, generated server-side per event
- **Deployment**: Railway.app (single service + Postgres addon)
- **Styling**: Yango Tech design system (custom fonts from yastatic.net, `#FF1A1A` red accent, monochrome palette)

## Project Structure

```
ai-literacy/
├── main.py              # FastAPI app — ALL routes (participant, admin, dashboard, API)
├── config.py            # Questions, scoring config, countries, industries, benchmarks
├── models.py            # SQLAlchemy models (Event, Participant, Response, Score)
├── database.py          # DB connection, session management, init
├── scoring.py           # Score computation from answers → level + dimensions
├── pdf_generator.py     # ReportLab PDF infographic with radar chart
├── requirements.txt     # Python deps
├── Procfile             # Railway entry point
├── railway.toml         # Railway build config
├── static/
│   ├── css/style.css    # All styles — Yango Tech design system
│   ├── js/.gitkeep
│   └── img/.gitkeep
└── templates/
    ├── participant.html  # Full participant flow (welcome → register → quiz → results)
    ├── dashboard.html    # Live projector dashboard with SSE
    └── admin.html        # Admin panel (passphrase-gated, event CRUD, QR, participants)
```

## Architecture Decisions

- **Single-page flows via JS**: Each template (participant, admin) handles multiple "steps" via show/hide with JS — no page reloads during the flow
- **No frontend framework**: Vanilla JS, no React/Vue. Templates use Jinja2 for server-side data injection (`{{ var }}` and `{{ var_json|safe }}`)
- **Questions defined in config.py, NOT in DB**: They change rarely; keeping them in code avoids unnecessary complexity
- **Soft delete for GDPR**: `deleted_at` timestamp on Participant — PII wiped, anonymous score kept for aggregates
- **SSE not WebSocket**: Dashboard uses `EventSource` → `/api/dashboard/{slug}/stream`. One-directional, simpler than WS
- **Static dirs created at startup**: `os.makedirs(exist_ok=True)` in main.py because Railway/git may not preserve empty dirs

## Key URLs

| URL | Purpose |
|---|---|
| `/admin` | Admin panel (passphrase: `yangotech2026` — set in config.py) |
| `/event/{slug}` | Participant entry point (what QR code points to) |
| `/dashboard/{slug}` | Live projector display |

## Data Model

- **events**: id, name, slug (unique, used in URLs), description, location, event_date, status (active/closed)
- **participants**: id, event_id (FK), name/email/phone (all nullable), country, industry, consent_store (bool), submitted_at, deleted_at (soft delete)
- **responses**: id, participant_id (FK), question_key, answer_value (1-4), dimension
- **scores**: id, participant_id (FK, unique), total_score (0-100 float), level (Explorer/Learner/Practitioner/Architect), dimension_scores (JSON)

## Scoring System

Based on Nate Jones' AI Fluency Framework + Judgment Layer:

**4 Levels**: Explorer (0-25%) → Learner (26-50%) → Practitioner (51-75%) → Architect (76-100%)

**6 Dimensions** (2 questions each = 12 total):
1. Context Assembly
2. Quality Judgment
3. Task Decomposition
4. Iterative Refinement
5. Workflow Integration
6. Frontier Recognition

Each answer scored 1-4. Normalization: `((raw_avg - 1) / 3) * 100`

## Styling Rules (Yango Tech)

- **Fonts**: `Yango Headline` (900 weight, headings, uppercase) + `Yango Group Text` (body, UI)
- **Colors**: `#FF1A1A` (primary/CTA only), `#141414` (dark), `#F5F5F5` (body bg), `#7A7A7A` (secondary text)
- **Radii**: Cards `1.875rem`, inputs `1.25rem`, buttons `2rem` (pill-shaped)
- **No shadows, no gradients** on surfaces — use white-on-#F5F5F5 contrast
- **Typography**: Headings uppercase; body text sentence case with `0.05em` spacing; UI chrome (labels, buttons) uppercase with `0.12em` spacing
- **Dark hero sections** (#000 bg, white text), light body sections (#F5F5F5)

## API Endpoints

```
# Participant
GET   /event/{slug}                    # Landing page
POST  /api/event/{slug}/submit         # Register + submit answers + get score (single call)
GET   /api/participant/{pid}/pdf       # Download results PDF
DELETE /api/participant/{pid}           # Soft-delete personal data

# Dashboard
GET   /dashboard/{slug}                # Projector page
GET   /api/dashboard/{slug}/stats      # Current stats JSON
GET   /api/dashboard/{slug}/stream     # SSE stream

# Admin
GET   /admin                           # Admin panel
POST  /api/admin/auth                  # Passphrase check
GET   /api/admin/events                # List events
POST  /api/admin/events                # Create event
PUT   /api/admin/events/{id}           # Update event
GET   /api/admin/events/{id}/qr        # Download QR PNG
GET   /api/admin/events/{id}/participants  # List consenting participants
```

## Environment Variables

- `DATABASE_URL` — Railway provides this automatically when Postgres addon is attached. Falls back to `sqlite:///./ai_literacy.db` for local dev.
- `PORT` — Railway provides this. Default 8000 locally.

## Running Locally

```bash
pip install -r requirements.txt
python main.py
# → http://localhost:8000/admin
```

## Common Tasks

- **Add/edit questions**: Edit `QUESTIONS` list in `config.py`. Each question has `key`, `dimension`, `text`, `options` (with scores 1-4), and `display_order` (shuffled indices)
- **Change admin passphrase**: Edit `ADMIN_PASSPHRASE` in `config.py`
- **Add countries/industries**: Edit `COUNTRIES` / `INDUSTRIES` lists in `config.py`
- **Adjust scoring thresholds**: Edit `LEVELS` in `config.py`
- **Modify PDF layout**: Edit `pdf_generator.py` — uses ReportLab canvas API
- **Style changes**: Edit `static/css/style.css` — follow Yango Tech design rules above

## Known Limitations / TODO

- Admin auth is passphrase-only (no sessions — re-enter on refresh)
- No export to CSV/Excel from admin yet
- PDF uses Helvetica (ReportLab built-in) instead of Yango fonts
- No email notifications
- English only
- SSE reconnects on error with 5s delay — could be more graceful

