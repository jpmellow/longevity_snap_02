"""
Personalization Agent for Longevity Snapshot App

This module implements the Personalization Agent which adapts health recommendations
to fit the user's individual context, preferences, and motivation drivers.
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
from enum import Enum
from .base_agent import BaseAgent, ConfidenceLevel

class MotivationDriver(Enum):
    """Enum representing different user motivation drivers"""
    HEALTH_SCARE = "health_scare"
    LONGEVITY = "longevity"
    PERFORMANCE = "performance"
    APPEARANCE = "appearance"
    ENERGY = "energy"
    COGNITIVE = "cognitive"
    MOOD = "mood"
    SOCIAL = "social"
    UNKNOWN = "unknown"

class PersonalizationAgent(BaseAgent):
    """
    Personalization Agent that adapts health recommendations to match users'
    individual contexts, preferences, and motivation drivers.
    """
    
    def __init__(self):
        """Initialize the Personalization Agent"""
        super().__init__("Personalization")
        
        # Define communication styles for different motivation drivers
        self.motivation_styles = {
            MotivationDriver.HEALTH_SCARE: {
                "tone": "supportive but direct",
                "focus": "risk reduction and prevention",
                "framing": "avoiding negative health outcomes",
                "timeframe": "immediate and short-term benefits"
            },
            MotivationDriver.LONGEVITY: {
                "tone": "informative and encouraging",
                "focus": "long-term health optimization",
                "framing": "adding healthy years to life",
                "timeframe": "long-term benefits and cumulative effects"
            },
            MotivationDriver.PERFORMANCE: {
                "tone": "energetic and goal-oriented",
                "focus": "optimization and measurable improvements",
                "framing": "enhancing capabilities and performance",
                "timeframe": "progressive improvements with clear milestones"
            },
            MotivationDriver.APPEARANCE: {
                "tone": "positive and affirming",
                "focus": "visible results and aesthetic benefits",
                "framing": "looking and feeling better",
                "timeframe": "noticeable changes within specific timeframes"
            },
            MotivationDriver.ENERGY: {
                "tone": "uplifting and practical",
                "focus": "daily energy and vitality",
                "framing": "feeling more energetic and productive",
                "timeframe": "immediate and daily benefits"
            },
            MotivationDriver.COGNITIVE: {
                "tone": "intellectually engaging and precise",
                "focus": "brain health and cognitive function",
                "framing": "optimizing mental performance and clarity",
                "timeframe": "both immediate effects and long-term protection"
            },
            MotivationDriver.MOOD: {
                "tone": "empathetic and supportive",
                "focus": "emotional wellbeing and resilience",
                "framing": "feeling better emotionally and psychologically",
                "timeframe": "consistent improvement in daily mood states"
            },
            MotivationDriver.SOCIAL: {
                "tone": "warm and community-oriented",
                "focus": "connection and shared experiences",
                "framing": "enhancing relationships and social wellbeing",
                "timeframe": "building meaningful connections over time"
            }
        }
    
    def _extract_relevant_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data relevant to personalization from the user data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing relevant data for personalization
        """
        relevant_data = {
            "recommendations": [],
            "user_profile": {}
        }
        
        # Extract user profile information
        if "preferences" in user_data:
            relevant_data["user_profile"]["preferences"] = user_data["preferences"]
        
        if "age" in user_data:
            relevant_data["user_profile"]["age"] = user_data["age"]
            
        if "gender" in user_data:
            relevant_data["user_profile"]["gender"] = user_data["gender"]
        
        # Extract activity patterns
        if "exercise_data" in user_data:
            relevant_data["user_profile"]["exercise_data"] = user_data["exercise_data"]
        
        # Extract dietary patterns
        if "nutrition_data" in user_data:
            relevant_data["user_profile"]["nutrition_data"] = user_data["nutrition_data"]
        
        # Extract sleep patterns
        if "sleep_data" in user_data:
            relevant_data["user_profile"]["sleep_data"] = user_data["sleep_data"]
        
        # Extract stress patterns
        if "stress_data" in user_data:
            relevant_data["user_profile"]["stress_data"] = user_data["stress_data"]
        
        # Extract motivation driver if available
        if "preferences" in user_data and user_data["preferences"] and "motivation_driver" in user_data["preferences"]:
            motivation = user_data["preferences"]["motivation_driver"]
            relevant_data["user_profile"]["motivation_driver"] = motivation
        else:
            # Try to infer motivation from goals if available
            if "preferences" in user_data and user_data["preferences"] and "goals" in user_data["preferences"]:
                goals = user_data["preferences"]["goals"]
                relevant_data["user_profile"]["motivation_driver"] = self._infer_motivation_from_goals(goals)
            else:
                relevant_data["user_profile"]["motivation_driver"] = MotivationDriver.UNKNOWN.value
        
        # Extract recommendations from other agents (in a real system, these would come from the Meta-Cognitive Processor)
        # For now, we'll use placeholder recommendations
        relevant_data["recommendations"] = self._get_placeholder_recommendations()
        
        return relevant_data
    
    def _infer_motivation_from_goals(self, goals: List[str]) -> str:
        """
        Infer the user's motivation driver from their health goals
        
        Args:
            goals: List of user's health and wellness goals
            
        Returns:
            String representing the inferred motivation driver
        """
        # Convert goals to lowercase for case-insensitive matching
        goals_lower = [goal.lower() for goal in goals]
        
        # Check for health scare indicators
        health_scare_keywords = ["prevent", "disease", "condition", "risk", "doctor", "medical", "health issue", "avoid", "family history"]
        if any(keyword in " ".join(goals_lower) for keyword in health_scare_keywords):
            return MotivationDriver.HEALTH_SCARE.value
        
        # Check for longevity indicators
        longevity_keywords = ["longevity", "lifespan", "long life", "healthy aging", "live longer", "aging well", "vitality"]
        if any(keyword in " ".join(goals_lower) for keyword in longevity_keywords):
            return MotivationDriver.LONGEVITY.value
        
        # Check for performance indicators
        performance_keywords = ["performance", "athletic", "fitness", "strength", "endurance", "competition", "personal best", "training"]
        if any(keyword in " ".join(goals_lower) for keyword in performance_keywords):
            return MotivationDriver.PERFORMANCE.value
        
        # Check for appearance indicators
        appearance_keywords = ["appearance", "look", "weight loss", "toning", "muscle definition", "physique", "body composition"]
        if any(keyword in " ".join(goals_lower) for keyword in appearance_keywords):
            return MotivationDriver.APPEARANCE.value
        
        # Check for energy indicators
        energy_keywords = ["energy", "fatigue", "tired", "productivity", "focus", "mental clarity", "stamina", "vitality"]
        if any(keyword in " ".join(goals_lower) for keyword in energy_keywords):
            return MotivationDriver.ENERGY.value
        
        # Check for cognitive indicators
        cognitive_keywords = ["brain", "memory", "cognitive", "focus", "concentration", "mental", "thinking", "clarity", "alzheimer's", "dementia"]
        if any(keyword in " ".join(goals_lower) for keyword in cognitive_keywords):
            return MotivationDriver.COGNITIVE.value
        
        # Check for mood indicators
        mood_keywords = ["mood", "happiness", "depression", "anxiety", "stress", "emotional", "mental health", "wellbeing", "feel better"]
        if any(keyword in " ".join(goals_lower) for keyword in mood_keywords):
            return MotivationDriver.MOOD.value
        
        # Check for social indicators
        social_keywords = ["social", "connection", "relationships", "community", "family", "friends", "belonging", "loneliness"]
        if any(keyword in " ".join(goals_lower) for keyword in social_keywords):
            return MotivationDriver.SOCIAL.value
        
        # Default to longevity if no clear pattern is detected
        return MotivationDriver.LONGEVITY.value
    
    def _get_placeholder_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get placeholder recommendations for testing
        
        Returns:
            List of dictionaries containing recommendations
        """
        return [
            {
                "type": "medical",
                "category": "sleep",
                "action": "improve_sleep_duration",
                "description": "Aim for 7-9 hours of quality sleep per night for optimal health",
                "priority": "high",
                "reasoning": "Insufficient sleep duration increases risk of cognitive impairment, mood disorders, and metabolic dysfunction",
                "evidence_category": "clinical_guidelines",
                "source_agent": "medical_reasoning"
            },
            {
                "type": "medical",
                "category": "physical_activity",
                "action": "increase_physical_activity",
                "description": "Gradually increase physical activity to at least 150 minutes of moderate-intensity exercise per week",
                "priority": "high",
                "reasoning": "Insufficient physical activity increases risk of cardiovascular disease, type 2 diabetes, and all-cause mortality",
                "evidence_category": "clinical_guidelines",
                "source_agent": "medical_reasoning"
            },
            {
                "type": "medical",
                "category": "stress_management",
                "action": "stress_reduction",
                "description": "Implement evidence-based stress management techniques such as mindfulness meditation, deep breathing exercises, or professional counseling",
                "priority": "medium",
                "reasoning": "High stress levels are associated with increased risk of cardiovascular disease, immune dysfunction, and mental health disorders",
                "evidence_category": "systematic_review",
                "source_agent": "medical_reasoning"
            }
        ]
    
    def _analyze_data(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the relevant data for personalization
        
        Args:
            relevant_data: Dictionary containing relevant data for personalization
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "user_profile": relevant_data["user_profile"],
            "motivation_driver": relevant_data["user_profile"].get("motivation_driver", MotivationDriver.UNKNOWN.value),
            "communication_style": {},
            "prioritized_recommendations": [],
            "personalization_factors": [],
            "feasibility_assessments": []
        }
        
        # Determine communication style based on motivation driver
        motivation = analysis["motivation_driver"]
        try:
            driver_enum = MotivationDriver(motivation)
            if driver_enum in self.motivation_styles:
                analysis["communication_style"] = self.motivation_styles[driver_enum]
            else:
                analysis["communication_style"] = self.motivation_styles[MotivationDriver.LONGEVITY]
        except (ValueError, KeyError):
            # Default to longevity style if motivation is not recognized
            analysis["communication_style"] = self.motivation_styles[MotivationDriver.LONGEVITY]
        
        # Identify personalization factors
        analysis["personalization_factors"] = self._identify_personalization_factors(relevant_data["user_profile"])
        
        # Assess feasibility of recommendations
        recommendations = relevant_data["recommendations"]
        for rec in recommendations:
            feasibility = self._assess_recommendation_feasibility(rec, relevant_data["user_profile"])
            analysis["feasibility_assessments"].append({
                "recommendation": rec,
                "feasibility_score": feasibility["score"],
                "barriers": feasibility["barriers"],
                "facilitators": feasibility["facilitators"]
            })
        
        # Prioritize recommendations based on impact and feasibility
        analysis["prioritized_recommendations"] = self._prioritize_recommendations(
            recommendations, 
            analysis["feasibility_assessments"]
        )
        
        return analysis
    
    def _identify_personalization_factors(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify factors that should influence personalization
        
        Args:
            user_profile: Dictionary containing user profile information
            
        Returns:
            List of dictionaries containing personalization factors
        """
        factors = []
        
        # Check for dietary preferences
        if "preferences" in user_profile and "diet" in user_profile["preferences"]:
            diet = user_profile["preferences"]["diet"]
            factors.append({
                "type": "dietary_preference",
                "value": diet,
                "impact": "nutrition_recommendations"
            })
        
        # Check for exercise time preferences
        if "preferences" in user_profile and "exercise_time" in user_profile["preferences"]:
            exercise_time = user_profile["preferences"]["exercise_time"]
            factors.append({
                "type": "exercise_time_preference",
                "value": exercise_time,
                "impact": "physical_activity_recommendations"
            })
        
        # Check for sleep time preferences
        if "preferences" in user_profile and "sleep_time" in user_profile["preferences"]:
            sleep_time = user_profile["preferences"]["sleep_time"]
            factors.append({
                "type": "sleep_time_preference",
                "value": sleep_time,
                "impact": "sleep_recommendations"
            })
        
        # Check for age-related factors
        if "age" in user_profile:
            age = user_profile["age"]
            age_group = "older_adult" if age >= 65 else "adult"
            factors.append({
                "type": "age_group",
                "value": age_group,
                "impact": "all_recommendations"
            })
        
        # Check for exercise experience level
        if "exercise_data" in user_profile:
            exercise_data = user_profile["exercise_data"]
            weekly_sessions = 0
            if "strength_training" in exercise_data:
                weekly_sessions += exercise_data["strength_training"]
            if "cardio" in exercise_data:
                weekly_sessions += exercise_data["cardio"]
            
            experience_level = "beginner"
            if weekly_sessions >= 5:
                experience_level = "advanced"
            elif weekly_sessions >= 3:
                experience_level = "intermediate"
            
            factors.append({
                "type": "exercise_experience",
                "value": experience_level,
                "impact": "physical_activity_recommendations"
            })
        
        return factors
    
    def _assess_recommendation_feasibility(self, recommendation: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the feasibility of a recommendation for the user
        
        Args:
            recommendation: Dictionary containing recommendation details
            user_profile: Dictionary containing user profile information
            
        Returns:
            Dictionary with feasibility assessment
        """
        assessment = {
            "score": 0.0,  # 0.0 to 1.0, where 1.0 is highly feasible
            "barriers": [],
            "facilitators": []
        }
        
        # Base score starts at 0.5 (neutral)
        score = 0.5
        
        # Analyze by recommendation category
        category = recommendation.get("category", "")
        
        # Sleep recommendations
        if category == "sleep":
            if "sleep_data" in user_profile:
                sleep_data = user_profile["sleep_data"]
                
                # Check if already close to target
                if "average_duration" in sleep_data and sleep_data["average_duration"] >= 6.5:
                    score += 0.2
                    assessment["facilitators"].append("Already close to recommended sleep duration")
                elif "average_duration" in sleep_data and sleep_data["average_duration"] < 5.5:
                    score -= 0.1
                    assessment["barriers"].append("Currently far from recommended sleep duration")
                
                # Check consistency as an indicator of sleep habits
                if "bedtime_consistency" in sleep_data:
                    consistency = sleep_data["bedtime_consistency"]
                    if consistency in ["high", "excellent"]:
                        score += 0.1
                        assessment["facilitators"].append("Already has consistent sleep schedule")
                    elif consistency in ["low", "poor"]:
                        score -= 0.1
                        assessment["barriers"].append("Irregular sleep schedule may make implementation challenging")
            
            # Check for sleep time preferences
            if "preferences" in user_profile and "sleep_time" in user_profile["preferences"]:
                score += 0.1
                assessment["facilitators"].append("Has established sleep time preference")
        
        # Physical activity recommendations
        elif category == "physical_activity":
            if "exercise_data" in user_profile:
                exercise_data = user_profile["exercise_data"]
                
                # Check current activity level
                weekly_sessions = 0
                if "strength_training" in exercise_data:
                    weekly_sessions += exercise_data["strength_training"]
                if "cardio" in exercise_data:
                    weekly_sessions += exercise_data["cardio"]
                
                if weekly_sessions >= 2:
                    score += 0.2
                    assessment["facilitators"].append("Already somewhat active, easier to increase")
                elif weekly_sessions == 0:
                    score -= 0.2
                    assessment["barriers"].append("Currently inactive, may face initial resistance")
                
                # Check intensity preference
                if "intensity" in exercise_data:
                    intensity = exercise_data["intensity"]
                    if intensity in ["medium", "high"]:
                        score += 0.1
                        assessment["facilitators"].append("Comfortable with moderate intensity exercise")
            
            # Check for exercise time preferences
            if "preferences" in user_profile and "exercise_time" in user_profile["preferences"]:
                score += 0.1
                assessment["facilitators"].append("Has established exercise time preference")
        
        # Stress management recommendations
        elif category == "stress_management":
            if "stress_data" in user_profile:
                stress_data = user_profile["stress_data"]
                
                # Check if they already use coping mechanisms
                if "coping_mechanisms" in stress_data and stress_data["coping_mechanisms"]:
                    score += 0.2
                    assessment["facilitators"].append("Already uses some stress management techniques")
                
                # Very high stress might indicate both urgency and difficulty
                if "level" in stress_data and stress_data["level"] >= 8:
                    score -= 0.1
                    assessment["barriers"].append("Very high stress levels may make new habits challenging")
                    
                    # But also add urgency as a facilitator
                    assessment["facilitators"].append("High stress creates urgency for change")
        
        # Nutrition recommendations
        elif category == "nutrition":
            if "nutrition_data" in user_profile:
                # Having detailed nutrition data suggests awareness and monitoring
                score += 0.1
                assessment["facilitators"].append("Already tracks nutrition data")
            
            # Check for dietary preferences
            if "preferences" in user_profile and "diet" in user_profile["preferences"]:
                score += 0.1
                assessment["facilitators"].append("Has established dietary preferences")
        
        # Adjust based on priority
        priority = recommendation.get("priority", "medium")
        if priority == "high":
            score += 0.1  # High priority recommendations may get more attention
        
        # Adjust based on motivation driver alignment
        motivation = user_profile.get("motivation_driver", MotivationDriver.UNKNOWN.value)
        score += self._calculate_motivation_alignment(recommendation, motivation)
        
        # Ensure score is between 0.0 and 1.0
        assessment["score"] = max(0.0, min(1.0, score))
        
        return assessment
    
    def _calculate_motivation_alignment(self, recommendation: Dict[str, Any], motivation: str) -> float:
        """
        Calculate how well a recommendation aligns with the user's motivation driver
        
        Args:
            recommendation: Dictionary containing recommendation details
            motivation: String representing the user's motivation driver
            
        Returns:
            Float representing alignment score adjustment (-0.2 to +0.2)
        """
        category = recommendation.get("category", "")
        
        try:
            motivation_enum = MotivationDriver(motivation)
        except ValueError:
            return 0.0  # No adjustment if motivation is not recognized
        
        # Health scare motivation
        if motivation_enum == MotivationDriver.HEALTH_SCARE:
            if category in ["cardiovascular_health", "weight_management", "preventive_care"]:
                return 0.2  # Strong alignment
            elif category in ["stress_management", "sleep"]:
                return 0.1  # Moderate alignment
        
        # Longevity motivation
        elif motivation_enum == MotivationDriver.LONGEVITY:
            if category in ["physical_activity", "nutrition", "sleep", "stress_management"]:
                return 0.2  # Strong alignment
            elif category in ["preventive_care", "cardiovascular_health"]:
                return 0.1  # Moderate alignment
        
        # Performance motivation
        elif motivation_enum == MotivationDriver.PERFORMANCE:
            if category in ["physical_activity", "cardiorespiratory_fitness"]:
                return 0.2  # Strong alignment
            elif category in ["nutrition", "sleep", "recovery"]:
                return 0.1  # Moderate alignment
        
        # Appearance motivation
        elif motivation_enum == MotivationDriver.APPEARANCE:
            if category in ["weight_management", "physical_activity"]:
                return 0.2  # Strong alignment
            elif category in ["nutrition", "sleep"]:
                return 0.1  # Moderate alignment
        
        # Energy motivation
        elif motivation_enum == MotivationDriver.ENERGY:
            if category in ["sleep", "stress_management", "nutrition"]:
                return 0.2  # Strong alignment
            elif category in ["physical_activity", "recovery"]:
                return 0.1  # Moderate alignment
        
        # Cognitive motivation
        elif motivation_enum == MotivationDriver.COGNITIVE:
            if category in ["sleep", "physical_activity", "stress_management", "nutrition"]:
                return 0.2  # Strong alignment
            elif category in ["cognitive_training"]:
                return 0.1  # Moderate alignment
        
        # Mood motivation
        elif motivation_enum == MotivationDriver.MOOD:
            if category in ["stress_management", "sleep", "physical_activity", "nutrition"]:
                return 0.2  # Strong alignment
            elif category in ["mindfulness", "relaxation"]:
                return 0.1  # Moderate alignment
        
        # Social motivation
        elif motivation_enum == MotivationDriver.SOCIAL:
            if category in ["social_connections", "community_engagement"]:
                return 0.2  # Strong alignment
            elif category in ["physical_activity", "group_fitness"]:
                return 0.1  # Moderate alignment
        
        return 0.0  # Neutral alignment
    
    def _prioritize_recommendations(self, recommendations: List[Dict[str, Any]], 
                                 feasibility_assessments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritize recommendations based on impact and feasibility
        
        Args:
            recommendations: List of dictionaries containing recommendations
            feasibility_assessments: List of dictionaries containing feasibility assessments
            
        Returns:
            List of dictionaries containing prioritized recommendations
        """
        # Create a dictionary mapping recommendations to their feasibility assessments
        feasibility_map = {
            assessment["recommendation"]["action"]: assessment 
            for assessment in feasibility_assessments
        }
        
        # Create a list of recommendations with their feasibility scores
        prioritized = []
        for rec in recommendations:
            action = rec.get("action", "")
            if action in feasibility_map:
                assessment = feasibility_map[action]
                
                # Calculate a combined priority score (0.0 to 1.0)
                priority_value = 0.5  # Default medium priority
                if rec.get("priority") == "high":
                    priority_value = 1.0
                elif rec.get("priority") == "low":
                    priority_value = 0.3
                
                # Combine priority with feasibility
                combined_score = (priority_value * 0.6) + (assessment["score"] * 0.4)
                
                prioritized.append({
                    "recommendation": rec,
                    "feasibility": assessment,
                    "combined_score": combined_score
                })
        
        # Sort by combined score (highest first)
        prioritized.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return prioritized
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized recommendations based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing personalized recommendations
        """
        personalized_recommendations = []
        
        # Get communication style based on motivation driver
        communication_style = analysis["communication_style"]
        
        # Process each prioritized recommendation
        for item in analysis["prioritized_recommendations"]:
            original_rec = item["recommendation"]
            feasibility = item["feasibility"]
            
            # Create a personalized version of the recommendation
            personalized_rec = {
                "original_action": original_rec["action"],
                "category": original_rec["category"],
                "personalized_action": self._personalize_action(original_rec, analysis),
                "personalized_description": self._personalize_description(
                    original_rec, 
                    communication_style,
                    analysis["user_profile"]
                ),
                "implementation_steps": self._create_implementation_steps(
                    original_rec, 
                    feasibility,
                    analysis["user_profile"]
                ),
                "barriers": feasibility["barriers"],
                "facilitators": feasibility["facilitators"],
                "motivation_alignment": self._get_motivation_alignment_message(
                    original_rec["category"],
                    analysis["motivation_driver"]
                ),
                "feasibility_score": feasibility["score"],
                "priority": original_rec.get("priority", "medium"),
                "source_agent": original_rec.get("source_agent", "unknown")
            }
            
            personalized_recommendations.append(personalized_rec)
        
        return personalized_recommendations
    
    def _personalize_action(self, recommendation: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Create a personalized action statement based on the recommendation and user profile
        
        Args:
            recommendation: Dictionary containing recommendation details
            analysis: Dictionary containing analysis results
            
        Returns:
            String containing personalized action
        """
        action = recommendation["action"]
        category = recommendation["category"]
        user_profile = analysis["user_profile"]
        
        # Sleep recommendations
        if category == "sleep":
            if action == "improve_sleep_duration":
                if "sleep_data" in user_profile and "average_duration" in user_profile["sleep_data"]:
                    current_duration = user_profile["sleep_data"]["average_duration"]
                    if current_duration < 6:
                        return f"Gradually increase sleep duration from {current_duration} to 7-8 hours"
                    elif current_duration > 9:
                        return f"Optimize sleep duration from {current_duration} to 7-9 hours"
                    else:
                        return "Maintain consistent 7-9 hour sleep schedule"
                else:
                    return "Establish a consistent 7-9 hour sleep schedule"
            
            elif action == "improve_sleep_quality":
                return "Create an optimal sleep environment and pre-sleep routine"
        
        # Physical activity recommendations
        elif category == "physical_activity":
            if action == "increase_physical_activity":
                if "exercise_data" in user_profile:
                    exercise_data = user_profile["exercise_data"]
                    weekly_sessions = 0
                    if "strength_training" in exercise_data:
                        weekly_sessions += exercise_data["strength_training"]
                    if "cardio" in exercise_data:
                        weekly_sessions += exercise_data["cardio"]
                    
                    if weekly_sessions == 0:
                        return "Begin with 10-minute daily walks and gradually build up activity"
                    elif weekly_sessions < 3:
                        return f"Build on your current {weekly_sessions} weekly sessions to reach 150 minutes of activity"
                    else:
                        return "Optimize your current exercise routine for balanced fitness"
                else:
                    return "Begin a progressive physical activity program"
        
        # Stress management recommendations
        elif category == "stress_management":
            if action == "stress_reduction":
                if "stress_data" in user_profile and "coping_mechanisms" in user_profile["stress_data"]:
                    coping = user_profile["stress_data"]["coping_mechanisms"]
                    if coping and len(coping) > 0:
                        return f"Enhance your stress management toolkit by building on {coping[0]}"
                    else:
                        return "Develop a personalized stress management toolkit"
                else:
                    return "Develop a personalized stress management toolkit"
        
        # If no specific personalization rules match, return a slightly modified version of the original
        return f"Personalized {' '.join(action.split('_'))}"
    
    def _personalize_description(self, recommendation: Dict[str, Any], 
                               communication_style: Dict[str, str],
                               user_profile: Dict[str, Any]) -> str:
        """
        Create a personalized description based on the recommendation and communication style
        
        Args:
            recommendation: Dictionary containing recommendation details
            communication_style: Dictionary containing communication style details
            user_profile: Dictionary containing user profile information
            
        Returns:
            String containing personalized description
        """
        original_description = recommendation.get("description", "")
        category = recommendation.get("category", "")
        tone = communication_style.get("tone", "supportive")
        focus = communication_style.get("focus", "health optimization")
        framing = communication_style.get("framing", "improving health outcomes")
        timeframe = communication_style.get("timeframe", "progressive improvements")
        
        # Start with the base description
        description = original_description
        
        # Add tone-appropriate opening
        if tone == "supportive but direct":
            opener = "It's important that you "
        elif tone == "informative and encouraging":
            opener = "Research shows that you can optimize your longevity by "
        elif tone == "energetic and goal-oriented":
            opener = "To maximize your performance, focus on "
        elif tone == "positive and affirming":
            opener = "You'll look and feel your best when you "
        elif tone == "uplifting and practical":
            opener = "To boost your daily energy, "
        elif tone == "intellectually engaging and precise":
            opener = "To optimize your cognitive function, "
        elif tone == "empathetic and supportive":
            opener = "To improve your emotional wellbeing, "
        elif tone == "warm and community-oriented":
            opener = "To enhance your social connections, "
        else:
            opener = "Consider "
        
        # Create personalized description based on category and communication style
        if category == "sleep":
            if "sleep_data" in user_profile and "average_duration" in user_profile["sleep_data"]:
                current_duration = user_profile["sleep_data"]["average_duration"]
                target = "7-9 hours"
                
                if framing == "avoiding negative health outcomes":
                    description = f"{opener}prioritizing {target} of quality sleep. Consistently sleeping less than {current_duration} hours is linked to increased risk of cognitive decline, metabolic disorders, and immune dysfunction."
                elif framing == "adding healthy years to life":
                    description = f"{opener}optimizing your sleep to {target} per night. Quality sleep is a cornerstone of longevity, supporting cellular repair, brain health, and metabolic function."
                elif framing == "enhancing capabilities and performance":
                    description = f"{opener}getting {target} of quality sleep. Optimal sleep dramatically improves cognitive performance, reaction time, and physical recovery."
                elif framing == "looking and feeling better":
                    description = f"{opener}getting {target} of quality sleep. Proper sleep reduces under-eye circles, improves skin clarity, and helps maintain a healthy weight."
                elif framing == "feeling more energetic and productive":
                    description = f"{opener}achieving {target} of quality sleep. Proper sleep is your foundation for all-day energy, mood stability, and productivity."
                elif framing == "optimizing mental performance and clarity":
                    description = f"{opener}getting {target} of quality sleep. Quality sleep is essential for cognitive function, memory consolidation, and mental clarity."
                elif framing == "feeling better emotionally and psychologically":
                    description = f"{opener}prioritizing {target} of quality sleep. Proper sleep regulates emotional processing and significantly improves mood stability."
                elif framing == "enhancing relationships and social wellbeing":
                    description = f"{opener}getting {target} of quality sleep. Quality sleep improves emotional regulation and social interactions."
                else:
                    description = f"{opener}aiming for {target} of quality sleep for optimal health."
        
        elif category == "physical_activity":
            if framing == "avoiding negative health outcomes":
                description = f"{opener}incorporating regular physical activity into your routine. A sedentary lifestyle significantly increases risk of cardiovascular disease, diabetes, and premature mortality."
            elif framing == "adding healthy years to life":
                description = f"{opener}making consistent physical activity a cornerstone of your longevity strategy. Regular exercise is one of the most powerful predictors of healthy lifespan."
            elif framing == "enhancing capabilities and performance":
                description = f"{opener}following a structured exercise program. Proper training progressively enhances your strength, endurance, and functional capabilities."
            elif framing == "looking and feeling better":
                description = f"{opener}engaging in regular physical activity. Exercise sculpts your physique, improves posture, and gives you a healthy, vibrant appearance."
            elif framing == "feeling more energetic and productive":
                description = f"{opener}moving your body consistently. Regular physical activity boosts energy levels, improves mood, and enhances focus throughout the day."
            elif framing == "optimizing mental performance and clarity":
                description = f"{opener}engaging in regular physical activity. Exercise enhances brain blood flow, neurogenesis, and cognitive function."
            elif framing == "feeling better emotionally and psychologically":
                description = f"{opener}engaging in regular physical activity. Exercise releases endorphins and improves mood both acutely and chronically."
            elif framing == "enhancing relationships and social wellbeing":
                description = f"{opener}engaging in group fitness activities. Exercise can be a social opportunity and enhances your energy for meaningful connections."
            else:
                description = f"{opener}incorporating regular physical activity for overall health."
        
        elif category == "stress_management":
            if framing == "avoiding negative health outcomes":
                description = f"{opener}implementing effective stress management techniques. Chronic unmanaged stress accelerates aging and increases risk of cardiovascular disease and immune dysfunction."
            elif framing == "adding healthy years to life":
                description = f"{opener}developing a comprehensive stress management practice. Effective stress regulation is a key longevity pathway that protects cellular health and brain function."
            elif framing == "enhancing capabilities and performance":
                description = f"{opener}mastering stress management techniques. Optimal stress regulation improves decision-making, focus, and recovery between training sessions."
            elif framing == "looking and feeling better":
                description = f"{opener}prioritizing stress management. Reduced stress improves skin clarity, reduces tension in your face and body, and helps maintain a healthy weight."
            elif framing == "feeling more energetic and productive":
                description = f"{opener}implementing daily stress management practices. Effective stress regulation prevents energy depletion and mental fatigue."
            elif framing == "optimizing mental performance and clarity":
                description = f"{opener}protecting your brain from chronic stress. Stress management optimizes cognitive performance and protects against neurodegenerative diseases."
            elif framing == "feeling better emotionally and psychologically":
                description = f"{opener}enhancing your emotional regulation. Stress management improves emotional wellbeing and psychological resilience."
            elif framing == "enhancing relationships and social wellbeing":
                description = f"{opener}improving your capacity for positive social engagement. Stress management enhances your emotional regulation and social interactions."
            else:
                description = f"{opener}developing effective stress management techniques for better health."
        
        # Add timeframe-appropriate closing if not already included
        if timeframe == "immediate and short-term benefits" and "immediate" not in description.lower():
            description += " You may notice improvements within days of implementing this change."
        elif timeframe == "long-term benefits and cumulative effects" and "long-term" not in description.lower():
            description += " The benefits compound over time, contributing significantly to your long-term health."
        elif timeframe == "progressive improvements with clear milestones" and "progress" not in description.lower():
            description += " Track your progress weekly to see measurable improvements."
        elif timeframe == "noticeable changes within specific timeframes" and "notice" not in description.lower():
            description += " Most people notice visible changes within 3-4 weeks of consistent implementation."
        elif timeframe == "immediate and daily benefits" and "daily" not in description.lower():
            description += " You'll likely experience day-to-day improvements in how you feel."
        elif timeframe == "both immediate effects and long-term protection" and "immediate" not in description.lower():
            description += " You may notice both immediate cognitive improvements and long-term protection against neurodegenerative diseases."
        elif timeframe == "consistent improvement in daily mood states" and "consistent" not in description.lower():
            description += " You can expect consistent improvement in your daily mood states with regular practice."
        elif timeframe == "building meaningful connections over time" and "building" not in description.lower():
            description += " You'll build meaningful connections over time as you engage in social activities and strengthen your relationships."
        
        return description
    
    def _create_implementation_steps(self, recommendation: Dict[str, Any], 
                                   feasibility: Dict[str, Any],
                                   user_profile: Dict[str, Any]) -> List[str]:
        """
        Create personalized implementation steps for a recommendation
        
        Args:
            recommendation: Dictionary containing recommendation details
            feasibility: Dictionary containing feasibility assessment
            user_profile: Dictionary containing user profile information
            
        Returns:
            List of strings containing implementation steps
        """
        category = recommendation.get("category", "")
        action = recommendation.get("action", "")
        barriers = feasibility.get("barriers", [])
        
        # Sleep recommendations
        if category == "sleep":
            if action == "improve_sleep_duration":
                steps = [
                    "Set a consistent bedtime and wake time, even on weekends",
                    "Create a relaxing pre-sleep routine (e.g., reading, gentle stretching)",
                    "Make your bedroom dark, quiet, and cool"
                ]
                
                # Add steps to address specific barriers
                if any("irregular" in barrier.lower() for barrier in barriers):
                    steps.append("Use a sleep tracking app to monitor your progress")
                
                # Personalize based on preferences
                if "preferences" in user_profile and "sleep_time" in user_profile["preferences"]:
                    sleep_time = user_profile["preferences"]["sleep_time"]
                    steps.append(f"Align your schedule with your preferred {sleep_time} sleep time")
                
                return steps
        
        # Physical activity recommendations
        elif category == "physical_activity":
            if action == "increase_physical_activity":
                # Check current activity level
                beginner = True
                if "exercise_data" in user_profile:
                    exercise_data = user_profile["exercise_data"]
                    weekly_sessions = 0
                    if "strength_training" in exercise_data:
                        weekly_sessions += exercise_data["strength_training"]
                    if "cardio" in exercise_data:
                        weekly_sessions += exercise_data["cardio"]
                    
                    beginner = weekly_sessions < 2
                
                if beginner:
                    steps = [
                        "Start with 10-15 minute walks daily",
                        "Gradually increase duration by 5 minutes each week",
                        "Add simple bodyweight exercises (squats, wall push-ups) twice weekly",
                        "Focus on consistency rather than intensity initially"
                    ]
                else:
                    steps = [
                        "Ensure your weekly activity includes both cardio and strength training",
                        "Gradually increase duration or intensity of current workouts",
                        "Add one additional activity session per week",
                        "Include recovery days between intense workouts"
                    ]
                
                # Personalize based on preferences
                if "preferences" in user_profile and "exercise_time" in user_profile["preferences"]:
                    exercise_time = user_profile["preferences"]["exercise_time"]
                    steps.append(f"Schedule workouts during your preferred {exercise_time} time")
                
                return steps
        
        # Stress management recommendations
        elif category == "stress_management":
            if action == "stress_reduction":
                # Check if they already use coping mechanisms
                has_coping = False
                if "stress_data" in user_profile and "coping_mechanisms" in user_profile["stress_data"]:
                    has_coping = len(user_profile["stress_data"]["coping_mechanisms"]) > 0
                
                if has_coping:
                    existing = user_profile["stress_data"]["coping_mechanisms"][0]
                    steps = [
                        f"Continue your practice of {existing}",
                        "Add a 5-minute breathing exercise to your morning routine",
                        "Identify your top 3 stress triggers and create specific plans for each",
                        "Schedule short breaks throughout your day for stress reset"
                    ]
                else:
                    steps = [
                        "Begin with a simple 5-minute daily breathing practice",
                        "Identify your top 3 stress triggers",
                        "Try a guided meditation app for 10 minutes before bed",
                        "Consider a weekly nature walk or other pleasant activity"
                    ]
                
                return steps
        
        # Default implementation steps if no specific rules match
        return [
            "Start with small, manageable changes",
            "Track your progress to stay motivated",
            "Build gradually over time",
            "Adjust as needed based on your results"
        ]
    
    def _get_motivation_alignment_message(self, category: str, motivation: str) -> str:
        """
        Create a message explaining how the recommendation aligns with the user's motivation
        
        Args:
            category: String representing the recommendation category
            motivation: String representing the user's motivation driver
            
        Returns:
            String containing motivation alignment message
        """
        try:
            motivation_enum = MotivationDriver(motivation)
        except ValueError:
            motivation_enum = MotivationDriver.UNKNOWN
        
        # Health scare motivation
        if motivation_enum == MotivationDriver.HEALTH_SCARE:
            if category in ["cardiovascular_health", "weight_management"]:
                return "This change directly addresses your health concerns by reducing disease risk factors"
            elif category == "sleep":
                return "Improving sleep significantly reduces your risk of developing serious health conditions"
            elif category == "physical_activity":
                return "Regular physical activity is one of the most effective ways to prevent disease progression"
            elif category == "stress_management":
                return "Managing stress effectively reduces inflammation and improves immune function"
            elif category == "nutrition":
                return "These dietary changes directly support risk reduction for common health conditions"
            else:
                return "This recommendation supports your goal of addressing health concerns"
        
        # Longevity motivation
        elif motivation_enum == MotivationDriver.LONGEVITY:
            if category == "sleep":
                return "Quality sleep is a fundamental pillar of longevity, supporting cellular repair and brain health"
            elif category == "physical_activity":
                return "Regular physical activity is one of the strongest predictors of healthy lifespan"
            elif category == "stress_management":
                return "Effective stress management protects your telomeres and slows biological aging"
            elif category == "nutrition":
                return "This dietary pattern is consistently associated with exceptional longevity in population studies"
            else:
                return "This recommendation supports your goal of optimizing longevity"
        
        # Performance motivation
        elif motivation_enum == MotivationDriver.PERFORMANCE:
            if category == "sleep":
                return "Optimal sleep dramatically improves reaction time, decision making, and physical recovery"
            elif category == "physical_activity":
                return "A structured exercise program progressively enhances your strength, endurance, and capabilities"
            elif category == "stress_management":
                return "Stress regulation improves focus, decision-making, and recovery between training sessions"
            elif category == "nutrition":
                return "This nutrition strategy optimizes energy availability and recovery for enhanced performance"
            else:
                return "This recommendation supports your goal of optimizing performance"
        
        # Appearance motivation
        elif motivation_enum == MotivationDriver.APPEARANCE:
            if category == "sleep":
                return "Quality sleep reduces under-eye circles, improves skin clarity, and helps maintain a healthy weight"
            elif category == "physical_activity":
                return "Regular exercise sculpts your physique, improves posture, and gives you a healthy, vibrant appearance"
            elif category == "stress_management":
                return "Stress management improves skin clarity, reduces tension in your face and body, and helps maintain weight"
            elif category == "nutrition":
                return "This dietary approach supports healthy body composition and skin vitality"
            else:
                return "This recommendation supports your goal of enhancing your appearance"
        
        # Energy motivation
        elif motivation_enum == MotivationDriver.ENERGY:
            if category == "sleep":
                return "Quality sleep is your foundation for all-day energy, mood stability, and productivity"
            elif category == "physical_activity":
                return "Regular physical activity boosts energy levels, improves mood, and enhances focus throughout the day"
            elif category == "stress_management":
                return "Effective stress regulation prevents energy depletion and mental fatigue"
            elif category == "nutrition":
                return "This eating pattern optimizes stable energy levels throughout the day"
            else:
                return "This recommendation supports your goal of increasing daily energy"
        
        # Cognitive motivation
        elif motivation_enum == MotivationDriver.COGNITIVE:
            if category == "sleep":
                return "Quality sleep is essential for memory consolidation, cognitive processing, and brain health"
            elif category == "physical_activity":
                return "Regular exercise enhances brain blood flow, neurogenesis, and cognitive function"
            elif category == "stress_management":
                return "Stress management protects brain structures and optimizes cognitive performance"
            elif category == "nutrition":
                return "This dietary pattern includes key nutrients that support brain health and cognitive function"
            else:
                return "This recommendation supports your goal of optimizing cognitive function"
        
        # Mood motivation
        elif motivation_enum == MotivationDriver.MOOD:
            if category == "sleep":
                return "Quality sleep regulates emotional processing and significantly improves mood stability"
            elif category == "physical_activity":
                return "Regular exercise releases endorphins and improves mood both acutely and chronically"
            elif category == "stress_management":
                return "These practices directly enhance emotional regulation and psychological wellbeing"
            elif category == "nutrition":
                return "This dietary approach includes nutrients that support neurotransmitter production and mood regulation"
            else:
                return "This recommendation supports your goal of enhancing emotional wellbeing"
        
        # Social motivation
        elif motivation_enum == MotivationDriver.SOCIAL:
            if category == "sleep":
                return "Quality sleep improves emotional regulation and social interactions"
            elif category == "physical_activity":
                return "Regular activity can be a social opportunity and enhances your energy for meaningful connections"
            elif category == "stress_management":
                return "Stress management improves your capacity for positive social engagement"
            elif category == "nutrition":
                return "This approach supports energy and wellbeing for social activities and connections"
            else:
                return "This recommendation supports your goal of enhancing social connections"
        
        # Default message
        return "This recommendation is tailored to support your health goals"
    
    def _get_motivation_description(self, motivation: str) -> str:
        """
        Get a description of the user's motivation driver
        
        Args:
            motivation: String representing the user's motivation driver
            
        Returns:
            String containing motivation description
        """
        try:
            motivation_enum = MotivationDriver(motivation)
        except ValueError:
            return "Your health recommendations have been personalized based on your profile"
        
        if motivation_enum == MotivationDriver.HEALTH_SCARE:
            return "Your health recommendations focus on risk reduction and prevention, with emphasis on immediate and short-term benefits"
        elif motivation_enum == MotivationDriver.LONGEVITY:
            return "Your health recommendations emphasize long-term health optimization and adding healthy years to your life"
        elif motivation_enum == MotivationDriver.PERFORMANCE:
            return "Your health recommendations focus on enhancing your capabilities and performance, with clear milestones for progress"
        elif motivation_enum == MotivationDriver.APPEARANCE:
            return "Your health recommendations highlight visible results and aesthetic benefits, with specific timeframes for noticeable changes"
        elif motivation_enum == MotivationDriver.ENERGY:
            return "Your health recommendations prioritize daily energy and vitality, with immediate and practical benefits"
        elif motivation_enum == MotivationDriver.COGNITIVE:
            return "Your health recommendations emphasize brain health and cognitive function, with strategies for both immediate clarity and long-term protection"
        elif motivation_enum == MotivationDriver.MOOD:
            return "Your health recommendations focus on emotional wellbeing and psychological resilience, with practices to enhance daily mood states"
        elif motivation_enum == MotivationDriver.SOCIAL:
            return "Your health recommendations support social connection and relationship quality, enhancing your capacity for meaningful interactions"
        else:
            return "Your health recommendations have been personalized based on your profile"
    
    def _extract_key_findings(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key findings from the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of strings containing key findings
        """
        findings = []
        
        # Finding about motivation driver
        motivation = analysis["motivation_driver"]
        try:
            motivation_enum = MotivationDriver(motivation)
            motivation_name = motivation_enum.name.replace("_", " ").title()
            findings.append(f"Primary motivation driver: {motivation_name}")
        except ValueError:
            pass
        
        # Finding about personalization factors
        if analysis["personalization_factors"]:
            factor_types = set(factor["type"] for factor in analysis["personalization_factors"])
            findings.append(f"Personalization based on: {', '.join(factor_types)}")
        
        # Finding about recommendation feasibility
        feasibility_scores = [assessment["feasibility_score"] for assessment in analysis["feasibility_assessments"]]
        avg_feasibility = sum(feasibility_scores) / len(feasibility_scores) if feasibility_scores else 0.5
        
        if avg_feasibility > 0.7:
            findings.append("High implementation readiness for recommendations")
        elif avg_feasibility < 0.4:
            findings.append("Additional support needed for implementation")
        
        # Finding about prioritized recommendations
        if analysis["prioritized_recommendations"]:
            top_rec = analysis["prioritized_recommendations"][0]["recommendation"]
            findings.append(f"Top priority recommendation: {top_rec.get('action', '')}")
        
        return findings
    
    def _determine_confidence(self, analysis: Dict[str, Any]) -> ConfidenceLevel:
        """
        Determine the confidence level of the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            ConfidenceLevel enum representing the confidence level
        """
        # Start with medium confidence
        confidence = ConfidenceLevel.MEDIUM
        
        # Check if we have a clear motivation driver
        if analysis["motivation_driver"] == MotivationDriver.UNKNOWN.value:
            return ConfidenceLevel.LOW
        
        # Check if we have personalization factors
        if not analysis["personalization_factors"]:
            return ConfidenceLevel.LOW
        
        # Check if we have enough user profile data
        user_profile = analysis["user_profile"]
        profile_completeness = 0
        
        # Check for key profile elements
        if "preferences" in user_profile:
            profile_completeness += 1
        
        if "exercise_data" in user_profile:
            profile_completeness += 1
            
        if "sleep_data" in user_profile:
            profile_completeness += 1
            
        if "stress_data" in user_profile:
            profile_completeness += 1
            
        if "nutrition_data" in user_profile:
            profile_completeness += 1
        
        # Determine confidence based on profile completeness
        if profile_completeness >= 4:
            confidence = ConfidenceLevel.HIGH
        elif profile_completeness <= 1:
            confidence = ConfidenceLevel.LOW
        
        return confidence
