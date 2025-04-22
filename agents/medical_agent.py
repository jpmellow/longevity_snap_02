"""
Medical Agent for Longevity Snapshot App

This module implements the Medical Agent which provides overall health assessment
and medical recommendations based on user health data.
"""

from typing import Dict, List, Any, Optional
import logging
from .base_agent import BaseAgent, ConfidenceLevel

class MedicalAgent(BaseAgent):
    """
    Medical Agent for overall health assessment and medical recommendations.
    """
    
    def __init__(self):
        """Initialize the Medical Agent"""
        super().__init__("Medical")
    
    def _extract_relevant_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data relevant to medical analysis from the user data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing relevant data for medical analysis
        """
        relevant_data = {}
        
        # Extract basic demographics
        for key in ["age", "gender", "height", "weight"]:
            if key in user_data:
                relevant_data[key] = user_data[key]
        
        # Extract relevant health metrics
        if "health_metrics" in user_data:
            relevant_data["health_metrics"] = user_data["health_metrics"]
        
        # Extract summary data from other domains for holistic analysis
        for domain in ["sleep_data", "nutrition_data", "stress_data", "exercise_data"]:
            if domain in user_data:
                # Only extract high-level summary data, not detailed data
                domain_data = user_data[domain]
                if isinstance(domain_data, dict):
                    summary = {}
                    # Extract only top-level metrics for each domain
                    for key, value in domain_data.items():
                        if not isinstance(value, (dict, list)):
                            summary[key] = value
                    relevant_data[domain] = summary
        
        # Extract medical history if available
        if "medical_history" in user_data:
            relevant_data["medical_history"] = user_data["medical_history"]
        
        return relevant_data
    
    def _analyze_data(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the relevant medical data
        
        Args:
            relevant_data: Dictionary containing relevant data for medical analysis
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "bmi": None,
            "health_risks": [],
            "health_strengths": [],
            "areas_of_concern": [],
            "data_completeness": "partial"  # default assumption
        }
        
        # Calculate BMI if height and weight are available
        if "height" in relevant_data and "weight" in relevant_data:
            # Height in meters, weight in kg
            height_m = relevant_data["height"] / 100  # convert cm to m
            weight_kg = relevant_data["weight"]
            bmi = weight_kg / (height_m * height_m)
            analysis["bmi"] = round(bmi, 1)
            
            # Assess BMI category
            if bmi < 18.5:
                analysis["health_risks"].append("underweight")
            elif bmi >= 25:
                analysis["health_risks"].append("overweight")
                if bmi >= 30:
                    analysis["health_risks"].append("obesity")
            else:
                analysis["health_strengths"].append("healthy_weight")
        
        # Assess sleep health
        if "sleep_data" in relevant_data:
            sleep_data = relevant_data["sleep_data"]
            if "average_duration" in sleep_data:
                avg_duration = sleep_data["average_duration"]
                if avg_duration < 7:
                    analysis["health_risks"].append("insufficient_sleep")
                    analysis["areas_of_concern"].append("sleep_duration")
                elif avg_duration > 9:
                    analysis["areas_of_concern"].append("excessive_sleep")
                else:
                    analysis["health_strengths"].append("adequate_sleep_duration")
        
        # Assess stress levels
        if "stress_data" in relevant_data:
            stress_data = relevant_data["stress_data"]
            if "level" in stress_data:
                stress_level = stress_data["level"]
                if stress_level >= 7:
                    analysis["health_risks"].append("high_stress")
                    analysis["areas_of_concern"].append("stress_management")
                elif stress_level <= 3:
                    analysis["health_strengths"].append("low_stress")
        
        # Assess exercise habits
        if "exercise_data" in relevant_data:
            exercise_data = relevant_data["exercise_data"]
            weekly_exercise = 0
            
            if "strength_training" in exercise_data:
                weekly_exercise += exercise_data["strength_training"]
            
            if "cardio" in exercise_data:
                weekly_exercise += exercise_data["cardio"]
            
            if weekly_exercise < 3:
                analysis["health_risks"].append("insufficient_physical_activity")
                analysis["areas_of_concern"].append("exercise_frequency")
            elif weekly_exercise >= 5:
                analysis["health_strengths"].append("regular_exercise")
        
        # Assess data completeness
        required_fields = ["age", "gender", "height", "weight", "health_metrics"]
        optional_fields = ["sleep_data", "nutrition_data", "stress_data", "exercise_data", "medical_history"]
        
        required_count = sum(1 for field in required_fields if field in relevant_data)
        optional_count = sum(1 for field in optional_fields if field in relevant_data)
        
        if required_count == len(required_fields) and optional_count >= len(optional_fields) - 1:
            analysis["data_completeness"] = "complete"
        elif required_count >= len(required_fields) - 1 and optional_count >= 2:
            analysis["data_completeness"] = "substantial"
        elif required_count < len(required_fields) - 2 or optional_count < 2:
            analysis["data_completeness"] = "minimal"
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate medical recommendations based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # Regular check-up recommendation (almost always included)
        recommendations.append({
            "type": "medical",
            "action": "regular_checkup",
            "description": "Schedule a regular health check-up with your primary care physician",
            "priority": "medium"
        })
        
        # BMI-related recommendations
        if "bmi" in analysis and analysis["bmi"] is not None:
            bmi = analysis["bmi"]
            if bmi < 18.5:
                recommendations.append({
                    "type": "medical",
                    "action": "weight_gain",
                    "description": "Consult with a healthcare provider about healthy weight gain strategies",
                    "priority": "medium"
                })
            elif bmi >= 30:
                recommendations.append({
                    "type": "medical",
                    "action": "weight_management",
                    "description": "Consult with a healthcare provider about weight management strategies",
                    "priority": "high"
                })
            elif bmi >= 25:
                recommendations.append({
                    "type": "medical",
                    "action": "weight_management",
                    "description": "Consider implementing a moderate weight management plan",
                    "priority": "medium"
                })
        
        # Sleep-related recommendations
        if "insufficient_sleep" in analysis["health_risks"]:
            recommendations.append({
                "type": "medical",
                "action": "improve_sleep",
                "description": "Aim for 7-9 hours of quality sleep per night for optimal health",
                "priority": "high"
            })
        
        # Stress-related recommendations
        if "high_stress" in analysis["health_risks"]:
            recommendations.append({
                "type": "medical",
                "action": "stress_management",
                "description": "Consider stress management techniques such as meditation or professional counseling",
                "priority": "high"
            })
        
        # Exercise-related recommendations
        if "insufficient_physical_activity" in analysis["health_risks"]:
            recommendations.append({
                "type": "medical",
                "action": "increase_physical_activity",
                "description": "Aim for at least 150 minutes of moderate-intensity exercise per week",
                "priority": "high"
            })
        
        # Data completeness recommendations
        if analysis["data_completeness"] == "minimal":
            recommendations.append({
                "type": "medical",
                "action": "complete_health_profile",
                "description": "Complete your health profile with additional metrics for more accurate assessment",
                "priority": "high"
            })
        
        return recommendations
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate medical insights based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing insights
        """
        insights = []
        
        # Overall health status insight
        health_status = "optimal"
        if len(analysis["health_risks"]) > 2:
            health_status = "concerning"
        elif len(analysis["health_risks"]) > 0:
            health_status = "suboptimal"
        
        insights.append({
            "type": "health_status",
            "description": f"Overall health indicators suggest {health_status} health status",
            "confidence": "medium" if analysis["data_completeness"] == "partial" else "high"
        })
        
        # BMI insight
        if "bmi" in analysis and analysis["bmi"] is not None:
            bmi = analysis["bmi"]
            bmi_category = "healthy weight"
            if bmi < 18.5:
                bmi_category = "underweight"
            elif bmi >= 30:
                bmi_category = "obese"
            elif bmi >= 25:
                bmi_category = "overweight"
            
            insights.append({
                "type": "bmi",
                "description": f"BMI of {bmi} indicates {bmi_category}",
                "confidence": "high"
            })
        
        # Health strengths insight
        if analysis["health_strengths"]:
            strengths_list = ", ".join(analysis["health_strengths"])
            insights.append({
                "type": "health_strengths",
                "description": f"Notable health strengths: {strengths_list}",
                "confidence": "medium"
            })
        
        # Areas of concern insight
        if analysis["areas_of_concern"]:
            concerns_list = ", ".join(analysis["areas_of_concern"])
            insights.append({
                "type": "areas_of_concern",
                "description": f"Areas that may need attention: {concerns_list}",
                "confidence": "medium"
            })
        
        return insights
    
    def _extract_key_findings(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key medical findings from the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of strings containing key findings
        """
        key_findings = []
        
        # BMI finding
        if "bmi" in analysis and analysis["bmi"] is not None:
            key_findings.append(f"BMI: {analysis['bmi']}")
        
        # Health risks
        for risk in analysis["health_risks"]:
            key_findings.append(f"Health risk: {risk}")
        
        # Health strengths
        for strength in analysis["health_strengths"]:
            key_findings.append(f"Health strength: {strength}")
        
        # Data completeness
        key_findings.append(f"Data completeness: {analysis['data_completeness']}")
        
        return key_findings
    
    def _determine_confidence(self, analysis: Dict[str, Any]) -> ConfidenceLevel:
        """
        Determine the confidence level of the medical analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            ConfidenceLevel enum representing the confidence level
        """
        # Base confidence on data completeness
        if analysis["data_completeness"] == "complete":
            return ConfidenceLevel.HIGH
        elif analysis["data_completeness"] == "substantial":
            return ConfidenceLevel.MEDIUM
        elif analysis["data_completeness"] == "partial":
            return ConfidenceLevel.MEDIUM
        else:  # minimal
            return ConfidenceLevel.LOW
