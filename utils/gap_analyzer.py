"""
Gap Analyzer - Identifies content gaps across persona/funnel matrix
"""

from typing import Dict, List, Any
from config import FUNNEL_STAGES, SCORING_THRESHOLDS


class GapAnalyzer:
    """Analyzes content coverage and identifies gaps"""
    
    def __init__(self, personas: List[Dict] = None):
        self.personas = personas or []
        self.funnel_stages = list(FUNNEL_STAGES.keys())
        self.thresholds = SCORING_THRESHOLDS
        self.coverage_matrix: Dict[str, Dict[str, Dict]] = {}
    
    def set_personas(self, personas: List[Dict]):
        """Update personas"""
        self.personas = personas
        self._initialize_matrix()
    
    def _initialize_matrix(self):
        """Initialize empty coverage matrix"""
        self.coverage_matrix = {}
        for persona in self.personas:
            persona_name = persona.get("name", "Unknown")
            self.coverage_matrix[persona_name] = {}
            for stage in self.funnel_stages:
                self.coverage_matrix[persona_name][stage] = {
                    "content_count": 0,
                    "content_items": [],
                    "avg_quality": 0,
                    "coverage_score": 0,
                    "status": "gap"
                }
    
    def analyze_coverage(self, analyzed_content: List[Dict]) -> Dict:
        """Analyze content coverage across persona/funnel matrix"""
        self._initialize_matrix()
        
        for content in analyzed_content:
            primary_persona = content.get("primary_persona", "Unknown")
            stage = content.get("funnel_stage", "awareness")
            quality = content.get("quality_score", 50)
            
            if primary_persona in self.coverage_matrix:
                if stage in self.coverage_matrix[primary_persona]:
                    cell = self.coverage_matrix[primary_persona][stage]
                    cell["content_count"] += 1
                    cell["content_items"].append({
                        "title": content.get("original_title", "Untitled"),
                        "source": content.get("original_source", ""),
                        "quality": quality
                    })
            
            for secondary_persona in content.get("secondary_personas", []):
                if secondary_persona in self.coverage_matrix:
                    if stage in self.coverage_matrix[secondary_persona]:
                        cell = self.coverage_matrix[secondary_persona][stage]
                        cell["content_count"] += 0.5
        
        self._calculate_scores()
        return self.coverage_matrix
    
    def _calculate_scores(self):
        """Calculate coverage scores for each cell"""
        max_content_per_cell = 5
        
        for persona_name in self.coverage_matrix:
            for stage in self.coverage_matrix[persona_name]:
                cell = self.coverage_matrix[persona_name][stage]
                content_score = min(100, (cell["content_count"] / max_content_per_cell) * 100)
                
                if cell["content_items"]:
                    qualities = [item["quality"] for item in cell["content_items"]]
                    cell["avg_quality"] = sum(qualities) / len(qualities)
                else:
                    cell["avg_quality"] = 0
                
                cell["coverage_score"] = round(
                    (content_score * 0.6) + (cell["avg_quality"] * 0.4), 1
                )
                
                if cell["coverage_score"] >= self.thresholds["strong"]:
                    cell["status"] = "strong"
                elif cell["coverage_score"] >= self.thresholds["moderate"]:
                    cell["status"] = "moderate"
                else:
                    cell["status"] = "gap"
    
    def get_gaps(self) -> List[Dict]:
        """Get list of all identified gaps"""
        gaps = []
        
        for persona_name in self.coverage_matrix:
            for stage in self.coverage_matrix[persona_name]:
                cell = self.coverage_matrix[persona_name][stage]
                if cell["status"] == "gap":
                    gaps.append({
                        "persona": persona_name,
                        "stage": stage,
                        "stage_name": FUNNEL_STAGES.get(stage, {}).get("name", stage),
                        "coverage_score": cell["coverage_score"],
                        "content_count": cell["content_count"],
                        "priority": self._calculate_priority(persona_name, stage, cell)
                    })
        
        gaps.sort(key=lambda x: x["priority"], reverse=True)
        return gaps
    
    def _calculate_priority(self, persona_name: str, stage: str, cell: Dict) -> int:
        """Calculate gap priority score"""
        priority = 100 - cell["coverage_score"]
        
        if stage == "decision":
            priority += 20
        elif stage == "consideration":
            priority += 10
        
        return min(100, priority)
    
    def get_strengths(self) -> List[Dict]:
        """Get areas with strong coverage"""
        strengths = []
        
        for persona_name in self.coverage_matrix:
            for stage in self.coverage_matrix[persona_name]:
                cell = self.coverage_matrix[persona_name][stage]
                if cell["status"] == "strong":
                    strengths.append({
                        "persona": persona_name,
                        "stage": stage,
                        "stage_name": FUNNEL_STAGES.get(stage, {}).get("name", stage),
                        "coverage_score": cell["coverage_score"],
                        "content_count": cell["content_count"],
                        "top_content": cell["content_items"][:3]
                    })
        
        return strengths
    
    def get_moderate_areas(self) -> List[Dict]:
        """Get areas with moderate coverage"""
        moderate = []
        
        for persona_name in self.coverage_matrix:
            for stage in self.coverage_matrix[persona_name]:
                cell = self.coverage_matrix[persona_name][stage]
                if cell["status"] == "moderate":
                    moderate.append({
                        "persona": persona_name,
                        "stage": stage,
                        "stage_name": FUNNEL_STAGES.get(stage, {}).get("name", stage),
                        "coverage_score": cell["coverage_score"],
                        "content_count": cell["content_count"],
                        "improvement_potential": 100 - cell["coverage_score"]
                    })
        
        return moderate
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        total_cells = len(self.personas) * len(self.funnel_stages)
        gaps = self.get_gaps()
        strengths = self.get_strengths()
        moderate = self.get_moderate_areas()
        
        return {
            "total_cells": total_cells,
            "gap_count": len(gaps),
            "moderate_count": len(moderate),
            "strong_count": len(strengths),
            "gap_percentage": round((len(gaps) / total_cells) * 100, 1) if total_cells > 0 else 0,
            "coverage_percentage": round(((len(strengths) + len(moderate)) / total_cells) * 100, 1) if total_cells > 0 else 0,
            "highest_priority_gap": gaps[0] if gaps else None
        }
    
    def get_stage_summary(self) -> Dict[str, Dict]:
        """Get summary by funnel stage"""
        summary = {}
        
        for stage in self.funnel_stages:
            stage_data = {
                "total_content": 0,
                "avg_coverage": 0,
                "personas_with_gaps": []
            }
            
            scores = []
            for persona_name in self.coverage_matrix:
                cell = self.coverage_matrix[persona_name][stage]
                stage_data["total_content"] += cell["content_count"]
                scores.append(cell["coverage_score"])
                
                if cell["status"] == "gap":
                    stage_data["personas_with_gaps"].append(persona_name)
            
            stage_data["avg_coverage"] = round(sum(scores) / len(scores), 1) if scores else 0
            summary[stage] = stage_data
        
        return summary
    
    def get_persona_summary(self) -> Dict[str, Dict]:
        """Get summary by persona"""
        summary = {}
        
        for persona_name in self.coverage_matrix:
            persona_data = {
                "total_content": 0,
                "avg_coverage": 0,
                "stages_with_gaps": [],
                "strongest_stage": None
            }
            
            scores = []
            max_score = 0
            max_stage = None
            
            for stage in self.funnel_stages:
                cell = self.coverage_matrix[persona_name][stage]
                persona_data["total_content"] += cell["content_count"]
                scores.append(cell["coverage_score"])
                
                if cell["coverage_score"] > max_score:
                    max_score = cell["coverage_score"]
                    max_stage = stage
                
                if cell["status"] == "gap":
                    persona_data["stages_with_gaps"].append(stage)
            
            persona_data["avg_coverage"] = round(sum(scores) / len(scores), 1) if scores else 0
            persona_data["strongest_stage"] = max_stage
            summary[persona_name] = persona_data
        
        return summary
    
    def export_matrix(self) -> Dict:
        """Export the full coverage matrix"""
        return self.coverage_matrix
