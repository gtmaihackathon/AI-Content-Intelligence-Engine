
"""
Gap Matrix Component - Visualizes content coverage gaps
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import pandas as pd
from config import FUNNEL_STAGES


def render_gap_matrix(coverage_matrix: Dict, gaps: List[Dict], summary: Dict):
    """Render the gap matrix visualization"""
    st.header("🔲 Content Gap Matrix")
    
    if not coverage_matrix:
        st.info("No coverage data available. Please analyze content first.")
        return
    
    # Summary Stats
    st.markdown("### Coverage Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Cells", summary.get("total_cells", 0))
    col2.metric("Gaps Identified", summary.get("gap_count", 0), delta=f"-{summary.get('gap_percentage', 0)}%", delta_color="inverse")
    col3.metric("Strong Coverage", summary.get("strong_count", 0))
    col4.metric("Coverage Rate", f"{summary.get('coverage_percentage', 0)}%")
    
    st.markdown("---")
    
    # Heatmap
    st.markdown("### Coverage Heatmap")
    st.markdown("*Darker = More content coverage | Hover for details*")
    _render_heatmap(coverage_matrix)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 Priority Gaps")
        _render_gap_list(gaps)
    
    with col2:
        st.markdown("### Gap Priority Chart")
        _render_gap_priority_chart(gaps)
    
    st.markdown("---")
    
    st.markdown("### Detailed Matrix")
    _render_detailed_matrix(coverage_matrix)


def _render_heatmap(coverage_matrix: Dict):
    """Render the main heatmap visualization"""
    personas = list(coverage_matrix.keys())
    stages = ["awareness", "consideration", "decision"]
    stage_labels = ["Awareness", "Consideration", "Decision"]
    
    z_data = []
    hover_text = []
    
    for persona in personas:
        row = []
        hover_row = []
        for stage in stages:
            cell = coverage_matrix[persona].get(stage, {})
            score = cell.get("coverage_score", 0)
            count = cell.get("content_count", 0)
            status = cell.get("status", "gap")
            
            row.append(score)
            hover_row.append(
                f"<b>{persona}</b><br>"
                f"Stage: {stage.title()}<br>"
                f"Score: {score}%<br>"
                f"Content: {count} items<br>"
                f"Status: {status.upper()}"
            )
        z_data.append(row)
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=stage_labels,
        y=personas,
        hovertext=hover_text,
        hoverinfo="text",
        colorscale=[
            [0, "#ffebee"],
            [0.4, "#fff3e0"],
            [0.7, "#e8f5e9"],
            [1, "#2e7d32"]
        ],
        showscale=True,
        colorbar=dict(title="Coverage %", ticksuffix="%")
    ))
    
    for i, persona in enumerate(personas):
        for j, stage in enumerate(stages):
            cell = coverage_matrix[persona].get(stage, {})
            score = cell.get("coverage_score", 0)
            status = cell.get("status", "gap")
            
            icon = "✅" if status == "strong" else "⚠️" if status == "moderate" else "❌"
            
            fig.add_annotation(
                x=stage_labels[j],
                y=persona,
                text=f"{icon}<br>{score}%",
                showarrow=False,
                font=dict(size=12, color="black")
            )
    
    fig.update_layout(
        xaxis=dict(side="top"),
        yaxis=dict(autorange="reversed"),
        height=max(300, len(personas) * 80),
        margin=dict(t=60, b=20, l=150, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_gap_list(gaps: List[Dict]):
    """Render prioritized list of gaps"""
    if not gaps:
        st.success("🎉 No significant gaps found!")
        return
    
    for gap in gaps[:10]:
        priority = gap.get("priority", 0)
        color = "🔴" if priority >= 80 else "🟠" if priority >= 60 else "🟡"
        
        with st.expander(f"{color} {gap['persona']} - {gap['stage_name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Priority Score", f"{priority}/100")
            with col2:
                st.metric("Current Coverage", f"{gap.get('coverage_score', 0)}%")
            
            st.markdown("**Recommended Actions:**")
            stage = gap.get("stage")
            if stage == "awareness":
                st.markdown("- Create educational blog posts\n- Develop thought leadership content")
            elif stage == "consideration":
                st.markdown("- Write comparison guides\n- Create how-to content")
            else:
                st.markdown("- Gather customer testimonials\n- Create case studies")


def _render_gap_priority_chart(gaps: List[Dict]):
    """Render gap priority visualization"""
    if not gaps:
        st.info("No gaps to display")
        return
    
    df = pd.DataFrame(gaps[:10])
    df["label"] = df["persona"] + " - " + df["stage_name"]
    
    fig = px.bar(
        df,
        x="priority",
        y="label",
        orientation="h",
        color="priority",
        color_continuous_scale="Reds"
    )
    
    fig.update_layout(
        xaxis_title="Priority Score",
        yaxis_title="",
        showlegend=False,
        height=400,
        margin=dict(l=10, r=10, t=10, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_detailed_matrix(coverage_matrix: Dict):
    """Render detailed matrix table"""
    personas = list(coverage_matrix.keys())
    stages = ["awareness", "consideration", "decision"]
    
    table_data = []
    for persona in personas:
        row = {"Persona": persona}
        for stage in stages:
            cell = coverage_matrix[persona].get(stage, {})
            score = cell.get("coverage_score", 0)
            count = cell.get("content_count", 0)
            status = cell.get("status", "gap")
            
            icon = "✅" if status == "strong" else "⚠️" if status == "moderate" else "❌"
            row[stage.title()] = f"{icon} {score}% ({count} items)"
        table_data.append(row)
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("✅ Strong (≥70%) | ⚠️ Moderate (40-69%) | ❌ Gap (<40%)")


def render_stage_analysis(stage_summary: Dict):
    """Render analysis by funnel stage"""
    st.markdown("### Analysis by Funnel Stage")
    
    cols = st.columns(3)
    stage_order = ["awareness", "consideration", "decision"]
    stage_icons = {"awareness": "🔍", "consideration": "🤔", "decision": "✅"}
    
    for i, stage in enumerate(stage_order):
        data = stage_summary.get(stage, {})
        with cols[i]:
            st.markdown(f"#### {stage_icons[stage]} {stage.title()}")
            st.metric("Total Content", int(data.get("total_content", 0)))
            st.metric("Avg Coverage", f"{data.get('avg_coverage', 0)}%")
            
            gaps_list = data.get("personas_with_gaps", [])
            if gaps_list:
                st.markdown("**Gaps for:**")
                for p in gaps_list:
                    st.markdown(f"- {p}")
            else:
                st.success("No gaps!")


def render_persona_analysis(persona_summary: Dict):
    """Render analysis by persona"""
    st.markdown("### Analysis by Persona")
    
    for persona_name, data in persona_summary.items():
        with st.expander(f"📌 {persona_name}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Content", int(data.get("total_content", 0)))
            with col2:
                st.metric("Avg Coverage", f"{data.get('avg_coverage', 0)}%")
            with col3:
                strongest = data.get("strongest_stage", "N/A")
                st.metric("Strongest Stage", strongest.title() if strongest else "N/A")
            
            gaps = data.get("stages_with_gaps", [])
            if gaps:
                st.warning(f"**Gaps at:** {', '.join([s.title() for s in gaps])}")
            else:
                st.success("Full coverage across all stages!")
