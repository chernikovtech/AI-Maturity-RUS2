"""
AI Literacy Assessment — Main Application
FastAPI server serving participant flow, admin panel, and live dashboard.
"""
import os
import io
import json
import asyncio
from datetime import datetime, timezone, date

from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, case

import qrcode

from database import get_db, init_db
from models import Event, Participant, Response as ParticipantResponse, Score
from scoring import compute_scores, get_level_info
from config import (
    ADMIN_PASSPHRASE, QUESTIONS, COUNTRIES, INDUSTRIES,
    DIMENSIONS, LEVELS, REGIONAL_BENCHMARKS, get_region_for_country,
)
from pdf_generator import generate_infographic_pdf


# ─── App Setup ───────────────────────────────────────────────────────────────
app = FastAPI(title="AI Literacy Assessment", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.on_event("startup")
def startup():
    init_db()


# ─── Helpers ─────────────────────────────────────────────────────────────────
def get_base_url(request: Request) -> str:
    scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("x-forwarded-host", request.url.hostname)
    port = request.url.port
    if port and port not in (80, 443):
        return f"{scheme}://{host}:{port}"
    return f"{scheme}://{host}"


def event_stats(db: Session, event_id: str) -> dict:
    """Compute aggregate stats for an event."""
    participants = (
        db.query(Participant)
        .filter(Participant.event_id == event_id, Participant.deleted_at.is_(None), Participant.submitted_at.isnot(None))
        .all()
    )
    if not participants:
        return {
            "count": 0, "avg_score": 0, "levels": {}, "dimensions": {},
            "countries": {}, "industries": {},
        }

    scores = []
    level_counts = {}
    dim_totals = {dk: [] for dk in DIMENSIONS}
    country_counts = {}
    industry_counts = {}

    for p in participants:
        if p.score:
            scores.append(p.score.total_score)
            level_counts[p.score.level] = level_counts.get(p.score.level, 0) + 1
            for dk, val in (p.score.dimension_scores or {}).items():
                dim_totals[dk].append(val)
        if p.country:
            country_counts[p.country] = country_counts.get(p.country, 0) + 1
        if p.industry:
            industry_counts[p.industry] = industry_counts.get(p.industry, 0) + 1

    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    dim_avgs = {}
    for dk, vals in dim_totals.items():
        dim_avgs[dk] = round(sum(vals) / len(vals), 1) if vals else 0

    return {
        "count": len(participants),
        "avg_score": avg_score,
        "levels": level_counts,
        "dimensions": dim_avgs,
        "countries": country_counts,
        "industries": industry_counts,
    }


# ─── Participant Flow ────────────────────────────────────────────────────────

@app.get("/event/{slug}", response_class=HTMLResponse)
def event_landing(slug: str, request: Request, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.slug == slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return templates.TemplateResponse("participant.html", {
        "request": request,
        "event": event,
        "questions": QUESTIONS,
        "countries": COUNTRIES,
        "industries": INDUSTRIES,
        "dimensions": DIMENSIONS,
        "levels": LEVELS,
        "questions_json": json.dumps(QUESTIONS),
        "countries_json": json.dumps(COUNTRIES),
        "industries_json": json.dumps(INDUSTRIES),
    })


@app.post("/api/event/{slug}/submit")
def submit_assessment(slug: str, request: Request, db: Session = Depends(get_db)):
    """Single endpoint: register + submit answers + compute score."""
    import json as _json
    # Parse body
    body = asyncio.get_event_loop().run_until_complete(request.json())

    event = db.query(Event).filter(Event.slug == slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != "active":
        raise HTTPException(status_code=400, detail="Event is closed")

    # Create participant
    participant = Participant(
        event_id=event.id,
        name=body.get("name", "").strip() or None,
        email=body.get("email", "").strip() or None,
        phone=body.get("phone", "").strip() or None,
        country=body.get("country", "").strip() or None,
        industry=body.get("industry", "").strip() or None,
        consent_store=body.get("consent_store", False),
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(participant)
    db.flush()

    # Save responses
    answers = body.get("answers", {})
    for q in QUESTIONS:
        key = q["key"]
        if key in answers:
            resp = ParticipantResponse(
                participant_id=participant.id,
                question_key=key,
                answer_value=int(answers[key]),
                dimension=q["dimension"],
            )
            db.add(resp)

    # Compute score
    result = compute_scores(answers)
    score = Score(
        participant_id=participant.id,
        total_score=result["total_score"],
        level=result["level"],
        dimension_scores=result["dimension_scores"],
    )
    db.add(score)
    db.commit()

    # Regional comparison
    region = get_region_for_country(participant.country or "")
    regional_data = REGIONAL_BENCHMARKS.get(region) if region else None
    global_avg = REGIONAL_BENCHMARKS["Global Average"]

    return {
        "participant_id": participant.id,
        "total_score": result["total_score"],
        "level": result["level"],
        "dimension_scores": result["dimension_scores"],
        "level_info": get_level_info(result["level"]),
        "regional_benchmark": {
            "region": region,
            "score": regional_data["score"] if regional_data else None,
            "level": regional_data["level"] if regional_data else None,
        } if regional_data else None,
        "global_benchmark": {
            "score": global_avg["score"],
            "level": global_avg["level"],
        },
    }


@app.get("/api/participant/{pid}/pdf")
def download_pdf(pid: str, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.id == pid, Participant.deleted_at.is_(None)).first()
    if not participant or not participant.score:
        raise HTTPException(status_code=404, detail="Not found")

    event = participant.event
    pdf_bytes = generate_infographic_pdf(
        total_score=participant.score.total_score,
        level=participant.score.level,
        dimension_scores=participant.score.dimension_scores,
        event_name=event.name if event else "",
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=ai-literacy-results.pdf"},
    )


@app.delete("/api/participant/{pid}")
def delete_participant(pid: str, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.id == pid).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Not found")

    # Soft delete: wipe PII, keep anonymous score for aggregates
    participant.name = None
    participant.email = None
    participant.phone = None
    participant.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "deleted"}


# ─── Dashboard ───────────────────────────────────────────────────────────────

@app.get("/dashboard/{slug}", response_class=HTMLResponse)
def dashboard_page(slug: str, request: Request, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.slug == slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    stats = event_stats(db, event.id)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "event": event,
        "stats": stats,
        "stats_json": json.dumps(stats),
        "dimensions": DIMENSIONS,
        "levels": LEVELS,
        "levels_json": json.dumps(LEVELS),
        "dimensions_json": json.dumps({k: v for k, v in DIMENSIONS.items()}),
        "benchmarks_json": json.dumps(REGIONAL_BENCHMARKS),
    })


@app.get("/api/dashboard/{slug}/stats")
def dashboard_stats(slug: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.slug == slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event_stats(db, event.id)


@app.get("/api/dashboard/{slug}/stream")
async def dashboard_stream(slug: str, db: Session = Depends(get_db)):
    """Server-Sent Events stream for live dashboard updates."""
    event = db.query(Event).filter(Event.slug == slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    async def generate():
        while True:
            # Get fresh session each iteration
            from database import SessionLocal
            session = SessionLocal()
            try:
                stats = event_stats(session, event.id)
                yield f"data: {json.dumps(stats)}\n\n"
            finally:
                session.close()
            await asyncio.sleep(3)  # Poll every 3 seconds

    return StreamingResponse(generate(), media_type="text/event-stream")


# ─── Admin ───────────────────────────────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("admin.html", {
        "request": request,
    })


@app.post("/api/admin/auth")
async def admin_auth(request: Request):
    body = await request.json()
    if body.get("passphrase") == ADMIN_PASSPHRASE:
        return {"status": "ok"}
    raise HTTPException(status_code=401, detail="Wrong passphrase")


@app.get("/api/admin/events")
def admin_list_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.created_at.desc()).all()
    result = []
    for e in events:
        count = (
            db.query(func.count(Participant.id))
            .filter(Participant.event_id == e.id, Participant.deleted_at.is_(None), Participant.submitted_at.isnot(None))
            .scalar()
        )
        result.append({
            "id": e.id,
            "name": e.name,
            "slug": e.slug,
            "location": e.location,
            "event_date": e.event_date.isoformat() if e.event_date else None,
            "status": e.status,
            "participant_count": count,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        })
    return result


@app.post("/api/admin/events")
async def admin_create_event(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    name = body.get("name", "").strip()
    slug = body.get("slug", "").strip().lower().replace(" ", "-")
    if not name or not slug:
        raise HTTPException(status_code=400, detail="Name and slug required")

    existing = db.query(Event).filter(Event.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")

    # Parse date string (YYYY-MM-DD) to Python date object
    event_date_str = body.get("event_date")
    event_date = None
    if event_date_str:
        try:
            event_date = date.fromisoformat(event_date_str)
        except (ValueError, TypeError):
            pass

    event = Event(
        name=name,
        slug=slug,
        description=body.get("description", ""),
        location=body.get("location", ""),
        event_date=event_date,
        status="active",
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"id": event.id, "slug": event.slug}


@app.put("/api/admin/events/{event_id}")
async def admin_update_event(event_id: str, request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if "status" in body:
        event.status = body["status"]
    if "name" in body:
        event.name = body["name"]
    db.commit()
    return {"status": "updated"}


@app.get("/api/admin/events/{event_id}/qr")
def admin_qr(event_id: str, request: Request, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    base = get_base_url(request)
    url = f"{base}/event/{event.slug}"

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#141414", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Use inline disposition so browsers can display it; download link uses <a download>
    return StreamingResponse(buf, media_type="image/png",
                             headers={"Content-Disposition": f"inline; filename=qr-{event.slug}.png"})


@app.get("/api/admin/events/{event_id}/participants")
def admin_participants(event_id: str, db: Session = Depends(get_db)):
    participants = (
        db.query(Participant)
        .filter(Participant.event_id == event_id, Participant.deleted_at.is_(None), Participant.consent_store == True)
        .order_by(Participant.submitted_at.desc())
        .all()
    )
    result = []
    for p in participants:
        result.append({
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "phone": p.phone,
            "country": p.country,
            "industry": p.industry,
            "total_score": p.score.total_score if p.score else None,
            "level": p.score.level if p.score else None,
            "submitted_at": p.submitted_at.isoformat() if p.submitted_at else None,
        })
    return result


# ─── Root redirect ───────────────────────────────────────────────────────────
@app.get("/")
def root():
    return RedirectResponse(url="/admin")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
