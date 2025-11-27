"""
AI Content Intelligence Engine - Main Application
Using OpenAI GPT-4 API
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import (
    APP_TITLE, APP_DESCRIPTION, SIDEBAR_PAGES,
    DEFAULT_PERSONAS, FUNNEL_STAGES, OPENAI_API_KEY
)

# Import utilities
from utils.pdf_processor import PDFProcessor
from utils.web_scraper import WebScraper
from utils.persona_manager import PersonaManager
from utils.content_analyzer import ContentAnalyzer
from utils.gap_analyzer import GapAnalyzer
from utils.strategy_generator import StrategyGenerator

# Import components
from components.upload_section import render_upload_section, render_persona_upload
from components.analysis_dashboard import render_analysis_dashboard, render_quick_stats
from components.gap_matrix import render_gap_matrix, render_stage_analysis, render_persona_analysis
from components.persona_chat import render_persona_chat, render_comparison_tool, render_content_advisor
from components.strategy_view import render_strategy_view, render_content_brief_generator

# Page configuration
st.set_page_config(
    page_title="Content Intelligence Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        "personas": [],
        "persona_manager": PersonaManager(),
        "content_analyzer": None,
        "gap_analyzer": None,
        "strategy_generator": StrategyGenerator(),
        "analyzed_content": [],
        "coverage_matrix": {},
        "gaps": [],
        "strategy": {},
        "pending_files": [],
        "pending_urls": [],
        "manual_personas": [],
        "current_page": "home"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    """Render the sidebar navigation"""
    st.sidebar.markdown(f"# {APP_TITLE}")
    st.sidebar.markdown(APP_DESCRIPTION)
    st.sidebar.markdown("---")
    
    # API Key Status
    if OPENAI_API_KEY:
        st.sidebar.success("✅ OpenAI API Connected")
    else:
        st.sidebar.error("❌ API Key Missing")
        st.sidebar.markdown("Add `OPENAI_API_KEY` to .env file")
    
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    
    pages = {
        "🏠 Home": "home",
        "📋 Persona Setup": "persona_setup",
        "🎯 Funnel Configuration": "funnel_config",
        "📥 Content Upload": "content_upload",
        "🔍 Analyze Content": "analyze",
        "📊 Analysis Dashboard": "analysis_dashboard",
        "🔲 Gap Matrix": "gap_matrix",
        "📈 Content Strategy": "content_strategy",
        "💬 Persona Chat": "persona_chat"
    }
    
    for label, page_id in pages.items():
        if st.sidebar.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.current_page = page_id
    
    # Quick stats
    if st.session_state.analyzed_content:
        render_quick_stats(st.session_state.analyzed_content)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Status")
    st.sidebar.markdown(f"📋 Personas: {len(st.session_state.personas)}")
    st.sidebar.markdown(f"📄 Content: {len(st.session_state.analyzed_content)}")
    st.sidebar.markdown(f"🔲 Gaps: {len(st.session_state.gaps)}")


def render_home():
    """Render the home page"""
    st.markdown('<p class="main-header">🧠 AI Content Intelligence Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze, classify, and optimize your content strategy with AI</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Content Audit")
        st.markdown("""
        - Upload blogs, PDFs, URLs
        - Auto-classify by persona & stage
        - Quality scoring & insights
        """)
        if st.button("Start Upload →", key="home_upload"):
            st.session_state.current_page = "content_upload"
            st.rerun()
    
    with col2:
        st.markdown("### 🔲 Gap Analysis")
        st.markdown("""
        - Visual coverage matrix
        - Identify content gaps
        - Prioritized recommendations
        """)
        if st.button("View Gaps →", key="home_gaps"):
            st.session_state.current_page = "gap_matrix"
            st.rerun()
    
    with col3:
        st.markdown("### 💬 Persona Chat")
        st.markdown("""
        - Chat with persona agent
        - Content recommendations
        - Sales prep assistance
        """)
        if st.button("Chat Now →", key="home_chat"):
            st.session_state.current_page = "persona_chat"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🚀 Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Step 1: Upload Persona Research**
        Upload your persona PDFs or add personas manually.
        
        **Step 2: Add Content Assets**
        Upload PDFs, documents, or paste URLs.
        
        **Step 3: Run Analysis**
        Click Analyze to classify all content.
        """)
    
    with col2:
        st.markdown("""
        **Step 4: Review Gap Matrix**
        See visual heatmap of content coverage.
        
        **Step 5: Get Strategy Recommendations**
        AI generates a quarterly content plan.
        
        **Step 6: Use Persona Chat**
        Ask questions about personas.
        """)
    
    if st.session_state.analyzed_content:
        st.markdown("---")
        st.markdown("### 📈 Current Analysis Status")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Personas", len(st.session_state.personas))
        col2.metric("Content Analyzed", len(st.session_state.analyzed_content))
        col3.metric("Gaps Found", len(st.session_state.gaps))
        col4.metric("Strategy Items", len(st.session_state.strategy.get("priority_content_to_create", [])))


def render_persona_setup_page():
    """Render persona setup page"""
    persona_files = render_persona_upload()
    
    if persona_files:
        if st.button("🔍 Extract Personas from Documents", type="primary"):
            with st.spinner("Extracting personas..."):
                pdf_processor = PDFProcessor()
                persona_manager = st.session_state.persona_manager
                
                for file_data in persona_files:
                    file = file_data["file"]
                    text = pdf_processor.extract_text(file)
                    
                    if text:
                        extracted = persona_manager.extract_personas_from_text(
                            text, 
                            source_name=file_data["name"]
                        )
                        persona_manager.add_personas(extracted)
                
                st.session_state.personas = persona_manager.get_all_personas()
                st.success(f"✅ Extracted {len(st.session_state.personas)} personas!")
    
    if st.session_state.manual_personas:
        st.session_state.persona_manager.add_personas(st.session_state.manual_personas)
        st.session_state.personas = st.session_state.persona_manager.get_all_personas()
    
    st.markdown("---")
    if st.button("📋 Use Default Personas"):
        st.session_state.persona_manager.load_default_personas()
        st.session_state.personas = st.session_state.persona_manager.get_all_personas()
        st.success("Loaded default personas!")
        st.rerun()
    
    if st.session_state.personas:
        st.markdown("---")
        st.markdown("### Current Personas")
        for persona in st.session_state.personas:
            with st.expander(f"👤 {persona.get('name', 'Unknown')}"):
                st.json(persona)


def render_funnel_config_page():
    """Render funnel configuration page"""
    st.header("🎯 Funnel Configuration")
    st.markdown("Configure your customer journey stages for content mapping.")
    
    st.markdown("### Current Funnel Stages")
    
    for stage_key, stage_data in FUNNEL_STAGES.items():
        with st.expander(f"📍 {stage_data['name']}", expanded=True):
            st.markdown(f"**Description:** {stage_data['description']}")
            st.markdown(f"**Content Types:** {', '.join(stage_data['content_types'])}")
            st.markdown(f"**Intent Signals:** {', '.join(stage_data['intent_signals'])}")
    
    st.info("💡 Funnel stages are pre-configured. Custom configuration coming soon!")


def render_content_upload_page():
    """Render content upload page"""
    uploaded_files, urls = render_upload_section()
    st.session_state.pending_files = uploaded_files
    st.session_state.pending_urls = urls


def render_analyze_page():
    """Render analysis execution page"""
    st.header("🔍 Analyze Content")
    
    pending_files = st.session_state.get("pending_files", [])
    pending_urls = st.session_state.get("pending_urls", [])
    
    total_items = len(pending_files) + len(pending_urls)
    
    if total_items == 0:
        st.warning("No content to analyze. Please upload files or add URLs first.")
        if st.button("Go to Content Upload"):
            st.session_state.current_page = "content_upload"
            st.rerun()
        return
    
    st.markdown(f"### Ready to Analyze: {total_items} items")
    st.markdown(f"- Files: {len(pending_files)}")
    st.markdown(f"- URLs: {len(pending_urls)}")
    
    personas = st.session_state.personas
    if not personas:
        st.warning("⚠️ No personas loaded. Analysis will use default classification.")
    else:
        st.success(f"✅ {len(personas)} personas loaded for classification")
    
    if st.button("🚀 Run Analysis", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        content_analyzer = ContentAnalyzer(personas)
        gap_analyzer = GapAnalyzer(personas)
        gap_analyzer.set_personas(personas)
        
        pdf_processor = PDFProcessor()
        web_scraper = WebScraper()
        
        all_content = []
        total_steps = total_items
        current_step = 0
        
        # Process files
        for file_data in pending_files:
            current_step += 1
            progress_bar.progress(current_step / total_steps)
            status_text.text(f"Processing: {file_data['name']}")
            
            try:
                text = pdf_processor.extract_text(file_data["file"])
                all_content.append({
                    "title": file_data["name"],
                    "content": text,
                    "source": "upload",
                    "type": file_data.get("type", "document")
                })
            except Exception as e:
                st.error(f"Error processing {file_data['name']}: {e}")
        
        # Process URLs
        for url in pending_urls:
            current_step += 1
            progress_bar.progress(current_step / total_steps)
            status_text.text(f"Fetching: {url[:50]}...")
            
            try:
                extracted = web_scraper.extract_content(url)
                if not extracted.get("error"):
                    all_content.append({
                        "title": extracted.get("title", url),
                        "content": extracted.get("content", ""),
                        "source": url,
                        "type": "web_page"
                    })
                else:
                    st.warning(f"Could not fetch: {url}")
            except Exception as e:
                st.error(f"Error fetching {url}: {e}")
        
        # Run AI analysis
        status_text.text("Running AI analysis...")
        analyzed = content_analyzer.batch_analyze(all_content)
        st.session_state.analyzed_content = analyzed
        st.session_state.content_analyzer = content_analyzer
        
        # Run gap analysis
        status_text.text("Analyzing content gaps...")
        coverage = gap_analyzer.analyze_coverage(analyzed)
        st.session_state.coverage_matrix = coverage
        st.session_state.gaps = gap_analyzer.get_gaps()
        st.session_state.gap_analyzer = gap_analyzer
        
        # Generate strategy
        status_text.text("Generating content strategy...")
        strategy = st.session_state.strategy_generator.generate_strategy(
            gaps=st.session_state.gaps,
            strengths=gap_analyzer.get_strengths(),
            personas=personas,
            analyzed_content=analyzed,
            coverage_matrix=coverage
        )
        st.session_state.strategy = strategy
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        st.success(f"""
        Analysis complete!
        - {len(analyzed)} content pieces analyzed
        - {len(st.session_state.gaps)} gaps identified
        - Strategy recommendations generated
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("View Dashboard"):
                st.session_state.current_page = "analysis_dashboard"
                st.rerun()
        
        with col2:
            if st.button("View Gap Matrix"):
                st.session_state.current_page = "gap_matrix"
                st.rerun()
        
        with col3:
            if st.button("View Strategy"):
                st.session_state.current_page = "content_strategy"
                st.rerun()


def render_analysis_dashboard_page():
    """Render analysis dashboard page"""
    analyzed_content = st.session_state.analyzed_content
    
    if not analyzed_content:
        st.warning("No content analyzed yet. Please run analysis first.")
        return
    
    content_analyzer = st.session_state.content_analyzer
    summary = content_analyzer.get_analysis_summary() if content_analyzer else {}
    render_analysis_dashboard(analyzed_content, summary)


def render_gap_matrix_page():
    """Render gap matrix page"""
    coverage_matrix = st.session_state.coverage_matrix
    gaps = st.session_state.gaps
    gap_analyzer = st.session_state.gap_analyzer
    
    if not coverage_matrix:
        st.warning("No coverage data. Please run analysis first.")
        return
    
    summary = gap_analyzer.get_summary_stats() if gap_analyzer else {}
    render_gap_matrix(coverage_matrix, gaps, summary)
    
    st.markdown("---")
    
    if gap_analyzer:
        tab1, tab2 = st.tabs(["📊 By Stage", "👥 By Persona"])
        with tab1:
            render_stage_analysis(gap_analyzer.get_stage_summary())
        with tab2:
            render_persona_analysis(gap_analyzer.get_persona_summary())


def render_content_strategy_page():
    """Render content strategy page"""
    strategy = st.session_state.strategy
    personas = st.session_state.personas
    
    if not strategy:
        st.warning("No strategy generated. Please run analysis first.")
        return
    
    render_strategy_view(strategy, personas)
    
    st.markdown("---")
    render_content_brief_generator(
        st.session_state.strategy_generator,
        personas,
        st.session_state.analyzed_content
    )


def render_persona_chat_page():
    """Render persona chat page"""
    persona_manager = st.session_state.persona_manager
    
    if st.session_state.personas and not persona_manager.get_all_personas():
        persona_manager.add_personas(st.session_state.personas)
    
    render_persona_chat(persona_manager)
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["⚖️ Compare Personas", "📝 Content Advisor"])
    
    with tab1:
        render_comparison_tool(persona_manager)
    with tab2:
        render_content_advisor(persona_manager)


def main():
    """Main application entry point"""
    initialize_session_state()
    render_sidebar()
    
    page = st.session_state.current_page
    
    if page == "home":
        render_home()
    elif page == "persona_setup":
        render_persona_setup_page()
    elif page == "funnel_config":
        render_funnel_config_page()
    elif page == "content_upload":
        render_content_upload_page()
    elif page == "analyze":
        render_analyze_page()
    elif page == "analysis_dashboard":
        render_analysis_dashboard_page()
    elif page == "gap_matrix":
        render_gap_matrix_page()
    elif page == "content_strategy":
        render_content_strategy_page()
    elif page == "persona_chat":
        render_persona_chat_page()
    else:
        render_home()


if __name__ == "__main__":
    main()
