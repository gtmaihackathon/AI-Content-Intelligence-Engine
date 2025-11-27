"""
Upload Section Component - Handles file and URL uploads
"""

import streamlit as st
from typing import List, Dict, Tuple
import validators


def render_upload_section() -> Tuple[List[Dict], List[str]]:
    """Render the content upload section"""
    st.header("📥 Content Upload")
    st.markdown("Upload your content assets for analysis. Supports PDFs, documents, and URLs.")
    
    uploaded_files = []
    urls = []
    
    tab1, tab2, tab3 = st.tabs(["📄 Upload Files", "🔗 Add URLs", "📋 Batch Import"])
    
    with tab1:
        st.markdown("### Upload Documents")
        st.markdown("Supported formats: PDF, TXT, MD, DOCX")
        
        files = st.file_uploader(
            "Drop files here",
            type=["pdf", "txt", "md", "docx"],
            accept_multiple_files=True,
            key="content_files"
        )
        
        if files:
            for file in files:
                file_type = _detect_content_type(file.name)
                uploaded_files.append({
                    "file": file,
                    "name": file.name,
                    "type": file_type,
                    "source": "upload"
                })
            
            st.success(f"✅ {len(files)} file(s) ready for analysis")
            
            with st.expander("View uploaded files"):
                for f in files:
                    st.markdown(f"- **{f.name}** ({f.type}, {f.size/1024:.1f} KB)")
    
    with tab2:
        st.markdown("### Add Website URLs")
        st.markdown("Enter blog posts, landing pages, or any web content URLs")
        
        single_url = st.text_input(
            "Enter URL",
            placeholder="https://example.com/blog/article-title",
            key="single_url"
        )
        
        if single_url:
            if validators.url(single_url):
                urls.append(single_url)
                st.success("✅ URL added")
            else:
                st.error("❌ Invalid URL format")
        
        st.markdown("---")
        st.markdown("**Or paste multiple URLs (one per line):**")
        
        multi_urls = st.text_area(
            "Multiple URLs",
            placeholder="https://example.com/blog/post-1\nhttps://example.com/blog/post-2",
            height=150,
            key="multi_urls",
            label_visibility="collapsed"
        )
        
        if multi_urls:
            url_list = [u.strip() for u in multi_urls.split("\n") if u.strip()]
            valid_urls = [u for u in url_list if validators.url(u)]
            invalid_count = len(url_list) - len(valid_urls)
            
            urls.extend(valid_urls)
            
            if valid_urls:
                st.success(f"✅ {len(valid_urls)} valid URL(s) added")
            if invalid_count > 0:
                st.warning(f"⚠️ {invalid_count} invalid URL(s) skipped")
    
    with tab3:
        st.markdown("### Batch Import")
        st.markdown("Upload a CSV or TXT file with URLs")
        
        batch_file = st.file_uploader(
            "Upload batch file",
            type=["csv", "txt"],
            key="batch_file"
        )
        
        if batch_file:
            content = batch_file.read().decode("utf-8")
            lines = [l.strip() for l in content.split("\n") if l.strip()]
            batch_urls = [l for l in lines if validators.url(l)]
            urls.extend(batch_urls)
            st.success(f"✅ Found {len(batch_urls)} URL(s) in batch file")
    
    # Summary
    st.markdown("---")
    total_items = len(uploaded_files) + len(urls)
    
    if total_items > 0:
        st.markdown(f"### Ready to Analyze: {total_items} item(s)")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Files", len(uploaded_files))
        col2.metric("URLs", len(urls))
        col3.metric("Total", total_items)
        
        st.session_state["pending_files"] = uploaded_files
        st.session_state["pending_urls"] = list(set(urls))
    else:
        st.info("📌 Upload files or add URLs above to begin analysis")
    
    return uploaded_files, urls


def _detect_content_type(filename: str) -> str:
    """Detect content type from filename"""
    filename_lower = filename.lower()
    
    if "case" in filename_lower and "study" in filename_lower:
        return "case_study"
    elif "whitepaper" in filename_lower:
        return "whitepaper"
    elif "ebook" in filename_lower:
        return "ebook"
    elif "deck" in filename_lower or "presentation" in filename_lower:
        return "sales_deck"
    elif "email" in filename_lower:
        return "email_template"
    elif filename_lower.endswith(".pdf"):
        return "document"
    else:
        return "unknown"


def render_persona_upload() -> List[Dict]:
    """Render persona research upload section"""
    st.header("📋 Persona Setup")
    st.markdown("Upload your persona research documents to enable persona-based analysis.")
    
    persona_files = []
    
    files = st.file_uploader(
        "Upload persona research (PDF, TXT, DOCX)",
        type=["pdf", "txt", "docx", "md"],
        accept_multiple_files=True,
        key="persona_files"
    )
    
    if files:
        for file in files:
            persona_files.append({
                "file": file,
                "name": file.name
            })
        st.success(f"✅ {len(files)} persona document(s) uploaded")
    
    # Manual persona entry
    st.markdown("---")
    st.markdown("### Or Add Personas Manually")
    
    with st.expander("Add a persona manually"):
        col1, col2 = st.columns(2)
        
        with col1:
            persona_name = st.text_input("Persona Name", placeholder="e.g., CMO Sarah")
            persona_role = st.text_input("Role/Title", placeholder="e.g., Chief Marketing Officer")
            persona_desc = st.text_area("Description", placeholder="Brief description")
        
        with col2:
            pain_points = st.text_area("Pain Points (one per line)", placeholder="Proving ROI\nScaling operations")
            goals = st.text_area("Goals (one per line)", placeholder="Drive growth\nBuild awareness")
        
        if st.button("Add Persona", key="add_manual_persona"):
            if persona_name:
                manual_persona = {
                    "name": persona_name,
                    "role": persona_role,
                    "description": persona_desc,
                    "pain_points": [p.strip() for p in pain_points.split("\n") if p.strip()],
                    "goals": [g.strip() for g in goals.split("\n") if g.strip()]
                }
                
                if "manual_personas" not in st.session_state:
                    st.session_state["manual_personas"] = []
                st.session_state["manual_personas"].append(manual_persona)
                st.success(f"✅ Added persona: {persona_name}")
            else:
                st.error("Please enter a persona name")
    
    # Show current personas
    if "manual_personas" in st.session_state and st.session_state["manual_personas"]:
        st.markdown("### Current Manual Personas")
        for i, persona in enumerate(st.session_state["manual_personas"]):
            with st.expander(f"📌 {persona['name']}"):
                st.markdown(f"**Role:** {persona.get('role', 'N/A')}")
                st.markdown(f"**Description:** {persona.get('description', 'N/A')}")
                if st.button(f"Remove", key=f"remove_persona_{i}"):
                    st.session_state["manual_personas"].pop(i)
                    st.rerun()
    
    return persona_files
