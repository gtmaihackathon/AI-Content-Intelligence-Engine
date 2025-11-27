"""
Persona Chat Component - Interactive chat with persona knowledge
"""

import streamlit as st
from typing import List, Dict


def render_persona_chat(persona_manager):
    """
    Render the persona chat interface
    
    Args:
        persona_manager: PersonaManager instance with loaded personas
    """
    st.header("💬 Persona Chat Agent")
    st.markdown("Ask questions about your personas to help create content or prepare for calls.")
    
    # Check if personas are loaded
    personas = persona_manager.get_all_personas()
    
    if not personas:
        st.warning("⚠️ No personas loaded. Please upload persona research first.")
        st.markdown("Go to **📋 Persona Setup** to add personas.")
        return
    
    # Show loaded personas
    with st.expander("📋 Loaded Personas", expanded=False):
        for persona in personas:
            st.markdown(f"**{persona.get('name', 'Unknown')}**")
            st.markdown(f"- Role: {persona.get('role', 'N/A')}")
            st.markdown(f"- Pain points: {', '.join(persona.get('pain_points', [])[:3])}")
            st.markdown("---")
    
    # Chat interface
    st.markdown("### Ask About Your Personas")
    
    # Initialize chat history
    if "persona_chat_history" not in st.session_state:
        st.session_state.persona_chat_history = []
    
    # Quick question buttons
    st.markdown("**Quick Questions:**")
    col1, col2 = st.columns(2)
    
    quick_questions = [
        "What are the main pain points for each persona?",
        "How do the personas differ in their buying process?",
        "What content types work best for each persona?",
        "What objections might each persona have?"
    ]
    
    with col1:
        if st.button(quick_questions[0], key="q1", use_container_width=True):
            _process_question(quick_questions[0], persona_manager)
        if st.button(quick_questions[1], key="q2", use_container_width=True):
            _process_question(quick_questions[1], persona_manager)
    
    with col2:
        if st.button(quick_questions[2], key="q3", use_container_width=True):
            _process_question(quick_questions[2], persona_manager)
        if st.button(quick_questions[3], key="q4", use_container_width=True):
            _process_question(quick_questions[3], persona_manager)
    
    st.markdown("---")
    
    # Chat history display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.persona_chat_history:
            if message["role"] == "user":
                st.markdown(f"**🧑 You:** {message['content']}")
            else:
                st.markdown(f"**🤖 Assistant:** {message['content']}")
            st.markdown("---")
    
    # Chat input
    user_input = st.chat_input("Ask about your personas...")
    
    if user_input:
        _process_question(user_input, persona_manager)
        st.rerun()
    
    # Clear chat button
    if st.session_state.persona_chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.persona_chat_history = []
            st.rerun()
    
    # Use case examples
    st.markdown("---")
    st.markdown("### 💡 Example Use Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Content Creation:**
        - "What topics would resonate with [persona]?"
        - "How should I position [topic] for [persona]?"
        - "What format would work best for [persona] at awareness stage?"
        """)
    
    with col2:
        st.markdown("""
        **Sales Prep:**
        - "I'm meeting with a [persona title]. What should I focus on?"
        - "What objections might [persona] raise?"
        - "How do I differentiate for [persona]?"
        """)


def _process_question(question: str, persona_manager):
    """Process a question and get AI response"""
    # Add user question to history
    st.session_state.persona_chat_history.append({
        "role": "user",
        "content": question
    })
    
    # Build conversation history for context
    conversation = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.persona_chat_history[:-1]
    ]
    
    # Get AI response
    with st.spinner("Thinking..."):
        response = persona_manager.chat_about_persona(question, conversation)
    
    # Add response to history
    st.session_state.persona_chat_history.append({
        "role": "assistant",
        "content": response
    })


def render_persona_cards(personas: List[Dict]):
    """Render persona cards for reference"""
    st.markdown("### 👥 Your Personas")
    
    cols = st.columns(min(3, len(personas)))
    
    for i, persona in enumerate(personas):
        col_idx = i % len(cols)
        
        with cols[col_idx]:
            st.markdown(f"#### {persona.get('name', 'Unknown')}")
            
            # Role
            role = persona.get('role', 'N/A')
            st.markdown(f"**Role:** {role}")
            
            # Description
            desc = persona.get('description', 'No description')
            st.markdown(f"*{desc[:100]}...*" if len(desc) > 100 else f"*{desc}*")
            
            # Pain points (top 3)
            pain_points = persona.get('pain_points', [])[:3]
            if pain_points:
                st.markdown("**Pain Points:**")
                for pp in pain_points:
                    st.markdown(f"- {pp}")
            
            # Goals (top 3)
            goals = persona.get('goals', [])[:3]
            if goals:
                st.markdown("**Goals:**")
                for g in goals:
                    st.markdown(f"- {g}")
            
            st.markdown("---")


def render_comparison_tool(persona_manager):
    """Render persona comparison tool"""
    st.markdown("### ⚖️ Compare Personas")
    
    personas = persona_manager.get_all_personas()
    persona_names = [p.get('name', 'Unknown') for p in personas]
    
    if len(personas) < 2:
        st.info("Add at least 2 personas to use comparison")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        persona1 = st.selectbox("First Persona", persona_names, key="compare_p1")
    
    with col2:
        remaining = [n for n in persona_names if n != persona1]
        persona2 = st.selectbox("Second Persona", remaining, key="compare_p2")
    
    if st.button("Compare", key="compare_btn"):
        question = f"Compare {persona1} and {persona2}. What are the key differences in their pain points, goals, and preferred content? How should my approach differ when targeting each?"
        
        with st.spinner("Analyzing..."):
            response = persona_manager.chat_about_persona(question)
        
        st.markdown("### Comparison Results")
        st.markdown(response)


def render_content_advisor(persona_manager):
    """Render content advice tool"""
    st.markdown("### 📝 Content Advisor")
    st.markdown("Get recommendations for content based on persona and stage.")
    
    personas = persona_manager.get_all_personas()
    persona_names = [p.get('name', 'Unknown') for p in personas]
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_persona = st.selectbox(
            "Target Persona",
            persona_names,
            key="content_advisor_persona"
        )
    
    with col2:
        selected_stage = st.selectbox(
            "Funnel Stage",
            ["Awareness", "Consideration", "Decision"],
            key="content_advisor_stage"
        )
    
    topic = st.text_input(
        "Content Topic (optional)",
        placeholder="e.g., AI automation, cost savings, efficiency",
        key="content_advisor_topic"
    )
    
    if st.button("Get Recommendations", key="get_content_advice"):
        question = f"""I want to create content for {selected_persona} at the {selected_stage} stage.
        {f'The topic is: {topic}' if topic else ''}
        
        What type of content should I create? What key messages should I include? 
        What angle or hook would resonate best with this persona at this stage?"""
        
        with st.spinner("Generating recommendations..."):
            response = persona_manager.chat_about_persona(question)
        
        st.markdown("### Recommendations")
        st.markdown(response)
