"""
Configuration settings for AI Content Intelligence Engine
"""

import os
import streamlit as st

# API Configuration - Using OpenAI
# Try Streamlit secrets first, then fall back to environment variable
try:
    OPENAI_API_KEY = st.secrets["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"]
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

MODEL_NAME = "gpt-4o"  # Options: "gpt-4o", "gpt-4o-mini", "gpt-4-turbo"

# Default Personas
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

# Content Types
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
    "strong": 70,
    "moderate": 40,
    "gap": 0
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
