"""
Strategy Generator - Generates AI-powered content strategy recommendations
"""

import json
from typing import Dict, List, Any
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, MODEL_NAME, FUNNEL_STAGES, CONTENT_TYPES


class StrategyGenerator:
    """Generates content strategy recommendations using AI"""
    
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
    
    def generate_strategy(
        self,
        gaps: List[Dict],
        strengths: List[Dict],
        personas: List[Dict],
        analyzed_content: List[Dict],
        coverage_matrix: Dict
    ) -> Dict:
        """
        Generate comprehensive content strategy recommendations
        
        Args:
            gaps: List of identified gaps
            strengths: List of strong coverage areas
            personas: List of personas
            analyzed_content: All analyzed content
            coverage_matrix: Full coverage matrix
            
        Returns:
            Strategy recommendations
        """
        if not self.client:
            return self._fallback_strategy(gaps, strengths, personas)
        
        # Build context for AI
        gaps_summary = "\n".join([
            f"- {g['persona']} at {g['stage_name']} stage (priority: {g['priority']})"
            for g in gaps[:10]  # Top 10 gaps
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
        "month_2": [...],
        "month_3": [...]
    }},
    
    "persona_specific_recommendations": {{
        "persona_name": {{
            "key_insight": "main insight about content for this persona",
            "content_priorities": ["priority 1", "priority 2"],
            "messaging_themes": ["theme 1", "theme 2"],
            "content_types_to_focus": ["type 1", "type 2"]
        }}
    }},
    
    "quick_wins": [
        "list of easy-to-implement improvements"
    ],
    
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

Provide specific, actionable recommendations. Focus on filling the highest-priority gaps while leveraging existing strengths.
Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            
            # Clean up response
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
        
        # Generate content recommendations based on gaps
        priority_content = []
        for gap in gaps[:5]:  # Top 5 gaps
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
            "executive_summary": f"Analysis identified {len(gaps)} content gaps and {len(strengths)} strong coverage areas. Priority should be given to creating content for the highest-priority gaps.",
            "priority_content_to_create": priority_content,
            "content_improvements": [
                {
                    "content_area": "General",
                    "current_issue": "AI analysis unavailable for detailed recommendations",
                    "recommendation": "Review content manually for improvement opportunities",
                    "impact": "Variable"
                }
            ],
            "quarterly_calendar": {
                "month_1": [],
                "month_2": [],
                "month_3": []
            },
            "persona_specific_recommendations": {
                p["name"]: {
                    "key_insight": "Manual analysis recommended",
                    "content_priorities": [],
                    "messaging_themes": [],
                    "content_types_to_focus": []
                }
                for p in personas
            },
            "quick_wins": ["Review and update existing content titles and meta descriptions"],
            "long_term_initiatives": [],
            "metrics_to_track": [
                {
                    "metric": "Content per persona/stage",
                    "why": "Ensure coverage across all segments",
                    "target": "3-5 pieces per cell"
                }
            ]
        }
    
    def generate_content_brief(
        self,
        content_recommendation: Dict,
        persona: Dict,
        existing_content: List[Dict] = None
    ) -> str:
        """
        Generate a detailed content brief for a specific piece
        
        Args:
            content_recommendation: The content piece to create
            persona: Target persona details
            existing_content: Related existing content for reference
            
        Returns:
            Detailed content brief
        """
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
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error generating brief: {str(e)}"
    
    def suggest_content_repurposing(self, content: Dict, target_formats: List[str] = None) -> List[Dict]:
        """
        Suggest ways to repurpose existing content
        
        Args:
            content: Analyzed content piece
            target_formats: Desired output formats
            
        Returns:
            List of repurposing suggestions
        """
        if not self.client:
            return []
        
        target_formats = target_formats or ["social_media", "email", "video_script", "infographic"]
        
        prompt = f"""Suggest ways to repurpose the following content:

ORIGINAL CONTENT:
Title: {content.get('original_title', 'Untitled')}
Type: {content.get('content_type', 'unknown')}
Summary: {content.get('summary', 'N/A')}
Key Messages: {', '.join(content.get('key_messages', []))}

TARGET FORMATS: {', '.join(target_formats)}

For each format, provide:
1. Suggested title/hook
2. Key points to include
3. Estimated effort
4. Best platform/channel

Return as JSON array of objects with format, title, key_points, effort, channel fields."""

        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            return json.loads(response_text.strip())
            
        except Exception as e:
            print(f"Repurposing suggestion error: {e}")
            return []
