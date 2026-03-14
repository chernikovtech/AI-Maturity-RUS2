"""
PDF Infographic Generator
Creates a generic AI Literacy Framework infographic with the participant's score overlaid.
Uses ReportLab.
"""
import io
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from config import DIMENSIONS, LEVELS


# ─── Colors ──────────────────────────────────────────────────────────────────
RED = HexColor("#FF1A1A")
DARK = HexColor("#141414")
MID_GREY = HexColor("#7A7A7A")
LIGHT_BG = HexColor("#F5F5F5")
WHITE = white
LEVEL_COLORS = {
    "Explorer": HexColor("#7A7A7A"),
    "Learner": HexColor("#FF8C00"),
    "Practitioner": HexColor("#FF1A1A"),
    "Architect": HexColor("#141414"),
}

W, H = A4  # 595.28 x 841.89 points


def generate_infographic_pdf(
    total_score: float,
    level: str,
    dimension_scores: dict,
    event_name: str = "",
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    _draw_page(c, total_score, level, dimension_scores, event_name)

    c.save()
    buf.seek(0)
    return buf.read()


def _draw_page(c, total_score, level, dimension_scores, event_name):
    # ── Dark header band ─────────────────────────────────────────────────
    header_h = 200
    c.setFillColor(DARK)
    c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)

    # Logo text (since we can't embed custom fonts in reportlab easily)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, H - 40, "YANGO TECH")
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#999999"))
    c.drawString(30, H - 55, "AI Literacy Assessment")

    # Big score
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 60)
    c.drawString(30, H - 130, f"{total_score:.0f}")
    c.setFont("Helvetica", 14)
    c.drawString(30 + c.stringWidth(f"{total_score:.0f}", "Helvetica-Bold", 60) + 8, H - 115, "/ 100")

    # Level badge
    lvl_color = LEVEL_COLORS.get(level, RED)
    badge_x = 30
    badge_y = H - 175
    badge_w = c.stringWidth(level.upper(), "Helvetica-Bold", 13) + 30
    c.setFillColor(lvl_color)
    c.roundRect(badge_x, badge_y, badge_w, 28, 14, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(badge_x + 15, badge_y + 8, level.upper())

    # Event name
    if event_name:
        c.setFillColor(HexColor("#666666"))
        c.setFont("Helvetica", 9)
        c.drawRightString(W - 30, H - 40, event_name)

    # ── Radar chart (right side of header) ───────────────────────────────
    cx, cy = W - 140, H - 110
    _draw_radar(c, cx, cy, 70, dimension_scores)

    # ── Body background ──────────────────────────────────────────────────
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, W, H - header_h, fill=1, stroke=0)

    # ── Your Dimensions section ──────────────────────────────────────────
    y = H - header_h - 40
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, y, "YOUR DIMENSIONS")
    y -= 10

    dim_keys = list(DIMENSIONS.keys())
    for i, dk in enumerate(dim_keys):
        y -= 42
        dim = DIMENSIONS[dk]
        score = dimension_scores.get(dk, 0)

        # Label
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DARK)
        c.drawString(30, y + 10, dim["label"].upper())

        # Score value
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(RED)
        c.drawRightString(W - 30, y + 10, f"{score:.0f}%")

        # Progress bar
        bar_x = 30
        bar_y = y - 2
        bar_w = W - 60
        bar_h = 8

        c.setFillColor(HexColor("#E2E2E2"))
        c.roundRect(bar_x, bar_y, bar_w, bar_h, 4, fill=1, stroke=0)
        if score > 0:
            fill_w = max(8, bar_w * score / 100)
            c.setFillColor(RED)
            c.roundRect(bar_x, bar_y, fill_w, bar_h, 4, fill=1, stroke=0)

    # ── The Framework section ────────────────────────────────────────────
    y -= 50
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, y, "AI LITERACY FRAMEWORK")
    c.setFont("Helvetica", 9)
    c.setFillColor(MID_GREY)
    c.drawString(30, y - 16, "Based on Nate Jones' 10-Level Fluency Scale & Judgment Layer")
    y -= 40

    # Level boxes
    for lvl in LEVELS:
        box_h = 52
        y -= box_h + 8

        # Background
        c.setFillColor(WHITE)
        c.roundRect(30, y, W - 60, box_h, 10, fill=1, stroke=0)

        # Color indicator
        c.setFillColor(HexColor(lvl["color"]))
        c.roundRect(30, y, 6, box_h, 3, fill=1, stroke=0)

        # Level name
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(48, y + box_h - 18, lvl["label"].upper())

        # Score range
        c.setFont("Helvetica", 9)
        c.setFillColor(MID_GREY)
        c.drawRightString(W - 40, y + box_h - 18, f"{lvl['min_pct']}–{lvl['max_pct']}%")

        # Description (truncated to fit)
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor("#555555"))
        desc = lvl["description"][:120] + ("..." if len(lvl["description"]) > 120 else "")
        c.drawString(48, y + 10, desc)

        # Highlight current level
        if lvl["label"] == level:
            c.setStrokeColor(RED)
            c.setLineWidth(2)
            c.roundRect(30, y, W - 60, box_h, 10, fill=0, stroke=1)

    # ── Footer ───────────────────────────────────────────────────────────
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 7)
    c.drawString(30, 20, "Powered by Yango Tech  |  Framework: Nate Jones / PAICE  |  tech.yango.com")
    c.drawRightString(W - 30, 20, "This is a self-assessment indicator, not a certification.")


def _draw_radar(c, cx, cy, radius, dimension_scores):
    """Draw a simple radar/spider chart."""
    dims = list(DIMENSIONS.keys())
    n = len(dims)
    if n == 0:
        return

    angle_step = 2 * math.pi / n
    start_angle = math.pi / 2  # start at top

    # Background circles
    for r_frac in [0.25, 0.5, 0.75, 1.0]:
        r = radius * r_frac
        c.setStrokeColor(HexColor("#555555"))
        c.setLineWidth(0.3)
        c.circle(cx, cy, r, fill=0, stroke=1)

    # Axis lines and labels
    points = []
    for i, dk in enumerate(dims):
        angle = start_angle - i * angle_step
        x_end = cx + radius * math.cos(angle)
        y_end = cy + radius * math.sin(angle)

        c.setStrokeColor(HexColor("#555555"))
        c.setLineWidth(0.3)
        c.line(cx, cy, x_end, y_end)

        # Labels
        label_r = radius + 14
        lx = cx + label_r * math.cos(angle)
        ly = cy + label_r * math.sin(angle)
        c.setFillColor(HexColor("#CCCCCC"))
        c.setFont("Helvetica", 6)
        c.drawCentredString(lx, ly - 3, DIMENSIONS[dk]["short"].upper())

        # Data point
        score = dimension_scores.get(dk, 0)
        data_r = radius * score / 100
        px = cx + data_r * math.cos(angle)
        py = cy + data_r * math.sin(angle)
        points.append((px, py))

    # Draw filled polygon
    if points:
        p = c.beginPath()
        p.moveTo(points[0][0], points[0][1])
        for px, py in points[1:]:
            p.lineTo(px, py)
        p.close()
        c.setFillColor(Color(1, 0.1, 0.1, alpha=0.25))
        c.setStrokeColor(RED)
        c.setLineWidth(1.5)
        c.drawPath(p, fill=1, stroke=1)

        # Dots
        for px, py in points:
            c.setFillColor(RED)
            c.circle(px, py, 3, fill=1, stroke=0)
