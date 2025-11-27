"""
Content Analyzer - Analyzes and classifies content assets
"""

import json
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, MODEL_NAME, FUNNEL_STAGES, CONTENT_TYPES


class ContentAnalyzer:
    """Analyzes content and classifies by persona, funnel stage, and intent"""
    
    def __init__(self, personas: List[Dict] = None):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
        self.personas = personas or []
        self.funnel_stages = FUNNEL_STAGES
        self.analyzed_content: List[Dict] = []
    
    def set_personas(self, personas: List[Dict]):
        """Update personas for analysis"""
        self.personas = personas
    
    def analyze_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single content piece
        
        Args:
            content: Dict with 'title', 'content', 'source', 'type' keys
            
        Returns:
            Analysis results including persona mapping, funnel stage, etc.
        """
        if not self.client:
            return self._fallback_analysis(content)
        
        # Build persona list for prompt
        persona_names = [p.get("name", "Unknown") for p in self.personas]
        persona_details = "\n".join([
            f"- {p.get('name')}: {p.get('description', '')}. Pain points: {', '.join(p.get('pain_points', []))}"
            for p in self.personas
        ])
        
        prompt = f"""Analyze the following content and classify it.

CONTENT:
Title: {content.get('title', 'Untitled')}
Source: {content.get('source', 'Unknown')}
Type: {content.get('type', 'Unknown')}

Content text:
{content.get('content', '')[:8000]}

PERSONAS TO CONSIDER:
{persona_details}

FUNNEL STAGES:
- awareness: Top of funnel - educational, problem-focused content
- consideration: Middle of funnel - solution-focused, comparison content
- decision: Bottom of funnel - proof, validation, buying content

Analyze this content and return a JSON object with:
{{
    "content_type": "detected content type (blog_post, case_study, whitepaper, etc.)",
    "primary_persona": "name of the persona this content best targets",
    "secondary_personas": ["list of other relevant personas"],
    "persona_scores": {{"persona_name": score_0_to_100}},
    "funnel_stage": "awareness|consideration|decision",
    "funnel_confidence": 0-100,
    "topics": ["list of main topics covered"],
    "intent": "educational|comparative|promotional|proof|other",
    "key_messages": ["list of key messages in the content"],
    "tone": "formal|casual|technical|inspirational",
    "strengths": ["what this content does well"],
    "improvements": ["suggested improvements"],
    "missing_elements": ["elements that could strengthen the content"],
    "quality_score": 0-100,
    "summary": "2-3 sentence summary of the content"
}}

Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            
            # Clean up response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            analysis = json.loads(response_text.strip())
            
            # Add original content metadata
            analysis["original_title"] = content.get("title")
            analysis["original_source"] = content.get("source")
            analysis["word_count"] = len(content.get("content", "").split())
            
            return analysis
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._fallback_analysis(content)
    
    def _fallback_analysis(self, content: Dict) -> Dict:
        """Fallback analysis without AI"""
        text = content.get("content", "").lower()
        title = content.get("title", "").lower()
        
        # Simple keyword-based classification
        awareness_keywords = ["what is", "introduction", "guide", "tips", "how to start", "basics"]
        consideration_keywords = ["compare", "vs", "alternative", "solution", "platform", "tool"]
        decision_keywords = ["case study", "testimonial", "pricing", "demo", "trial", "buy"]
        
        # Determine funnel stage
        funnel_stage = "awareness"
        if any(kw in text or kw in title for kw in decision_keywords):
            funnel_stage = "decision"
        elif any(kw in text or kw in title for kw in consideration_keywords):
            funnel_stage = "consideration"
        
        # Basic persona scoring
        persona_scores = {}
        for persona in self.personas:
            score = 50  # Default score
            persona_keywords = persona.get("pain_points", []) + persona.get("goals", [])
            for keyword in persona_keywords:
                if keyword.lower() in text:
                    score += 10
            persona_scores[persona.get("name", "Unknown")] = min(score, 100)
        
        return {
            "content_type": content.get("type", "unknown"),
            "primary_persona": max(persona_scores, key=persona_scores.get) if persona_scores else "Unknown",
            "secondary_personas": [],
            "persona_scores": persona_scores,
            "funnel_stage": funnel_stage,
            "funnel_confidence": 50,
            "topics": [],
            "intent": "educational",
            "key_messages": [],
            "tone": "neutral",
            "strengths": [],
            "improvements": ["AI analysis unavailable - manual review recommended"],
            "missing_elements": [],
            "quality_score": 50,
            "summary": "Automated analysis - AI not available",
            "original_title": content.get("title"),
            "original_source": content.get("source"),
            "word_count": len(content.get("content", "").split())
        }
    
    def batch_analyze(self, contents: List[Dict]) -> List[Dict]:
        """Analyze multiple content pieces"""
        results = []
        for content in contents:
            analysis = self.analyze_content(content)
            results.append(analysis)
            self.analyzed_content.append(analysis)
        return results
    
    def get_analysis_summary(self) -> Dict:
        """Get summary statistics of analyzed content"""
        if not self.analyzed_content:
            return {"error": "No content analyzed yet"}
        
        # Count by funnel stage
        stage_counts = {"awareness": 0, "consideration": 0, "decision": 0}
        for content in self.analyzed_content:
            stage = content.get("funnel_stage", "awareness")
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        # Count by persona
        persona_counts = {}
        for content in self.analyzed_content:
            persona = content.get("primary_persona", "Unknown")
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
        
        # Average quality score
        quality_scores = [c.get("quality_score", 50) for c in self.analyzed_content]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Content types
        type_counts = {}
        for content in self.analyzed_content:
            ctype = content.get("content_type", "unknown")
            type_counts[ctype] = type_counts.get(ctype, 0) + 1
        
        return {
            "total_content": len(self.analyzed_content),
            "by_funnel_stage": stage_counts,
            "by_persona": persona_counts,
            "by_content_type": type_counts,
            "average_quality_score": round(avg_quality, 1),
            "total_word_count": sum(c.get("word_count", 0) for c in self.analyzed_content)
        }
    
    def get_content_by_stage(self, stage: str) -> List[Dict]:
        """Get all content for a specific funnel stage"""
        return [c for c in self.analyzed_content if c.get("funnel_stage") == stage]
    
    def get_content_by_persona(self, persona_name: str) -> List[Dict]:
        """Get all content targeting a specific persona"""
        return [c for c in self.analyzed_content if c.get("primary_persona") == persona_name]
    
    def clear_analysis(self):
        """Clear all analyzed content"""
        self.analyzed_content = []
    
    def export_analysis(self) -> List[Dict]:
        """Export all analysis results"""
        return self.analyzed_content
