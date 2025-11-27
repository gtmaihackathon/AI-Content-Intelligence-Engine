"""
Strategy Generator - Generates AI-powered content strategy recommendations
Using OpenAI API
"""

import json
from typing import Dict, List, Any
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME, FUNNEL_STAGES, CONTENT_TYPES


class StrategyGenerator:
    """Generates content strategy recommendations using AI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    
    def generate_strategy(
        self,
        gaps: List[Dict],
        strengths: List[Dict],
        personas: List[Dict],
        analyzed_content: List[Dict],
        coverage_matrix: Dict
    ) -> Dict:
        """Generate comprehensive content strategy recommendations"""
        if not self.client:
            return self._fallback_strategy(gaps, strengths, personas)
        
        gaps_summary = "\n".join([
            f"- {g['persona']} at {g['stage_name']} stage (priority: {g['priority']})"
            for g in gaps[:10]
        ])
        
        strengths_summary = "\n".join([
            f"- {s['persona']} at {s['stage_name']} stage (score: {s['coverage_score']})"
            for s in strengths[:10]
        ])
        
        persona_summary = "\n".join([
            f"- {p['name']}: {p.get('description', '')}. Pain points: {', '.join(p.get('pain_points', [])[:3])}"
            for p in personas
        ])
        
        content_summary = f"Total content analyzed: {len(analyzed_content)} pieces"
        
        prompt = f"""You are a content strategy expert. Based on the following content audit results, generate a comprehensive quarterly content strategy.

PERSONAS:
{persona_summary}

CONTENT GAPS (prioritized):
{gaps_summary}

STRONG COVERAGE AREAS:
{strengths_summary}

{content_summary}

Generate a detailed content strategy with the following structure. Return as JSON:

{{
    "executive_summary": "2-3 paragraph overview of findings and recommendations",
    
    "priority_content_to_create": [
        {{
            "title": "suggested content title",
            "type": "blog_post|case_study|whitepaper|etc",
            "target_persona": "persona name",
            "funnel_stage": "awareness|consideration|decision",
            "priority": "high|medium|low",
            "rationale": "why this content is needed",
            "key_topics": ["topic1", "topic2"],
            "suggested_angle": "unique angle or hook",
            "estimated_effort": "small|medium|large"
        }}
    ],
    
    "content_improvements": [
        {{
            "content_area": "description of content area",
            "current_issue": "what's wrong or missing",
            "recommendation": "specific improvement suggestion",
            "impact": "expected impact of improvement"
        }}
    ],
    
    "quarterly_calendar": {{
        "month_1": [
            {{
                "week": 1,
                "content_title": "title",
                "content_type": "type",
                "target_persona": "persona"
            }}
        ],
        "month_2": [],
        "month_3": []
    }},
    
    "persona_specific_recommendations": {{
        "persona_name": {{
            "key_insight": "main insight about content for this persona",
            "content_priorities": ["priority 1", "priority 2"],
            "messaging_themes": ["theme 1", "theme 2"],
            "content_types_to_focus": ["type 1", "type 2"]
        }}
    }},
    
    "quick_wins": ["list of easy-to-implement improvements"],
    
    "long_term_initiatives": [
        {{
            "initiative": "description",
            "timeline": "estimated timeline",
            "resources_needed": "what's needed",
            "expected_outcome": "what success looks like"
        }}
    ],
    
    "metrics_to_track": [
        {{
            "metric": "metric name",
            "why": "why this metric matters",
            "target": "suggested target"
        }}
    ]
}}

Provide specific, actionable recommendations. Focus on filling the highest-priority gaps.
Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.5
            )
            
            response_text = response.choices[0].message.content
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            strategy = json.loads(response_text.strip())
            return strategy
        except Exception as e:
            print(f"Strategy generation error: {e}")
            return self._fallback_strategy(gaps, strengths, personas)
    
    def _fallback_strategy(self, gaps: List[Dict], strengths: List[Dict], personas: List[Dict]) -> Dict:
        """Generate basic strategy without AI"""
        priority_content = []
        for gap in gaps[:5]:
            content_type = "blog_post"
            if gap["stage"] == "decision":
                content_type = "case_study"
            elif gap["stage"] == "consideration":
                content_type = "whitepaper"
            
            priority_content.append({
                "title": f"Content for {gap['persona']} - {gap['stage_name']} Stage",
                "type": content_type,
                "target_persona": gap["persona"],
                "funnel_stage": gap["stage"],
                "priority": "high" if gap["priority"] > 70 else "medium",
                "rationale": f"Gap identified: No content for {gap['persona']} at {gap['stage_name']} stage",
                "key_topics": [],
                "suggested_angle": "Address key pain points",
                "estimated_effort": "medium"
            })
        
        return {
            "executive_summary": f"Analysis identified {len(gaps)} content gaps and {len(strengths)} strong coverage areas.",
            "priority_content_to_create": priority_content,
            "content_improvements": [],
            "quarterly_calendar": {"month_1": [], "month_2": [], "month_3": []},
            "persona_specific_recommendations": {},
            "quick_wins": ["Review and update existing content titles"],
            "long_term_initiatives": [],
            "metrics_to_track": [{"metric": "Content per persona/stage", "why": "Coverage", "target": "3-5 pieces"}]
        }
    
    def generate_content_brief(
        self,
        content_recommendation: Dict,
        persona: Dict,
        existing_content: List[Dict] = None
    ) -> str:
        """Generate a detailed content brief for a specific piece"""
        if not self.client:
            return "API not available. Please create brief manually."
        
        existing_summary = ""
        if existing_content:
            existing_summary = "\nRelated existing content:\n" + "\n".join([
                f"- {c.get('original_title', 'Untitled')}: {c.get('summary', '')[:100]}"
                for c in existing_content[:5]
            ])
        
        prompt = f"""Create a detailed content brief for the following piece:

CONTENT TO CREATE:
Title: {content_recommendation.get('title', 'TBD')}
Type: {content_recommendation.get('type', 'blog_post')}
Funnel Stage: {content_recommendation.get('funnel_stage', 'awareness')}

TARGET PERSONA:
Name: {persona.get('name', 'Unknown')}
Role: {persona.get('role', 'N/A')}
Pain Points: {', '.join(persona.get('pain_points', []))}
Goals: {', '.join(persona.get('goals', []))}
{existing_summary}

Generate a comprehensive content brief including:
1. Working title options (3)
2. Target keywords (5-7)
3. Content outline with sections
4. Key messages to convey
5. Desired reader takeaways
6. Call-to-action recommendations
7. Internal linking opportunities
8. Visual/media suggestions
9. Distribution channels
10. Success metrics

Provide actionable, specific guidance."""

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating brief: {str(e)}"
