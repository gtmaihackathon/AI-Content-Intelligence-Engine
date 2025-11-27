"""
Configuration settings for AI Content Intelligence Engine
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_NAME = "claude-sonnet-4-20250514"

# Default Personas (can be overridden by user uploads)
DEFAULT_PERSONAS = [
    {
        "name": "CMO / VP Marketing",
        "description": "Senior marketing leader focused on strategy and ROI",
        "pain_points": ["Proving marketing ROI", "Scaling content operations", "Alignment with sales"],
        "goals": ["Drive revenue growth", "Build brand awareness", "Improve marketing efficiency"]
    },
    {
        "name": "Content Manager",
        "description": "Hands-on content creator and strategist",
        "pain_points": ["Content production speed", "Maintaining quality", "Measuring content performance"],
        "goals": ["Create engaging content", "Improve SEO rankings", "Support sales team"]
    },
    {
        "name": "Sales Leader",
        "description": "VP Sales or Sales Director focused on closing deals",
        "pain_points": ["Finding relevant content for prospects", "Competitive differentiation", "Shortening sales cycles"],
        "goals": ["Hit revenue targets", "Enable sales team", "Improve win rates"]
    }
]

# Funnel Stages Configuration
FUNNEL_STAGES = {
    "awareness": {
        "name": "Awareness",
        "description": "Top of funnel - Problem recognition and education",
        "content_types": ["blog_post", "social_media", "infographic", "video", "podcast"],
        "intent_signals": ["educational", "informational", "thought_leadership"]
    },
    "consideration": {
        "name": "Consideration", 
        "description": "Middle of funnel - Solution evaluation and comparison",
        "content_types": ["whitepaper", "ebook", "webinar", "comparison_guide", "how_to"],
        "intent_signals": ["evaluative", "comparative", "solution_focused"]
    },
    "decision": {
        "name": "Decision",
        "description": "Bottom of funnel - Purchase decision and validation",
        "content_types": ["case_study", "testimonial", "product_demo", "pricing", "roi_calculator"],
        "intent_signals": ["transactional", "proof_seeking", "validation"]
    }
}

# Content Types with Metadata
CONTENT_TYPES = {
    "blog_post": {"icon": "📝", "typical_stage": "awareness"},
    "case_study": {"icon": "📊", "typical_stage": "decision"},
    "whitepaper": {"icon": "📄", "typical_stage": "consideration"},
    "ebook": {"icon": "📚", "typical_stage": "consideration"},
    "webinar": {"icon": "🎥", "typical_stage": "consideration"},
    "video": {"icon": "▶️", "typical_stage": "awareness"},
    "infographic": {"icon": "📈", "typical_stage": "awareness"},
    "email_template": {"icon": "📧", "typical_stage": "all"},
    "sales_deck": {"icon": "📑", "typical_stage": "decision"},
    "product_sheet": {"icon": "📋", "typical_stage": "decision"},
    "comparison_guide": {"icon": "⚖️", "typical_stage": "consideration"},
    "testimonial": {"icon": "💬", "typical_stage": "decision"},
    "landing_page": {"icon": "🌐", "typical_stage": "all"}
}

# Analysis Thresholds
SCORING_THRESHOLDS = {
    "strong": 70,      # >= 70% = strong coverage
    "moderate": 40,    # >= 40% = moderate coverage
    "gap": 0           # < 40% = gap identified
}

# UI Configuration
APP_TITLE = "🧠 AI Content Intelligence Engine"
APP_DESCRIPTION = "Analyze, classify, and optimize your content strategy"

SIDEBAR_PAGES = [
    ("📋 Persona Setup", "persona_setup"),
    ("🎯 Funnel Configuration", "funnel_config"),
    ("📥 Content Upload", "content_upload"),
    ("📊 Analysis Dashboard", "analysis_dashboard"),
    ("🔲 Gap Matrix", "gap_matrix"),
    ("📈 Content Strategy", "content_strategy"),
    ("💬 Persona Chat", "persona_chat")
]

# Export all config
__all__ = [
    "ANTHROPIC_API_KEY",
    "MODEL_NAME",
    "DEFAULT_PERSONAS",
    "FUNNEL_STAGES",
    "CONTENT_TYPES",
    "SCORING_THRESHOLDS",
    "APP_TITLE",
    "APP_DESCRIPTION",
    "SIDEBAR_PAGES"
]
