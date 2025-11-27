"""
Analysis Dashboard Component - Displays content analysis results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Dict


def render_analysis_dashboard(analyzed_content: List[Dict], summary: Dict):
    """Render the analysis dashboard with results"""
    st.header("📊 Analysis Dashboard")
    
    if not analyzed_content:
        st.info("No content analyzed yet. Go to Content Upload to add content.")
        return
    
    # Key Metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Content", summary.get("total_content", 0))
    col2.metric("Avg Quality Score", f"{summary.get('average_quality_score', 0)}%")
    col3.metric("Total Words", f"{summary.get('total_word_count', 0):,}")
    col4.metric("Content Types", len(summary.get("by_content_type", {})))
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Content by Funnel Stage")
        stage_data = summary.get("by_funnel_stage", {})
        if stage_data:
            fig = px.pie(
                values=list(stage_data.values()),
                names=[s.title() for s in stage_data.keys()],
                color_discrete_sequence=["#4CAF50", "#FFC107", "#2196F3"],
                hole=0.4
            )
            fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Content by Persona")
        persona_data = summary.get("by_persona", {})
        if persona_data:
            fig = px.bar(
                x=list(persona_data.keys()),
                y=list(persona_data.values()),
                color=list(persona_data.values()),
                color_continuous_scale="Blues"
            )
            fig.update_layout(
                xaxis_title="Persona",
                yaxis_title="Content Count",
                showlegend=False,
                height=300,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Content Table
    st.markdown("### Content Inventory")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stage_filter = st.multiselect(
            "Filter by Stage",
            options=["awareness", "consideration", "decision"],
            default=[]
        )
    
    with col2:
        persona_options = list(summary.get("by_persona", {}).keys())
        persona_filter = st.multiselect("Filter by Persona", options=persona_options, default=[])
    
    with col3:
        quality_filter = st.slider("Min Quality Score", 0, 100, 0)
    
    # Apply filters
    filtered_content = analyzed_content.copy()
    if stage_filter:
        filtered_content = [c for c in filtered_content if c.get("funnel_stage") in stage_filter]
    if persona_filter:
        filtered_content = [c for c in filtered_content if c.get("primary_persona") in persona_filter]
    filtered_content = [c for c in filtered_content if c.get("quality_score", 0) >= quality_filter]
    
    if filtered_content:
        df_data = []
        for content in filtered_content:
            df_data.append({
                "Title": content.get("original_title", "Untitled")[:50],
                "Type": content.get("content_type", "unknown"),
                "Persona": content.get("primary_persona", "Unknown"),
                "Stage": content.get("funnel_stage", "unknown").title(),
                "Quality": content.get("quality_score", 0),
                "Words": content.get("word_count", 0)
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, height=400)
        st.caption(f"Showing {len(filtered_content)} of {len(analyzed_content)} items")
    else:
        st.info("No content matches the current filters")
    
    # Detailed View
    st.markdown("---")
    st.markdown("### Detailed Content Analysis")
    
    content_titles = [c.get("original_title", f"Content {i+1}") for i, c in enumerate(analyzed_content)]
    selected_title = st.selectbox("Select content to view details", content_titles)
    
    if selected_title:
        selected_idx = content_titles.index(selected_title)
        selected_content = analyzed_content[selected_idx]
        _render_content_details(selected_content)


def _render_content_details(content: Dict):
    """Render detailed view of a single content piece"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"#### {content.get('original_title', 'Untitled')}")
        st.markdown(f"**Source:** {content.get('original_source', 'N/A')}")
        st.markdown(f"**Type:** {content.get('content_type', 'Unknown')}")
        
        st.markdown("**Summary:**")
        st.info(content.get("summary", "No summary available"))
        
        key_messages = content.get("key_messages", [])
        if key_messages:
            st.markdown("**Key Messages:**")
            for msg in key_messages:
                st.markdown(f"- {msg}")
    
    with col2:
        st.markdown("#### Scores")
        st.metric("Quality Score", f"{content.get('quality_score', 0)}%")
        st.metric("Classification Confidence", f"{content.get('funnel_confidence', 0)}%")
        st.markdown(f"**Funnel Stage:** {content.get('funnel_stage', 'Unknown').title()}")
        st.markdown(f"**Intent:** {content.get('intent', 'Unknown')}")
        
        persona_scores = content.get("persona_scores", {})
        if persona_scores:
            st.markdown("#### Persona Fit")
            for persona, score in sorted(persona_scores.items(), key=lambda x: x[1], reverse=True):
                st.progress(score / 100, text=f"{persona}: {score}%")
    
    # Improvements
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### ✅ Strengths")
        for s in content.get("strengths", []):
            st.markdown(f"- {s}")
    
    with col2:
        st.markdown("##### 🔧 Improvements")
        for i in content.get("improvements", []):
            st.markdown(f"- {i}")
    
    with col3:
        st.markdown("##### ❌ Missing Elements")
        for m in content.get("missing_elements", []):
            st.markdown(f"- {m}")


def render_quick_stats(analyzed_content: List[Dict]) -> Dict:
    """Render quick stats sidebar widget"""
    if not analyzed_content:
        return {}
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Quick Stats")
    
    total = len(analyzed_content)
    avg_quality = sum(c.get("quality_score", 0) for c in analyzed_content) / total if total else 0
    
    st.sidebar.metric("Content Analyzed", total)
    st.sidebar.metric("Avg Quality", f"{avg_quality:.0f}%")
    
    return {"total": total, "avg_quality": avg_quality}
