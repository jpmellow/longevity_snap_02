"""
Exercise Agent for Longevity Snapshot App

This module implements a specialized agent for analyzing physical activity data
and providing evidence-based exercise recommendations for longevity.
"""

from typing import Dict, List, Any, Optional
import logging
from .base_agent import BaseAgent, ConfidenceLevel

logger = logging.getLogger("agent.exercise")

class ExerciseAgent(BaseAgent):
    """
    Specialized agent for physical activity analysis and recommendations
    focused on longevity-promoting exercise patterns.
    """
    
    def __init__(self):
        """Initialize the Exercise Agent"""
        super().__init__("Exercise")
        
        # Evidence-based exercise guidelines for longevity
        self.exercise_guidelines = {
            "cardio_minutes": {"min": 150, "optimal": 225, "max": 300, "unit": "minutes/week"},
            "strength_sessions": {"min": 2, "optimal": 3, "max": 4, "unit": "sessions/week"},
            "steps": {"min": 7000, "optimal": 10000, "max": 15000, "unit": "steps/day"},
            "sedentary_breaks": {"min": 2, "optimal": 4, "max": 6, "unit": "breaks/day"}
        }
        
        # Exercise types and their benefits
        self.exercise_benefits = {
            "walking": ["accessibility", "joint-friendly", "cardiovascular", "metabolic"],
            "running": ["cardiovascular", "bone density", "metabolic", "efficiency"],
            "cycling": ["joint-friendly", "cardiovascular", "metabolic", "lower body"],
            "swimming": ["joint-friendly", "full-body", "cardiovascular", "low-impact"],
            "strength_training": ["muscle maintenance", "bone density", "metabolic", "functional"],
            "yoga": ["flexibility", "balance", "stress reduction", "mindfulness"],
            "hiit": ["time-efficiency", "metabolic", "cardiovascular", "adaptability"],
            "pilates": ["core strength", "posture", "balance", "low-impact"]
        }
    
    def _extract_relevant_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract exercise-related data from user data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing relevant exercise data
        """
        relevant_data = {
            "user_profile": {},
            "exercise_data": {}
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
        
        # Extract exercise data
        if "exercise_data" in user_data and user_data["exercise_data"]:
            relevant_data["exercise_data"] = user_data["exercise_data"]
        
        # Extract exercise preferences
        if "preferences" in user_data and user_data["preferences"]:
            if "exercise_time" in user_data["preferences"]:
                relevant_data["user_profile"]["exercise_time_preference"] = user_data["preferences"]["exercise_time"]
        
        # Extract medical history relevant to exercise
        if "medical_history" in user_data and user_data["medical_history"]:
            exercise_relevant_conditions = [
                "arthritis", "heart disease", "hypertension", "diabetes", 
                "respiratory", "back pain", "joint pain", "osteoporosis"
            ]
            relevant_data["user_profile"]["exercise_relevant_conditions"] = [
                condition for condition in user_data["medical_history"]
                if any(rel_condition in condition.lower() for rel_condition in exercise_relevant_conditions)
            ]
        
        return relevant_data
    
    def _analyze_data(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze exercise data to identify patterns and areas for improvement
        
        Args:
            relevant_data: Dictionary containing relevant exercise data
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "activity_level": {},
            "exercise_balance": {},
            "longevity_alignment": {},
            "areas_for_improvement": [],
            "strengths": []
        }
        
        # Extract exercise data
        exercise_data = relevant_data.get("exercise_data", {})
        user_profile = relevant_data.get("user_profile", {})
        
        # Analyze activity level
        if exercise_data:
            # Calculate total weekly sessions
            strength_sessions = exercise_data.get("strength_training", 0)
            cardio_sessions = exercise_data.get("cardio", 0)
            total_sessions = strength_sessions + cardio_sessions
            
            # Estimate weekly minutes (using average duration if available)
            duration = exercise_data.get("duration", 30)  # Default to 30 minutes if not specified
            estimated_minutes = total_sessions * duration
            
            # Determine activity level
            if estimated_minutes >= self.exercise_guidelines["cardio_minutes"]["optimal"]:
                activity_level = "High"
            elif estimated_minutes >= self.exercise_guidelines["cardio_minutes"]["min"]:
                activity_level = "Moderate"
            elif estimated_minutes > 0:
                activity_level = "Low"
            else:
                activity_level = "Sedentary"
            
            analysis["activity_level"] = {
                "level": activity_level,
                "weekly_sessions": total_sessions,
                "estimated_minutes": estimated_minutes,
                "strength_sessions": strength_sessions,
                "cardio_sessions": cardio_sessions
            }
            
            # Analyze exercise balance
            has_cardio = cardio_sessions > 0
            has_strength = strength_sessions > 0
            
            if has_cardio and has_strength:
                balance = "Balanced"
            elif has_cardio:
                balance = "Cardio-dominant"
            elif has_strength:
                balance = "Strength-dominant"
            else:
                balance = "Insufficient data"
            
            analysis["exercise_balance"]["balance"] = balance
            
            # Identify exercise types
            exercise_types = exercise_data.get("types", [])
            analysis["exercise_balance"]["exercise_types"] = exercise_types
            
            # Identify strengths and areas for improvement
            
            # Check cardio volume
            if estimated_minutes >= self.exercise_guidelines["cardio_minutes"]["optimal"]:
                analysis["strengths"].append("Optimal cardio volume for longevity benefits")
            elif estimated_minutes >= self.exercise_guidelines["cardio_minutes"]["min"]:
                analysis["strengths"].append("Adequate cardio volume")
            else:
                analysis["areas_for_improvement"].append("Increase cardio volume to at least 150 minutes weekly")
            
            # Check strength training
            if strength_sessions >= self.exercise_guidelines["strength_sessions"]["optimal"]:
                analysis["strengths"].append("Optimal strength training frequency for muscle maintenance and longevity")
            elif strength_sessions >= self.exercise_guidelines["strength_sessions"]["min"]:
                analysis["strengths"].append("Adequate strength training frequency")
            else:
                analysis["areas_for_improvement"].append("Include at least 2 strength training sessions weekly")
            
            # Check exercise balance
            if balance == "Balanced":
                analysis["strengths"].append("Well-balanced exercise routine including both cardio and strength")
            else:
                if balance == "Cardio-dominant":
                    analysis["areas_for_improvement"].append("Add strength training for muscle preservation and metabolic health")
                elif balance == "Strength-dominant":
                    analysis["areas_for_improvement"].append("Add cardio for cardiovascular and metabolic benefits")
            
            # Check exercise variety
            if exercise_types and len(exercise_types) >= 3:
                analysis["strengths"].append("Good exercise variety supporting multiple fitness domains")
            elif exercise_types and len(exercise_types) > 0:
                analysis["areas_for_improvement"].append("Increase exercise variety to support multiple fitness domains")
            
            # Check intensity
            intensity = exercise_data.get("intensity", "")
            if intensity:
                if intensity.lower() in ["medium", "high"]:
                    analysis["strengths"].append(f"{intensity.capitalize()} intensity supporting fitness adaptations")
                else:
                    analysis["areas_for_improvement"].append("Gradually incorporate some moderate-intensity exercise")
        else:
            analysis["activity_level"] = {
                "level": "Unknown",
                "weekly_sessions": 0,
                "estimated_minutes": 0,
                "strength_sessions": 0,
                "cardio_sessions": 0
            }
            analysis["areas_for_improvement"].append("Begin with light activity and gradually build exercise habits")
        
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
        Generate exercise recommendations based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # Generate recommendations based on areas for improvement
        for area in analysis.get("areas_for_improvement", []):
            if "cardio volume" in area.lower():
                recommendations.append({
                    "category": "physical_activity",
                    "subcategory": "cardio",
                    "action": "increase_cardio_volume",
                    "description": "Gradually increase cardiovascular exercise to at least 150 minutes of moderate-intensity activity weekly",
                    "reasoning": "Regular cardiovascular exercise is strongly associated with reduced all-cause mortality and extended healthspan in longitudinal studies",
                    "implementation": [
                        "Start with 10-minute sessions if currently inactive",
                        "Gradually increase duration by 10% each week",
                        "Choose activities you enjoy for better adherence",
                        "Break up sessions throughout the week (e.g., 5 x 30 minutes)"
                    ],
                    "evidence_category": "clinical_guidelines",
                    "priority": "high"
                })
            
            if "strength training" in area.lower():
                recommendations.append({
                    "category": "physical_activity",
                    "subcategory": "strength",
                    "action": "incorporate_strength_training",
                    "description": "Include at least 2 strength training sessions weekly targeting major muscle groups",
                    "reasoning": "Resistance training preserves muscle mass and function with aging, supports metabolic health, and is associated with reduced mortality risk independent of aerobic exercise",
                    "implementation": [
                        "Start with bodyweight exercises if new to strength training",
                        "Focus on compound movements (squats, push-ups, rows)",
                        "Aim for 2-3 sets of 8-12 repetitions per exercise",
                        "Allow 48 hours between sessions for the same muscle group"
                    ],
                    "evidence_category": "systematic_review",
                    "priority": "high"
                })
            
            if "exercise variety" in area.lower():
                recommendations.append({
                    "category": "physical_activity",
                    "subcategory": "variety",
                    "action": "increase_exercise_variety",
                    "description": "Incorporate a wider variety of movement patterns to support multiple fitness domains",
                    "reasoning": "Exercise variety supports comprehensive fitness development, reduces injury risk, and enhances adherence through reduced monotony",
                    "implementation": [
                        "Include at least one activity focused on cardiovascular fitness",
                        "Include at least one activity focused on strength development",
                        "Add activities that enhance flexibility and balance",
                        "Consider both weight-bearing and non-weight-bearing options"
                    ],
                    "evidence_category": "expert_consensus",
                    "priority": "medium"
                })
            
            if "intensity" in area.lower():
                recommendations.append({
                    "category": "physical_activity",
                    "subcategory": "intensity",
                    "action": "incorporate_moderate_intensity",
                    "description": "Gradually introduce moderate-intensity exercise periods within your current activity",
                    "reasoning": "Moderate-intensity exercise provides substantial health benefits with minimal injury risk, while supporting cardiovascular and metabolic adaptations",
                    "implementation": [
                        "Start with brief intervals (30-60 seconds) of increased effort",
                        "Use the talk test (able to talk but not sing) to gauge moderate intensity",
                        "Gradually increase the duration of moderate-intensity periods",
                        "Consider structured interval training as fitness improves"
                    ],
                    "evidence_category": "randomized_controlled_trial",
                    "priority": "medium"
                })
            
            if "begin with light activity" in area.lower():
                recommendations.append({
                    "category": "physical_activity",
                    "subcategory": "beginner",
                    "action": "start_exercise_habit",
                    "description": "Begin a progressive physical activity program starting with light, enjoyable activities",
                    "reasoning": "Even small amounts of physical activity provide health benefits, with the dose-response curve being steepest at the lower end of activity levels",
                    "implementation": [
                        "Start with daily walking, gradually increasing from 5 to 30 minutes",
                        "Focus on consistency rather than intensity initially",
                        "Choose activities you genuinely enjoy to build sustainable habits",
                        "Consider tracking steps with a goal of eventually reaching 7,000-10,000 daily"
                    ],
                    "evidence_category": "clinical_guidelines",
                    "priority": "high"
                })
        
        # Add general longevity exercise recommendation if few specific ones
        if len(recommendations) < 2:
            recommendations.append({
                "category": "physical_activity",
                "subcategory": "longevity",
                "action": "optimize_longevity_exercise",
                "description": "Optimize your exercise routine for longevity benefits",
                "reasoning": "Specific exercise patterns are consistently associated with extended healthspan and reduced mortality risk in longitudinal studies",
                "implementation": [
                    "Maintain 150-300 minutes of moderate cardiovascular activity weekly",
                    "Include 2-3 strength training sessions weekly targeting major muscle groups",
                    "Add flexibility and balance work, especially important with advancing age",
                    "Break up sedentary time with movement breaks throughout the day"
                ],
                "evidence_category": "systematic_review",
                "priority": "high"
            })
        
        return recommendations
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights based on the exercise analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing insights
        """
        insights = []
        
        # Generate insight about activity level
        activity_level = analysis.get("activity_level", {}).get("level", "")
        if activity_level:
            insights.append({
                "type": "activity_level",
                "title": f"Activity Level: {activity_level}",
                "description": self._get_activity_level_description(activity_level),
                "relevance": "high"
            })
        
        # Generate insight about exercise balance
        balance = analysis.get("exercise_balance", {}).get("balance", "")
        if balance and balance != "Insufficient data":
            insights.append({
                "type": "exercise_balance",
                "title": f"Exercise Balance: {balance}",
                "description": self._get_exercise_balance_description(balance),
                "relevance": "medium"
            })
        
        # Generate insight about exercise types and benefits
        exercise_types = analysis.get("exercise_balance", {}).get("exercise_types", [])
        if exercise_types:
            benefits = []
            for exercise_type in exercise_types:
                if exercise_type.lower() in self.exercise_benefits:
                    benefits.extend(self.exercise_benefits[exercise_type.lower()])
            
            if benefits:
                unique_benefits = list(set(benefits))
                insights.append({
                    "type": "exercise_benefits",
                    "title": "Your Exercise Benefits Profile",
                    "description": f"Your current activities provide benefits for: {', '.join(unique_benefits)}",
                    "relevance": "medium"
                })
        
        # Generate insight about longevity alignment
        longevity_alignment = analysis.get("longevity_alignment", {}).get("overall", "")
        if longevity_alignment:
            insights.append({
                "type": "longevity_alignment",
                "title": f"Longevity Exercise Alignment: {longevity_alignment}",
                "description": self._get_longevity_alignment_description(longevity_alignment),
                "relevance": "high"
            })
        
        return insights
    
    def _get_activity_level_description(self, level: str) -> str:
        """Get description for an activity level"""
        descriptions = {
            "High": "Your current activity level exceeds general exercise guidelines, providing substantial "
                   "health benefits. Research shows that this level of activity is associated with significant "
                   "reductions in all-cause mortality and extended healthspan.",
            
            "Moderate": "Your current activity level meets general exercise guidelines, providing important "
                       "health benefits. This level of activity is associated with reduced risk of chronic "
                       "disease and improved longevity outcomes.",
            
            "Low": "Your current activity level provides some health benefits but falls below general exercise "
                  "guidelines. Gradually increasing your activity could provide substantial additional benefits "
                  "for longevity and healthspan.",
            
            "Sedentary": "Your current activity level is primarily sedentary, which research associates with "
                        "increased health risks. Even small increases in physical activity can provide meaningful "
                        "benefits, with the greatest relative gains coming from moving from sedentary to light activity."
        }
        
        return descriptions.get(level, "Your activity level has been analyzed based on your reported exercise patterns.")
    
    def _get_exercise_balance_description(self, balance: str) -> str:
        """Get description for exercise balance"""
        descriptions = {
            "Balanced": "Your exercise routine includes both cardiovascular and strength components, creating "
                       "a well-rounded approach that supports multiple aspects of fitness and longevity. This "
                       "balanced approach is optimal for healthy aging.",
            
            "Cardio-dominant": "Your exercise routine emphasizes cardiovascular activities, which provide excellent "
                              "benefits for heart health, metabolic function, and endurance. Adding strength training "
                              "would create a more balanced approach to support muscle maintenance and bone health with aging.",
            
            "Strength-dominant": "Your exercise routine emphasizes strength training, which provides excellent benefits "
                                "for muscle maintenance, bone health, and metabolic function. Adding cardiovascular "
                                "activities would create a more balanced approach to support heart health and endurance."
        }
        
        return descriptions.get(balance, "Your exercise balance has been analyzed based on your reported activities.")
    
    def _get_longevity_alignment_description(self, alignment: str) -> str:
        """Get description for longevity alignment"""
        descriptions = {
            "Strong": "Your current exercise pattern strongly aligns with evidence-based approaches for "
                     "promoting longevity and healthspan. Your routine includes key elements associated with "
                     "reduced mortality risk and extended healthy years.",
            
            "Moderate": "Your current exercise pattern includes several elements associated with longevity, "
                       "along with some opportunities for optimization. Implementing the suggested "
                       "recommendations could further enhance the longevity-promoting aspects of your routine.",
            
            "Needs improvement": "Your current exercise pattern has significant opportunities for alignment "
                                "with evidence-based approaches for promoting longevity. Implementing the "
                                "suggested recommendations could substantially enhance your physical activity "
                                "foundation for healthy aging."
        }
        
        return descriptions.get(alignment, "Your exercise pattern has been analyzed for alignment with longevity research.")
    
    def _extract_key_findings(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key findings from the exercise analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of strings containing key findings
        """
        key_findings = []
        
        # Add activity level finding
        activity_level = analysis.get("activity_level", {})
        if activity_level:
            level = activity_level.get("level", "")
            if level:
                key_findings.append(f"Activity level: {level}")
            
            sessions = activity_level.get("weekly_sessions", 0)
            minutes = activity_level.get("estimated_minutes", 0)
            if sessions > 0 or minutes > 0:
                key_findings.append(f"Weekly exercise: {sessions} sessions, ~{minutes} minutes")
        
        # Add exercise balance finding
        balance = analysis.get("exercise_balance", {}).get("balance", "")
        if balance and balance != "Insufficient data":
            key_findings.append(f"Exercise balance: {balance}")
        
        # Add strength training finding
        strength_sessions = analysis.get("activity_level", {}).get("strength_sessions", 0)
        if strength_sessions > 0:
            if strength_sessions >= self.exercise_guidelines["strength_sessions"]["optimal"]:
                key_findings.append(f"Optimal strength training: {strength_sessions} sessions/week")
            elif strength_sessions >= self.exercise_guidelines["strength_sessions"]["min"]:
                key_findings.append(f"Adequate strength training: {strength_sessions} sessions/week")
            else:
                key_findings.append(f"Suboptimal strength training: {strength_sessions} sessions/week")
        
        # Add cardio finding
        estimated_minutes = analysis.get("activity_level", {}).get("estimated_minutes", 0)
        if estimated_minutes > 0:
            if estimated_minutes >= self.exercise_guidelines["cardio_minutes"]["optimal"]:
                key_findings.append(f"Optimal cardio volume: ~{estimated_minutes} minutes/week")
            elif estimated_minutes >= self.exercise_guidelines["cardio_minutes"]["min"]:
                key_findings.append(f"Adequate cardio volume: ~{estimated_minutes} minutes/week")
            else:
                key_findings.append(f"Suboptimal cardio volume: ~{estimated_minutes} minutes/week")
        
        # Add longevity alignment finding
        longevity_alignment = analysis.get("longevity_alignment", {}).get("overall", "")
        if longevity_alignment:
            key_findings.append(f"Longevity exercise alignment: {longevity_alignment}")
        
        return key_findings
    
    def _determine_confidence(self, analysis: Dict[str, Any]) -> ConfidenceLevel:
        """
        Determine the confidence level of the exercise analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            ConfidenceLevel enum representing the confidence level
        """
        # Start with medium confidence
        confidence = ConfidenceLevel.MEDIUM
        
        # Check if we have detailed exercise data
        has_detailed_data = "activity_level" in analysis and analysis["activity_level"].get("level") != "Unknown"
        
        # Check if we have exercise types
        has_exercise_types = "exercise_balance" in analysis and analysis["exercise_balance"].get("exercise_types")
        
        # Determine confidence based on data completeness
        if has_detailed_data and has_exercise_types:
            confidence = ConfidenceLevel.HIGH
        elif not has_detailed_data and not has_exercise_types:
            confidence = ConfidenceLevel.LOW
        
        return confidence
