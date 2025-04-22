"""
Nutrition Agent for Longevity Snapshot App

This module implements a specialized agent for analyzing nutrition data
and providing evidence-based dietary recommendations.
"""

from typing import Dict, List, Any, Optional
import logging
from .base_agent import BaseAgent, ConfidenceLevel

logger = logging.getLogger("agent.nutrition")

class NutritionAgent(BaseAgent):
    """
    Specialized agent for nutrition analysis and recommendations
    focused on longevity-promoting dietary patterns.
    """
    
    def __init__(self):
        """Initialize the Nutrition Agent"""
        super().__init__("Nutrition")
        
        # Evidence-based dietary patterns associated with longevity
        self.longevity_dietary_patterns = [
            "Mediterranean",
            "DASH",
            "Plant-forward",
            "Blue Zone inspired",
            "MIND"
        ]
        
        # Key nutrients for longevity
        self.longevity_nutrients = {
            "protein": {"min": 0.8, "optimal": 1.2, "max": 2.0, "unit": "g/kg/day"},
            "fiber": {"min": 25, "optimal": 30, "max": 50, "unit": "g/day"},
            "omega3": {"min": 1.1, "optimal": 2.0, "max": 3.0, "unit": "g/day"},
            "polyphenols": {"min": 500, "optimal": 1000, "max": None, "unit": "mg/day"}
        }
    
    def _extract_relevant_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract nutrition-related data from user data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing relevant nutrition data
        """
        relevant_data = {
            "user_profile": {},
            "nutrition_data": {}
        }
        
        # Extract basic user profile
        if "age" in user_data:
            relevant_data["user_profile"]["age"] = user_data["age"]
        if "gender" in user_data:
            relevant_data["user_profile"]["gender"] = user_data["gender"]
        if "weight" in user_data:
            relevant_data["user_profile"]["weight"] = user_data["weight"]
        if "height" in user_data:
            relevant_data["user_profile"]["height"] = user_data["height"]
        
        # Extract nutrition data
        if "nutrition_data" in user_data and user_data["nutrition_data"]:
            relevant_data["nutrition_data"] = user_data["nutrition_data"]
        
        # Extract dietary preferences
        if "preferences" in user_data and user_data["preferences"]:
            if "diet" in user_data["preferences"]:
                relevant_data["user_profile"]["diet_preference"] = user_data["preferences"]["diet"]
        
        # Extract medical history relevant to nutrition
        if "medical_history" in user_data and user_data["medical_history"]:
            nutrition_relevant_conditions = [
                "diabetes", "hypertension", "cardiovascular disease", 
                "celiac", "food allergies", "ibs", "inflammatory bowel disease"
            ]
            relevant_data["user_profile"]["nutrition_relevant_conditions"] = [
                condition for condition in user_data["medical_history"]
                if any(rel_condition in condition.lower() for rel_condition in nutrition_relevant_conditions)
            ]
        
        return relevant_data
    
    def _analyze_data(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze nutrition data to identify patterns and areas for improvement
        
        Args:
            relevant_data: Dictionary containing relevant nutrition data
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "nutrient_analysis": {},
            "dietary_pattern": {},
            "longevity_alignment": {},
            "areas_for_improvement": [],
            "strengths": []
        }
        
        # Extract nutrition data
        nutrition_data = relevant_data.get("nutrition_data", {})
        user_profile = relevant_data.get("user_profile", {})
        
        # Analyze macronutrient distribution
        if nutrition_data:
            total_calories = nutrition_data.get("calories", 0)
            if total_calories > 0:
                # Calculate macronutrient percentages
                protein_cals = nutrition_data.get("protein", 0) * 4
                carbs_cals = nutrition_data.get("carbs", 0) * 4
                fat_cals = nutrition_data.get("fat", 0) * 9
                
                protein_pct = (protein_cals / total_calories) * 100 if total_calories > 0 else 0
                carbs_pct = (carbs_cals / total_calories) * 100 if total_calories > 0 else 0
                fat_pct = (fat_cals / total_calories) * 100 if total_calories > 0 else 0
                
                analysis["nutrient_analysis"]["macronutrient_distribution"] = {
                    "protein_percentage": round(protein_pct, 1),
                    "carbohydrate_percentage": round(carbs_pct, 1),
                    "fat_percentage": round(fat_pct, 1)
                }
                
                # Evaluate protein adequacy
                weight_kg = user_profile.get("weight", 70) / 2.2  # Convert to kg if in pounds
                protein_g = nutrition_data.get("protein", 0)
                protein_per_kg = protein_g / weight_kg if weight_kg > 0 else 0
                
                analysis["nutrient_analysis"]["protein_per_kg"] = round(protein_per_kg, 1)
                
                # Evaluate fiber intake
                fiber_g = nutrition_data.get("fiber", 0)
                analysis["nutrient_analysis"]["fiber_g"] = fiber_g
                
                # Identify strengths and areas for improvement
                if protein_per_kg >= self.longevity_nutrients["protein"]["optimal"]:
                    analysis["strengths"].append("Optimal protein intake for muscle maintenance and longevity")
                elif protein_per_kg >= self.longevity_nutrients["protein"]["min"]:
                    analysis["strengths"].append("Adequate protein intake")
                else:
                    analysis["areas_for_improvement"].append("Increase protein intake for optimal muscle maintenance")
                
                if fiber_g >= self.longevity_nutrients["fiber"]["optimal"]:
                    analysis["strengths"].append("Excellent fiber intake supporting gut health and longevity")
                elif fiber_g >= self.longevity_nutrients["fiber"]["min"]:
                    analysis["strengths"].append("Adequate fiber intake")
                else:
                    analysis["areas_for_improvement"].append("Increase fiber intake from diverse plant sources")
                
                # Assess dietary pattern
                diet_preference = user_profile.get("diet_preference", "")
                if diet_preference in self.longevity_dietary_patterns:
                    analysis["dietary_pattern"]["current_pattern"] = diet_preference
                    analysis["dietary_pattern"]["longevity_aligned"] = True
                    analysis["strengths"].append(f"Following {diet_preference} dietary pattern associated with longevity")
                else:
                    # Infer dietary pattern from macronutrient distribution
                    if protein_pct > 25 and carbs_pct < 40:
                        analysis["dietary_pattern"]["current_pattern"] = "High protein, lower carb"
                    elif fat_pct > 40:
                        analysis["dietary_pattern"]["current_pattern"] = "High fat"
                    elif carbs_pct > 60:
                        analysis["dietary_pattern"]["current_pattern"] = "High carbohydrate"
                    else:
                        analysis["dietary_pattern"]["current_pattern"] = "Mixed/balanced"
                    
                    # Assess alignment with longevity patterns
                    plant_focus = nutrition_data.get("detailed_macros", False)
                    if plant_focus:
                        analysis["dietary_pattern"]["longevity_aligned"] = True
                        analysis["strengths"].append("Diet includes diverse plant foods supporting longevity")
                    else:
                        analysis["dietary_pattern"]["longevity_aligned"] = False
                        analysis["areas_for_improvement"].append("Increase plant diversity for longevity benefits")
        
        # Overall longevity alignment assessment
        if len(analysis["strengths"]) > len(analysis["areas_for_improvement"]):
            analysis["longevity_alignment"]["overall"] = "Strong"
        elif len(analysis["strengths"]) == len(analysis["areas_for_improvement"]):
            analysis["longevity_alignment"]["overall"] = "Moderate"
        else:
            analysis["longevity_alignment"]["overall"] = "Needs improvement"
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate nutrition recommendations based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # Generate recommendations based on areas for improvement
        for area in analysis.get("areas_for_improvement", []):
            if "protein" in area.lower():
                recommendations.append({
                    "category": "nutrition",
                    "subcategory": "protein",
                    "action": "increase_protein_intake",
                    "description": "Gradually increase protein intake to 1.2-1.6g per kg of body weight daily",
                    "reasoning": "Optimal protein intake supports muscle maintenance, immune function, and metabolic health - all critical factors in longevity",
                    "implementation": [
                        "Include a protein source with each meal (20-30g)",
                        "Consider protein distribution throughout the day rather than single large doses",
                        "Focus on high-quality protein sources (lean meats, fish, legumes, dairy)"
                    ],
                    "evidence_category": "systematic_review",
                    "priority": "high"
                })
            
            if "fiber" in area.lower():
                recommendations.append({
                    "category": "nutrition",
                    "subcategory": "fiber",
                    "action": "increase_fiber_intake",
                    "description": "Gradually increase fiber intake to 30+ grams daily from diverse plant sources",
                    "reasoning": "Dietary fiber supports gut microbiome diversity, reduces inflammation, and is consistently associated with longevity in population studies",
                    "implementation": [
                        "Add an additional serving of vegetables to lunch and dinner",
                        "Include legumes (beans, lentils) 3+ times weekly",
                        "Choose whole grains over refined options",
                        "Aim for 30+ different plant foods weekly for microbiome diversity"
                    ],
                    "evidence_category": "meta_analysis",
                    "priority": "high"
                })
            
            if "plant" in area.lower():
                recommendations.append({
                    "category": "nutrition",
                    "subcategory": "dietary_pattern",
                    "action": "adopt_plant_forward_diet",
                    "description": "Shift toward a more plant-forward dietary pattern while maintaining adequate protein",
                    "reasoning": "Plant-forward dietary patterns are consistently associated with longevity and reduced chronic disease risk in population studies",
                    "implementation": [
                        "Make vegetables the center of your plate",
                        "Include a wide variety of colorful plant foods",
                        "Limit ultra-processed foods",
                        "Consider a Mediterranean or MIND dietary pattern"
                    ],
                    "evidence_category": "clinical_guidelines",
                    "priority": "medium"
                })
        
        # Add general longevity nutrition recommendation if few specific ones
        if len(recommendations) < 2:
            recommendations.append({
                "category": "nutrition",
                "subcategory": "dietary_pattern",
                "action": "optimize_longevity_nutrition",
                "description": "Adopt key nutritional practices associated with longevity and healthspan",
                "reasoning": "Specific dietary patterns and practices are consistently associated with exceptional longevity in population studies",
                "implementation": [
                    "Emphasize plant diversity (30+ different plant foods weekly)",
                    "Include adequate protein (1.2-1.6g/kg/day) distributed throughout the day",
                    "Consume omega-3 rich foods regularly (fatty fish, walnuts, flax)",
                    "Consider time-restricted eating (8-10 hour eating window)"
                ],
                "evidence_category": "systematic_review",
                "priority": "high"
            })
        
        return recommendations
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights based on the nutrition analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing insights
        """
        insights = []
        
        # Generate insights about dietary pattern
        dietary_pattern = analysis.get("dietary_pattern", {}).get("current_pattern", "")
        if dietary_pattern:
            insights.append({
                "type": "dietary_pattern",
                "title": f"Current Dietary Pattern: {dietary_pattern}",
                "description": self._get_dietary_pattern_description(dietary_pattern),
                "relevance": "high"
            })
        
        # Generate insight about macronutrient distribution
        macros = analysis.get("nutrient_analysis", {}).get("macronutrient_distribution", {})
        if macros:
            insights.append({
                "type": "macronutrient_distribution",
                "title": "Macronutrient Balance",
                "description": f"Your current diet consists of approximately {macros.get('protein_percentage', 0)}% protein, "
                               f"{macros.get('carbohydrate_percentage', 0)}% carbohydrates, and "
                               f"{macros.get('fat_percentage', 0)}% fat.",
                "relevance": "medium"
            })
        
        # Generate insight about longevity alignment
        longevity_alignment = analysis.get("longevity_alignment", {}).get("overall", "")
        if longevity_alignment:
            insights.append({
                "type": "longevity_alignment",
                "title": f"Longevity Nutrition Alignment: {longevity_alignment}",
                "description": self._get_longevity_alignment_description(longevity_alignment),
                "relevance": "high"
            })
        
        return insights
    
    def _get_dietary_pattern_description(self, pattern: str) -> str:
        """Get description for a dietary pattern"""
        descriptions = {
            "Mediterranean": "Your diet resembles the Mediterranean pattern, characterized by abundant plant foods, "
                            "olive oil, moderate fish and dairy, and limited red meat. This pattern is strongly "
                            "associated with longevity and reduced chronic disease risk.",
            
            "DASH": "Your diet aligns with the DASH (Dietary Approaches to Stop Hypertension) pattern, "
                   "which emphasizes fruits, vegetables, whole grains, lean proteins, and limited sodium. "
                   "This pattern supports cardiovascular health and longevity.",
            
            "Plant-forward": "Your diet emphasizes plant foods while not necessarily eliminating animal products. "
                            "This flexible approach is associated with longevity benefits while maintaining "
                            "nutritional adequacy.",
            
            "Blue Zone inspired": "Your diet reflects patterns observed in Blue Zones (regions with exceptional longevity), "
                                 "including abundant plant foods, limited meat, and moderate caloric intake.",
            
            "MIND": "Your diet follows the MIND (Mediterranean-DASH Intervention for Neurodegenerative Delay) pattern, "
                   "which combines elements of Mediterranean and DASH diets with specific emphasis on foods "
                   "that support brain health and cognitive function.",
            
            "High protein, lower carb": "Your diet emphasizes protein with moderate fat and limited carbohydrates. "
                                       "While protein adequacy supports muscle maintenance with aging, consider "
                                       "plant diversity and quality of carbohydrate sources for optimal longevity.",
            
            "High fat": "Your diet contains a higher proportion of fat. The quality and sources of fat "
                       "(e.g., olive oil, avocados, nuts vs. processed foods) significantly impact "
                       "how this pattern affects longevity.",
            
            "High carbohydrate": "Your diet emphasizes carbohydrates. The quality of carbohydrate sources "
                                "(whole vs. refined, fiber content) significantly impacts how this pattern "
                                "affects longevity and metabolic health.",
            
            "Mixed/balanced": "Your diet contains a balanced mix of macronutrients without strong emphasis "
                             "in any particular direction. Focus on food quality and plant diversity to "
                             "optimize this pattern for longevity."
        }
        
        return descriptions.get(pattern, "Your dietary pattern has been analyzed based on your reported intake.")
    
    def _get_longevity_alignment_description(self, alignment: str) -> str:
        """Get description for longevity alignment"""
        descriptions = {
            "Strong": "Your current dietary pattern strongly aligns with evidence-based approaches for "
                     "promoting longevity and healthspan. Continue these beneficial practices while "
                     "making minor optimizations as suggested.",
            
            "Moderate": "Your current dietary pattern includes several elements associated with longevity, "
                       "along with some opportunities for optimization. Implementing the suggested "
                       "recommendations could further enhance the longevity-promoting aspects of your diet.",
            
            "Needs improvement": "Your current dietary pattern has significant opportunities for alignment "
                                "with evidence-based approaches for promoting longevity. Implementing the "
                                "suggested recommendations could substantially enhance your nutritional "
                                "foundation for healthy aging."
        }
        
        return descriptions.get(alignment, "Your dietary pattern has been analyzed for alignment with longevity research.")
    
    def _extract_key_findings(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key findings from the nutrition analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of strings containing key findings
        """
        key_findings = []
        
        # Add dietary pattern finding
        dietary_pattern = analysis.get("dietary_pattern", {}).get("current_pattern", "")
        if dietary_pattern:
            key_findings.append(f"Current dietary pattern: {dietary_pattern}")
        
        # Add macronutrient distribution finding
        macros = analysis.get("nutrient_analysis", {}).get("macronutrient_distribution", {})
        if macros:
            key_findings.append(f"Macronutrient ratio: {macros.get('protein_percentage', 0)}% protein, "
                              f"{macros.get('carbohydrate_percentage', 0)}% carbs, "
                              f"{macros.get('fat_percentage', 0)}% fat")
        
        # Add protein finding
        protein_per_kg = analysis.get("nutrient_analysis", {}).get("protein_per_kg", 0)
        if protein_per_kg > 0:
            if protein_per_kg >= self.longevity_nutrients["protein"]["optimal"]:
                key_findings.append(f"Optimal protein intake: {protein_per_kg}g/kg")
            elif protein_per_kg >= self.longevity_nutrients["protein"]["min"]:
                key_findings.append(f"Adequate protein intake: {protein_per_kg}g/kg")
            else:
                key_findings.append(f"Suboptimal protein intake: {protein_per_kg}g/kg")
        
        # Add fiber finding
        fiber_g = analysis.get("nutrient_analysis", {}).get("fiber_g", 0)
        if fiber_g > 0:
            if fiber_g >= self.longevity_nutrients["fiber"]["optimal"]:
                key_findings.append(f"Excellent fiber intake: {fiber_g}g")
            elif fiber_g >= self.longevity_nutrients["fiber"]["min"]:
                key_findings.append(f"Adequate fiber intake: {fiber_g}g")
            else:
                key_findings.append(f"Suboptimal fiber intake: {fiber_g}g")
        
        # Add longevity alignment finding
        longevity_alignment = analysis.get("longevity_alignment", {}).get("overall", "")
        if longevity_alignment:
            key_findings.append(f"Longevity nutrition alignment: {longevity_alignment}")
        
        return key_findings
    
    def _determine_confidence(self, analysis: Dict[str, Any]) -> ConfidenceLevel:
        """
        Determine the confidence level of the nutrition analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            ConfidenceLevel enum representing the confidence level
        """
        # Start with medium confidence
        confidence = ConfidenceLevel.MEDIUM
        
        # Check if we have detailed nutrition data
        has_detailed_data = "nutrient_analysis" in analysis and analysis["nutrient_analysis"]
        
        # Check if we have a clear dietary pattern
        has_dietary_pattern = "dietary_pattern" in analysis and analysis["dietary_pattern"].get("current_pattern")
        
        # Determine confidence based on data completeness
        if has_detailed_data and has_dietary_pattern:
            confidence = ConfidenceLevel.HIGH
        elif not has_detailed_data and not has_dietary_pattern:
            confidence = ConfidenceLevel.LOW
        
        return confidence
