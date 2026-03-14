"""
Scoring engine
Computes AI literacy scores from participant responses.
"""
from config import DIMENSIONS, LEVELS, QUESTIONS


def compute_scores(answers: dict[str, int]) -> dict:
    """
    answers: {"context_q1": 3, "context_q2": 2, ...}
    Returns: {"total_score": 58.3, "level": "Practitioner", "dimension_scores": {...}}
    """
    # Group answers by dimension
    dim_answers: dict[str, list[int]] = {}
    for q in QUESTIONS:
        key = q["key"]
        dim = q["dimension"]
        if key in answers:
            dim_answers.setdefault(dim, []).append(answers[key])

    # Compute per-dimension scores (normalized 0-100)
    dimension_scores = {}
    all_raw = []
    for dim_key in DIMENSIONS:
        vals = dim_answers.get(dim_key, [])
        if vals:
            raw_avg = sum(vals) / len(vals)
            normalized = ((raw_avg - 1) / 3) * 100
            dimension_scores[dim_key] = round(normalized, 1)
            all_raw.extend(vals)
        else:
            dimension_scores[dim_key] = 0.0

    # Overall score
    if all_raw:
        overall_avg = sum(all_raw) / len(all_raw)
        total_score = round(((overall_avg - 1) / 3) * 100, 1)
    else:
        total_score = 0.0

    # Determine level
    level = "Explorer"
    for lvl in LEVELS:
        if lvl["min_pct"] <= total_score <= lvl["max_pct"]:
            level = lvl["label"]
            break
    # Handle edge case: score exactly 100
    if total_score > 75:
        level = "Architect"

    return {
        "total_score": total_score,
        "level": level,
        "dimension_scores": dimension_scores,
    }


def get_level_info(level_label: str) -> dict:
    for lvl in LEVELS:
        if lvl["label"] == level_label:
            return lvl
    return LEVELS[0]
