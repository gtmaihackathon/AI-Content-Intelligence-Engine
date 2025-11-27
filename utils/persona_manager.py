"""
Persona Manager - Handles persona data extraction, storage, and retrieval
"""

import json
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from config import OPENAI_API_KEY, MODEL_NAME, DEFAULT_PERSONAS


class PersonaManager:
    """Manages persona data and persona-related AI operations"""

    class PersonaManager:
    def __init__(self):
        # Get API key when the class is instantiated, not at import time
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except (FileNotFoundError, KeyError):
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            st.error("❌ API Key Missing: Add `OPENAI_API_KEY` to .streamlit/secrets.toml")
            st.stop()
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.personas: List[Dict[str, Any]] = []
        self.persona_texts: Dict[str, str] = {}  # Store raw text for chat
    
    def load_default_personas(self):
        """Load default personas from config"""
        self.personas = DEFAULT_PERSONAS.copy()
    
    def extract_personas_from_text(self, text: str, source_name: str = "uploaded") -> List[Dict]:
        """
        Use AI to extract structured persona data from raw text
        
        Args:
            text: Raw text containing persona information
            source_name: Name of the source document
            
        Returns:
            List of structured persona dictionaries
        """
        if not self.client:
            return self._fallback_persona_extraction(text)
        
        prompt = f"""Analyze the following persona research document and extract structured persona information.

For each persona found, extract:
1. name: The persona name/title (e.g., "CFO Emma", "Marketing Manager Mike")
2. role: Their job role/title
3. description: Brief description of who they are
4. demographics: Any demographic info (company size, industry, etc.)
5. pain_points: List of their key challenges and pain points
6. goals: List of their primary goals and objectives
7. motivations: What drives their decisions
8. objections: Common objections or concerns they have
9. preferred_content: Types of content they prefer
10. buying_triggers: What triggers them to buy/evaluate solutions
11. key_messages: Messages that resonate with them

Return the data as a JSON array of persona objects. If certain fields aren't mentioned, use null.

Document text:
{text[:15000]}  # Limit to avoid token limits

Return ONLY valid JSON, no other text."""

        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            response_text = response.content[0].text
            
            # Clean up response if needed
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            personas = json.loads(response_text.strip())
            
            # Store the raw text for this persona set
            for persona in personas:
                persona_name = persona.get("name", "Unknown")
                self.persona_texts[persona_name] = text
            
            return personas
            
        except Exception as e:
            print(f"AI extraction error: {e}")
            return self._fallback_persona_extraction(text)
    
    def _fallback_persona_extraction(self, text: str) -> List[Dict]:
        """Fallback extraction without AI"""
        # Basic extraction based on common patterns
        personas = []
        
        # Look for common persona indicators
        lines = text.split('\n')
        current_persona = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for persona headers
            lower_line = line.lower()
            if any(indicator in lower_line for indicator in ['persona:', 'buyer persona', 'target audience', 'ideal customer']):
                if current_persona:
                    personas.append(current_persona)
                current_persona = {
                    "name": line.split(':')[-1].strip() if ':' in line else line,
                    "role": None,
                    "description": "",
                    "pain_points": [],
                    "goals": [],
                    "motivations": [],
                    "objections": [],
                    "preferred_content": [],
                    "buying_triggers": []
                }
        
        if current_persona:
            personas.append(current_persona)
        
        # If no personas found, create a generic one
        if not personas:
            personas = [{
                "name": "Extracted Persona",
                "role": "Unknown",
                "description": text[:500],
                "pain_points": [],
                "goals": [],
                "motivations": [],
                "objections": [],
                "preferred_content": [],
                "buying_triggers": []
            }]
        
        return personas
    
    def add_persona(self, persona: Dict[str, Any]):
        """Add a persona to the collection"""
        self.personas.append(persona)
    
    def add_personas(self, personas: List[Dict[str, Any]]):
        """Add multiple personas"""
        self.personas.extend(personas)
    
    def get_persona_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific persona by name"""
        for persona in self.personas:
            if persona.get("name", "").lower() == name.lower():
                return persona
        return None
    
    def get_all_personas(self) -> List[Dict]:
        """Get all personas"""
        return self.personas
    
    def get_persona_names(self) -> List[str]:
        """Get list of all persona names"""
        return [p.get("name", "Unknown") for p in self.personas]
    
    def clear_personas(self):
        """Clear all personas"""
        self.personas = []
        self.persona_texts = {}
    
    def get_persona_summary(self) -> str:
        """Get a text summary of all personas for AI prompts"""
        if not self.personas:
            return "No personas defined."
        
        summaries = []
        for persona in self.personas:
            summary = f"""
**{persona.get('name', 'Unknown')}**
- Role: {persona.get('role', 'N/A')}
- Description: {persona.get('description', 'N/A')}
- Pain Points: {', '.join(persona.get('pain_points', [])) or 'N/A'}
- Goals: {', '.join(persona.get('goals', [])) or 'N/A'}
"""
            summaries.append(summary)
        
        return "\n".join(summaries)
    
    def chat_about_persona(self, query: str, conversation_history: List[Dict] = None) -> str:
        """
        Chat interface for asking questions about personas
        
        Args:
            query: User's question about personas
            conversation_history: Previous messages in conversation
            
        Returns:
            AI response about personas
        """
        if not self.client:
            return "API key not configured. Please set ANTHROPIC_API_KEY."
        
        if not self.personas:
            return "No personas loaded. Please upload persona research first."
        
        # Build context with all persona information
        persona_context = self.get_persona_summary()
        
        # Include raw text if available
        raw_texts = "\n\n".join([
            f"--- Raw research for {name} ---\n{text[:3000]}"
            for name, text in self.persona_texts.items()
        ])
        
        system_prompt = f"""You are a helpful persona research assistant. You have detailed knowledge about the following buyer personas:

{persona_context}

Additional research context:
{raw_texts[:10000]}

Help users understand these personas to create better content and sales materials. Answer questions about:
- Persona pain points and motivations
- What content would resonate with each persona
- How to position messaging for specific personas
- Differences between personas
- How to approach prospects that match these personas

Be specific and actionable in your responses. Reference the actual persona data when answering."""

        messages = conversation_history or []
        messages.append({"role": "user", "content": query})
        
        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=2000,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    def to_dict(self) -> Dict:
        """Export personas to dictionary"""
        return {
            "personas": self.personas,
            "persona_texts": self.persona_texts
        }
    
    def from_dict(self, data: Dict):
        """Import personas from dictionary"""
        self.personas = data.get("personas", [])
        self.persona_texts = data.get("persona_texts", {})
