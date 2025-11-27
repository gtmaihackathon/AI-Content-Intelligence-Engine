"""
Strategy View Component - Displays content strategy recommendations
"""

import streamlit as st
import pandas as pd
from typing import Dict, List
import json


def render_strategy_view(strategy: Dict, personas: List[Dict]):
    """Render the content strategy recommendations view"""
    st.header("📈 Content Strategy Recommendations")
    
    if not strategy:
        st.info("No strategy generated yet. Please analyze content first.")
        return
    
    # Executive Summary
    st.markdown("### 📋 Executive Summary")
    st.info(strategy.get("executive_summary", "No summary available"))
    
    st.markdown("---")
    
    # Quick Wins
    quick_wins = strategy.get("quick_wins", [])
    if quick_wins:
        st.markdown("### ⚡ Quick Wins")
        for win in quick_wins:
            st.markdown(f"- ✅ {win}")
    
    st.markdown("---")
    
    # Priority Content
    st.markdown("### 🎯 Priority Content to Create")
    _render_priority_content(strategy.get("priority_content_to_create", []))
    
    st.markdown("---")
    
    # Quarterly Calendar
    st.markdown("### 📅 Quarterly Content Calendar")
    _render_quarterly_calendar(strategy.get("quarterly_calendar", {}))
    
    st.markdown("---")
    
    # Persona Recommendations
    st.markdown("### 👥 Persona-Specific Recommendations")
    _render_persona_recommendations(strategy.get("persona_specific_recommendations", {}))
    
    st.markdown("---")
    
    # Metrics
    st.markdown("### 📊 Metrics to Track")
    _render_metrics(strategy.get("metrics_to_track", []))
    
    # Export
    st.markdown("---")
    st.markdown("### 📤 Export Strategy")
    _render_export_options(strategy)


def _render_priority_content(content_list: List[Dict]):
    """Render priority content recommendations"""
    if not content_list:
        st.info("No priority content recommendations available")
        return
    
    high_priority = [c for c in content_list if c.get("priority") == "high"]
    medium_priority = [c for c in content_list if c.get("priority") == "medium"]
    low_priority = [c for c in content_list if c.get("priority") == "low"]
    
    tab1, tab2, tab3 = st.tabs([
        f"🔴 High Priority ({len(high_priority)})",
        f"🟠 Medium Priority ({len(medium_priority)})",
        f"🟢 Low Priority ({len(low_priority)})"
    ])
    
    with tab1:
        _render_content_cards(high_priority)
    with tab2:
        _render_content_cards(medium_priority)
    with tab3:
        _render_content_cards(low_priority)


def _render_content_cards(content_list: List[Dict]):
    """Render content recommendation cards"""
    if not content_list:
        st.info("No content in this priority level")
        return
    
    for content in content_list:
        with st.expander(f"📄 {content.get('title', 'Untitled')}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Type:** {content.get('type', 'Unknown')}")
                st.markdown(f"**Target Persona:** {content.get('target_persona', 'Unknown')}")
                st.markdown(f"**Funnel Stage:** {content.get('funnel_stage', 'Unknown').title()}")
                st.markdown(f"**Effort:** {content.get('estimated_effort', 'Unknown')}")
                st.markdown("**Rationale:**")
                st.markdown(content.get('rationale', 'N/A'))
            
            with col2:
                st.markdown("**Key Topics:**")
                for topic in content.get('key_topics', []):
                    st.markdown(f"- {topic}")
                st.markdown("**Suggested Angle:**")
                st.markdown(content.get('suggested_angle', 'N/A'))


def _render_quarterly_calendar(calendar: Dict):
    """Render quarterly content calendar"""
    if not calendar:
        st.info("No calendar data available")
        return
    
    months = list(calendar.keys())
    if not months:
        st.info("Calendar not populated")
        return
    
    tabs = st.tabs([m.replace("_", " ").title() for m in months])
    
    for i, month in enumerate(months):
        with tabs[i]:
            month_content = calendar.get(month, [])
            if not month_content:
                st.info(f"No content planned for {month}")
                continue
            
            df_data = []
            for item in month_content:
                df_data.append({
                    "Week": item.get("week", "TBD"),
                    "Content": item.get("content_title", "TBD"),
                    "Type": item.get("content_type", "TBD"),
                    "Persona": item.get("target_persona", "TBD")
                })
            
            if df_data:
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)


def _render_persona_recommendations(recommendations: Dict):
    """Render persona-specific recommendations"""
    if not recommendations:
        st.info("No persona-specific recommendations available")
        return
    
    for persona_name, rec in recommendations.items():
        with st.expander(f"👤 {persona_name}"):
            st.markdown("**Key Insight:**")
            st.info(rec.get("key_insight", "N/A"))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Content Priorities:**")
                for p in rec.get("content_priorities", []):
                    st.markdown(f"- {p}")
            
            with col2:
                st.markdown("**Messaging Themes:**")
                for t in rec.get("messaging_themes", []):
                    st.markdown(f"- {t}")


def _render_metrics(metrics: List[Dict]):
    """Render metrics to track"""
    if not metrics:
        st.info("No metrics defined")
        return
    
    cols = st.columns(min(3, len(metrics)))
    
    for i, metric in enumerate(metrics):
        col_idx = i % len(cols)
        with cols[col_idx]:
            st.markdown(f"**📊 {metric.get('metric', 'Metric')}**")
            st.markdown(f"*Why:* {metric.get('why', 'N/A')}")
            st.markdown(f"*Target:* `{metric.get('target', 'TBD')}`")


def _render_export_options(strategy: Dict):
    """Render export options for strategy"""
    col1, col2 = st.columns(2)
    
    with col1:
        strategy_json = json.dumps(strategy, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=strategy_json,
            file_name="content_strategy.json",
            mime="application/json"
        )
    
    with col2:
        summary_text = _generate_text_summary(strategy)
        st.download_button(
            label="📥 Download Summary",
            data=summary_text,
            file_name="content_strategy_summary.txt",
            mime="text/plain"
        )


def _generate_text_summary(strategy: Dict) -> str:
    """Generate text summary of strategy"""
    lines = [
        "CONTENT STRATEGY SUMMARY",
        "=" * 50,
        "",
        "EXECUTIVE SUMMARY",
        "-" * 30,
        strategy.get("executive_summary", "N/A"),
        "",
        "QUICK WINS",
        "-" * 30,
    ]
    
    for win in strategy.get("quick_wins", []):
        lines.append(f"• {win}")
    
    lines.extend([
        "",
        "PRIORITY CONTENT TO CREATE",
        "-" * 30,
    ])
    
    for content in strategy.get("priority_content_to_create", []):
        lines.append(f"• [{content.get('priority', 'N/A').upper()}] {content.get('title', 'Untitled')}")
        lines.append(f"  Type: {content.get('type', 'N/A')} | Persona: {content.get('target_persona', 'N/A')}")
    
    return "\n".join(lines)


def render_content_brief_generator(strategy_generator, personas: List[Dict], analyzed_content: List[Dict]):
    """Render content brief generator"""
    st.markdown("### 📝 Generate Content Brief")
    
    content_titles = ["Custom..."]
    strategy = st.session_state.get("strategy", {})
    content_list = strategy.get("priority_content_to_create", [])
    content_titles += [c.get("title", "Untitled") for c in content_list]
    
    selected = st.selectbox("Select content to brief", content_titles)
    
    if selected == "Custom...":
        custom_title = st.text_input("Enter content title")
        content_type = st.selectbox("Content type", ["blog_post", "case_study", "whitepaper", "video"])
        content_rec = {"title": custom_title, "type": content_type}
    else:
        content_rec = next((c for c in content_list if c.get("title") == selected), {})
    
    persona_names = [p.get("name", "Unknown") for p in personas]
    selected_persona_name = st.selectbox("Target persona", persona_names)
    selected_persona = next((p for p in personas if p.get("name") == selected_persona_name), {})
    
    if st.button("Generate Brief"):
        with st.spinner("Generating content brief..."):
            brief = strategy_generator.generate_content_brief(
                content_rec,
                selected_persona,
                analyzed_content
            )
        
        st.markdown("### Generated Brief")
        st.markdown(brief)
        
        st.download_button(
            label="📥 Download Brief",
            data=brief,
            file_name=f"content_brief_{selected_persona_name.lower().replace(' ', '_')}.md",
            mime="text/markdown"
        )
