"""
Analysis Dashboard Component - Displays content analysis results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict


def render_analysis_dashboard(analyzed_content: List[Dict], summary: Dict):
    """
    Render the analysis dashboard with results
    
    Args:
        analyzed_content: List of analyzed content items
        summary: Summary statistics
    """
    st.header("📊 Analysis Dashboard")
    
    if not analyzed_content:
        st.info("No content analyzed yet. Go to Content Upload to add content.")
        return
    
    # Key Metrics Row
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        "Total Content",
        summary.get("total_content", 0),
        help="Total number of content pieces analyzed"
    )
    col2.metric(
        "Avg Quality Score",
        f"{summary.get('average_quality_score', 0)}%",
        help="Average quality score across all content"
    )
    col3.metric(
        "Total Words",
        f"{summary.get('total_word_count', 0):,}",
        help="Total word count across all content"
    )
    col4.metric(
        "Content Types",
        len(summary.get("by_content_type", {})),
        help="Number of different content types"
    )
    
    st.markdown("---")
    
    # Charts Row
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
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                margin=dict(t=20, b=20, l=20, r=20),
                height=300
            )
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
                margin=dict(t=20, b=20, l=20, r=20),
                height=300
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Content Type Distribution
    st.markdown("### Content Type Distribution")
    type_data = summary.get("by_content_type", {})
    
    if type_data:
        fig = px.bar(
            x=list(type_data.keys()),
            y=list(type_data.values()),
            color=list(type_data.keys()),
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            xaxis_title="Content Type",
            yaxis_title="Count",
            showlegend=False,
            margin=dict(t=20, b=40, l=20, r=20),
            height=300
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Content Table
    st.markdown("### Content Inventory")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stage_filter = st.multiselect(
            "Filter by Stage",
            options=["awareness", "consideration", "decision"],
            default=[],
            key="stage_filter"
        )
    
    with col2:
        persona_options = list(summary.get("by_persona", {}).keys())
        persona_filter = st.multiselect(
            "Filter by Persona",
            options=persona_options,
            default=[],
            key="persona_filter"
        )
    
    with col3:
        quality_filter = st.slider(
            "Min Quality Score",
            min_value=0,
            max_value=100,
            value=0,
            key="quality_filter"
        )
    
    # Apply filters
    filtered_content = analyzed_content.copy()
    
    if stage_filter:
        filtered_content = [c for c in filtered_content if c.get("funnel_stage") in stage_filter]
    
    if persona_filter:
        filtered_content = [c for c in filtered_content if c.get("primary_persona") in persona_filter]
    
    filtered_content = [c for c in filtered_content if c.get("quality_score", 0) >= quality_filter]
    
    # Display as dataframe
    if filtered_content:
        df_data = []
        for content in filtered_content:
            df_data.append({
                "Title": content.get("original_title", "Untitled")[:50],
                "Type": content.get("content_type", "unknown"),
                "Persona": content.get("primary_persona", "Unknown"),
                "Stage": content.get("funnel_stage", "unknown").title(),
                "Intent": content.get("intent", "unknown"),
                "Quality": f"{content.get('quality_score', 0)}%",
                "Words": content.get("word_count", 0)
            })
        
        df = pd.DataFrame(df_data)
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            height=400,
            column_config={
                "Quality": st.column_config.ProgressColumn(
                    "Quality",
                    format="%d%%",
                    min_value=0,
                    max_value=100
                )
            }
        )
        
        st.caption(f"Showing {len(filtered_content)} of {len(analyzed_content)} items")
    else:
        st.info("No content matches the current filters")
    
    # Detailed View
    st.markdown("---")
    st.markdown("### Detailed Content Analysis")
    
    # Select content for detailed view
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
        
        # Key Messages
        key_messages = content.get("key_messages", [])
        if key_messages:
            st.markdown("**Key Messages:**")
            for msg in key_messages:
                st.markdown(f"- {msg}")
        
        # Topics
        topics = content.get("topics", [])
        if topics:
            st.markdown("**Topics:**")
            st.markdown(" · ".join([f"`{t}`" for t in topics]))
    
    with col2:
        # Scores
        st.markdown("#### Scores")
        
        quality = content.get("quality_score", 0)
        st.metric("Quality Score", f"{quality}%")
        
        confidence = content.get("funnel_confidence", 0)
        st.metric("Classification Confidence", f"{confidence}%")
        
        st.markdown(f"**Funnel Stage:** {content.get('funnel_stage', 'Unknown').title()}")
        st.markdown(f"**Intent:** {content.get('intent', 'Unknown')}")
        st.markdown(f"**Tone:** {content.get('tone', 'Unknown')}")
        
        # Persona Scores
        persona_scores = content.get("persona_scores", {})
        if persona_scores:
            st.markdown("#### Persona Fit")
            for persona, score in sorted(persona_scores.items(), key=lambda x: x[1], reverse=True):
                st.progress(score / 100, text=f"{persona}: {score}%")
    
    # Improvements Section
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### ✅ Strengths")
        strengths = content.get("strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(f"- {s}")
        else:
            st.markdown("*No specific strengths identified*")
    
    with col2:
        st.markdown("##### 🔧 Improvements")
        improvements = content.get("improvements", [])
        if improvements:
            for i in improvements:
                st.markdown(f"- {i}")
        else:
            st.markdown("*No improvements suggested*")
    
    with col3:
        st.markdown("##### ❌ Missing Elements")
        missing = content.get("missing_elements", [])
        if missing:
            for m in missing:
                st.markdown(f"- {m}")
        else:
            st.markdown("*No missing elements identified*")


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
    
    # Stage distribution
    stages = {}
    for c in analyzed_content:
        stage = c.get("funnel_stage", "unknown")
        stages[stage] = stages.get(stage, 0) + 1
    
    st.sidebar.markdown("**By Stage:**")
    for stage, count in stages.items():
        st.sidebar.markdown(f"- {stage.title()}: {count}")
    
    return {
        "total": total,
        "avg_quality": avg_quality,
        "by_stage": stages
    }
