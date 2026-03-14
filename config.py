"""
AI Literacy Test Configuration
Questions, scoring, reference data
"""

# ─── Admin ───────────────────────────────────────────────────────────────────
ADMIN_PASSPHRASE = "yangotech2026"

# ─── Maturity Levels ─────────────────────────────────────────────────────────
LEVELS = [
    {"key": "explorer", "label": "Explorer", "min_pct": 0, "max_pct": 25,
     "description": "You're at the start of your AI journey. You use AI occasionally for basic tasks like rewriting text or quick searches. There's a huge opportunity ahead — with some structured practice, you can rapidly level up.",
     "color": "#7A7A7A"},
    {"key": "learner", "label": "Learner", "min_pct": 26, "max_pct": 50,
     "description": "You understand AI basics and use it regularly, but haven't yet built systematic habits. You're past the curiosity phase — now it's about developing consistent workflows and learning to evaluate AI output critically.",
     "color": "#FF8C00"},
    {"key": "practitioner", "label": "Practitioner", "min_pct": 51, "max_pct": 75,
     "description": "You work with AI systematically. You know how to set it up for success, catch its mistakes, and have repeatable processes. You're the person your team turns to for AI guidance.",
     "color": "#FF1A1A"},
    {"key": "architect", "label": "Architect", "min_pct": 76, "max_pct": 100,
     "description": "You design AI-powered systems and workflows. You understand model limitations deeply, use multiple specialized tools, and continuously push the boundaries of what's possible. You don't just use AI — you orchestrate it.",
     "color": "#141414"},
]

# ─── Dimensions (6 from Nate Jones Judgment Layer) ───────────────────────────
DIMENSIONS = {
    "context_assembly": {
        "label": "Context Assembly",
        "short": "Context",
        "description": "The skill of providing AI with exactly the right background, constraints, and examples to get high-quality output.",
    },
    "quality_judgment": {
        "label": "Quality Judgment",
        "short": "Quality",
        "description": "The ability to detect errors, hallucinations, and calibrate review depth based on task risk.",
    },
    "task_decomposition": {
        "label": "Task Decomposition",
        "short": "Decomposition",
        "description": "Breaking large goals into AI-appropriate sub-tasks for better, more controlled results.",
    },
    "iterative_refinement": {
        "label": "Iterative Refinement",
        "short": "Refinement",
        "description": "Treating first outputs as drafts and systematically improving them through structured feedback.",
    },
    "workflow_integration": {
        "label": "Workflow Integration",
        "short": "Workflow",
        "description": "Embedding AI into daily work processes with repeatable prompts and documented playbooks.",
    },
    "frontier_recognition": {
        "label": "Frontier Recognition",
        "short": "Frontier",
        "description": "Knowing where AI excels and where it breaks — and adapting your approach accordingly.",
    },
}

# ─── Questions ───────────────────────────────────────────────────────────────
# Each question has 4 options scored 1-4 (Explorer → Architect)
# display_order is shuffled per question to avoid obvious patterns

QUESTIONS = [
    # ── Context Assembly ──
    {
        "key": "context_q1",
        "dimension": "context_assembly",
        "text": "You need AI to help you write a client proposal. What do you give it?",
        "options": [
            {"text": "\"Write me a proposal\"", "score": 1},
            {"text": "I paste in all my notes, emails, and documents — the more the better", "score": 2},
            {"text": "I give it the client brief, our value prop, the desired tone, and a sample proposal", "score": 3},
            {"text": "I have a reusable prompt template that I customize per client with exactly the right context", "score": 4},
        ],
        "display_order": [2, 0, 3, 1],
    },
    {
        "key": "context_q2",
        "dimension": "context_assembly",
        "text": "When you use AI for a task, how much background do you typically provide?",
        "options": [
            {"text": "I just ask the question directly", "score": 1},
            {"text": "I give it a lot of background — better safe than sorry", "score": 2},
            {"text": "I think about what context the AI actually needs and provide just that", "score": 3},
            {"text": "I've tested what context level gets the best results and adjust accordingly", "score": 4},
        ],
        "display_order": [0, 3, 1, 2],
    },
    # ── Quality Judgment ──
    {
        "key": "quality_q1",
        "dimension": "quality_judgment",
        "text": "AI writes a detailed, confident two-page analysis for you. What do you do?",
        "options": [
            {"text": "If it sounds right, I use it", "score": 1},
            {"text": "I skim it and fix obvious mistakes", "score": 2},
            {"text": "I fact-check the key claims and verify numbers from original sources", "score": 3},
            {"text": "I calibrate my review depth based on risk — low-stakes gets a quick scan, high-stakes gets full verification", "score": 4},
        ],
        "display_order": [3, 1, 0, 2],
    },
    {
        "key": "quality_q2",
        "dimension": "quality_judgment",
        "text": "How would you describe AI's \"confidence\" in its answers?",
        "options": [
            {"text": "If it sounds confident, it's probably right", "score": 1},
            {"text": "I know AI can be wrong sometimes, so I stay careful", "score": 2},
            {"text": "AI's confident tone is a language feature, not a measure of accuracy", "score": 3},
            {"text": "I've mapped specific areas where AI sounds confident but is unreliable", "score": 4},
        ],
        "display_order": [1, 3, 2, 0],
    },
    # ── Task Decomposition ──
    {
        "key": "decomp_q1",
        "dimension": "task_decomposition",
        "text": "You need to create a 30-page strategy document using AI. How do you approach it?",
        "options": [
            {"text": "I ask AI to write the whole thing in one go", "score": 1},
            {"text": "I ask for an outline first, then write it section by section", "score": 2},
            {"text": "I break it into sub-tasks — research, structure, draft each section, review — with clear instructions for each", "score": 3},
            {"text": "I use different AI tools for different parts and assemble the final product myself", "score": 4},
        ],
        "display_order": [0, 2, 1, 3],
    },
    {
        "key": "decomp_q2",
        "dimension": "task_decomposition",
        "text": "When AI gives you a poor result on a complex task, what's usually the reason?",
        "options": [
            {"text": "The AI isn't smart enough", "score": 1},
            {"text": "I probably didn't write a good enough prompt", "score": 2},
            {"text": "The task was too big or vague — I should have broken it into smaller pieces", "score": 3},
            {"text": "I need to diagnose whether it's a context issue, a task-scope issue, or a model limitation", "score": 4},
        ],
        "display_order": [3, 0, 2, 1],
    },
    # ── Iterative Refinement ──
    {
        "key": "refine_q1",
        "dimension": "iterative_refinement",
        "text": "AI gives you a decent first draft. What happens next?",
        "options": [
            {"text": "I use it as-is, maybe with minor edits", "score": 1},
            {"text": "I ask AI to improve it (\"make it better\")", "score": 2},
            {"text": "I give specific feedback: adjust the tone here, expand this argument, cut that section", "score": 3},
            {"text": "I treat the first output as raw material and go through structured rounds of refinement", "score": 4},
        ],
        "display_order": [1, 3, 0, 2],
    },
    {
        "key": "refine_q2",
        "dimension": "iterative_refinement",
        "text": "How many rounds of back-and-forth do you typically have with AI on an important task?",
        "options": [
            {"text": "Usually just one — I take what it gives me", "score": 1},
            {"text": "2–3 rounds, I ask it to fix things I don't like", "score": 2},
            {"text": "3–5 rounds with specific, directed feedback each time", "score": 3},
            {"text": "As many as needed — I have a structured refinement process", "score": 4},
        ],
        "display_order": [2, 0, 1, 3],
    },
    # ── Workflow Integration ──
    {
        "key": "workflow_q1",
        "dimension": "workflow_integration",
        "text": "How does AI fit into your daily work right now?",
        "options": [
            {"text": "I use it occasionally when I'm stuck or curious", "score": 1},
            {"text": "I use it regularly for specific tasks like writing or research", "score": 2},
            {"text": "AI is embedded in several of my standard workflows with go-to prompts", "score": 3},
            {"text": "AI is core to how I operate — I've built systematic processes and prompt libraries", "score": 4},
        ],
        "display_order": [0, 2, 3, 1],
    },
    {
        "key": "workflow_q2",
        "dimension": "workflow_integration",
        "text": "If a colleague asked how they should start using AI at work, what would you say?",
        "options": [
            {"text": "\"Just try ChatGPT, it's pretty cool\"", "score": 1},
            {"text": "\"Here are some tasks it's good at — try it for emails and summaries\"", "score": 2},
            {"text": "\"Let me show you how I use it — I've got a process that works\"", "score": 3},
            {"text": "\"Let's map your recurring tasks, figure out which ones AI handles, and build a system\"", "score": 4},
        ],
        "display_order": [3, 1, 0, 2],
    },
    # ── Frontier Recognition ──
    {
        "key": "frontier_q1",
        "dimension": "frontier_recognition",
        "text": "Which of these tasks would you trust AI to do reliably WITHOUT human review?",
        "options": [
            {"text": "All of these — AI is quite capable now", "score": 1},
            {"text": "Writing emails and summarizing documents", "score": 2},
            {"text": "Formatting and restructuring text — but not anything requiring factual accuracy", "score": 3},
            {"text": "It depends on the specific model, the task, and the stakes — I'd test first", "score": 4},
        ],
        "display_order": [2, 0, 1, 3],
    },
    {
        "key": "frontier_q2",
        "dimension": "frontier_recognition",
        "text": "AI technology updates constantly. How do you keep up?",
        "options": [
            {"text": "I don't really follow it — I use what's available", "score": 1},
            {"text": "I read about AI occasionally and try new tools when they come out", "score": 2},
            {"text": "I actively test new models and features to see how they affect my work", "score": 3},
            {"text": "I systematically evaluate new capabilities, document what works, and update my workflows", "score": 4},
        ],
        "display_order": [1, 3, 0, 2],
    },
]

# ─── Countries (curated to Yango Tech markets) ──────────────────────────────
COUNTRIES = [
    # Gulf
    "UAE", "Saudi Arabia", "Qatar", "Bahrain", "Oman", "Kuwait",
    # Africa
    "Ethiopia", "Nigeria", "Kenya", "South Africa", "Mozambique",
    "Ghana", "Tanzania", "Rwanda", "Egypt",
    # LATAM
    "Brazil", "Mexico", "Colombia", "Argentina",
    # CIS / Asia
    "Kazakhstan", "Uzbekistan", "Turkey", "India", "Indonesia",
    # Catch-all
    "Other",
]

# ─── Industries ──────────────────────────────────────────────────────────────
INDUSTRIES = [
    "Banking & Financial Services",
    "Government & Public Sector",
    "Telecommunications",
    "Logistics & Transportation",
    "Retail & E-commerce",
    "Technology & Software",
    "Energy & Utilities",
    "Healthcare",
    "Education",
    "Consulting & Professional Services",
    "Other",
]

# ─── Regional Benchmarks (seeded, approximate) ──────────────────────────────
# Based on Stanford HAI, Oxford Insights, Cisco AI Readiness indices
# Normalized to our 0-100 scale. These are directional, not scientific.
REGIONAL_BENCHMARKS = {
    "Gulf": {"score": 45, "level": "Learner", "countries": ["UAE", "Saudi Arabia", "Qatar", "Bahrain", "Oman", "Kuwait"]},
    "East Africa": {"score": 28, "level": "Learner", "countries": ["Ethiopia", "Kenya", "Tanzania", "Rwanda"]},
    "West Africa": {"score": 25, "level": "Explorer", "countries": ["Nigeria", "Ghana"]},
    "Southern Africa": {"score": 35, "level": "Learner", "countries": ["South Africa", "Mozambique"]},
    "North Africa": {"score": 32, "level": "Learner", "countries": ["Egypt"]},
    "Latin America": {"score": 38, "level": "Learner", "countries": ["Brazil", "Mexico", "Colombia", "Argentina"]},
    "Central Asia": {"score": 30, "level": "Learner", "countries": ["Kazakhstan", "Uzbekistan", "Turkey"]},
    "South & SE Asia": {"score": 42, "level": "Learner", "countries": ["India", "Indonesia"]},
    "Global Average": {"score": 39, "level": "Learner", "countries": []},
}

def get_region_for_country(country: str) -> str | None:
    for region, data in REGIONAL_BENCHMARKS.items():
        if country in data["countries"]:
            return region
    return None
