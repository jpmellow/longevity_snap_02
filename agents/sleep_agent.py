"""
Sleep Agent for Longevity Snapshot App

This module implements the Sleep Agent which analyzes sleep patterns
and provides sleep-related recommendations based on user sleep data.
"""

from typing import Dict, List, Any, Optional
import logging
from .base_agent import BaseAgent, ConfidenceLevel

class SleepAgent(BaseAgent):
    """
    Sleep Agent for sleep pattern analysis and recommendations.
    """
    
    def __init__(self):
        """Initialize the Sleep Agent"""
        super().__init__("Sleep")
    
    def _extract_relevant_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data relevant to sleep analysis from the user data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing relevant data for sleep analysis
        """
        relevant_data = {}
        
        # Extract sleep data
        if "sleep_data" in user_data:
            relevant_data["sleep_data"] = user_data["sleep_data"]
        
        # Extract basic demographics that might affect sleep recommendations
        for key in ["age", "gender"]:
            if key in user_data:
                relevant_data[key] = user_data[key]
        
        # Extract stress data that might affect sleep
        if "stress_data" in user_data:
            relevant_data["stress_data"] = user_data["stress_data"]
        
        # Extract exercise data that might affect sleep
        if "exercise_data" in user_data:
            relevant_data["exercise_data"] = user_data["exercise_data"]
        
        # Extract user preferences related to sleep
        if "preferences" in user_data and isinstance(user_data["preferences"], dict):
            sleep_preferences = {}
            preferences = user_data["preferences"]
            
            if "sleep_time" in preferences:
                sleep_preferences["sleep_time"] = preferences["sleep_time"]
            
            if "wake_time" in preferences:
                sleep_preferences["wake_time"] = preferences["wake_time"]
            
            if "sleep_environment" in preferences:
                sleep_preferences["sleep_environment"] = preferences["sleep_environment"]
            
            if sleep_preferences:
                relevant_data["sleep_preferences"] = sleep_preferences
        
        return relevant_data
    
    def _analyze_data(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the relevant sleep data
        
        Args:
            relevant_data: Dictionary containing relevant data for sleep analysis
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "sleep_quality": None,
            "sleep_duration": None,
            "sleep_consistency": None,
            "sleep_issues": [],
            "sleep_strengths": [],
            "data_completeness": "partial"  # default assumption
        }
        
        # Check if sleep data exists
        if "sleep_data" not in relevant_data:
            analysis["data_completeness"] = "minimal"
            return analysis
        
        sleep_data = relevant_data["sleep_data"]
        
        # Analyze sleep duration
        if "average_duration" in sleep_data:
            duration = sleep_data["average_duration"]
            analysis["sleep_duration"] = duration
            
            # Assess sleep duration
            if duration < 6:
                analysis["sleep_issues"].append("severe_sleep_deprivation")
            elif duration < 7:
                analysis["sleep_issues"].append("mild_sleep_deprivation")
            elif duration > 9:
                analysis["sleep_issues"].append("excessive_sleep")
            else:
                analysis["sleep_strengths"].append("optimal_sleep_duration")
        
        # Analyze sleep quality
        if "quality" in sleep_data:
            quality = sleep_data["quality"]
            analysis["sleep_quality"] = quality
            
            if quality in ["low", "poor"]:
                analysis["sleep_issues"].append("poor_sleep_quality")
            elif quality in ["high", "excellent"]:
                analysis["sleep_strengths"].append("high_sleep_quality")
        
        # Analyze sleep consistency
        if "bedtime_consistency" in sleep_data:
            consistency = sleep_data["bedtime_consistency"]
            analysis["sleep_consistency"] = consistency
            
            if consistency in ["low", "poor"]:
                analysis["sleep_issues"].append("irregular_sleep_schedule")
            elif consistency in ["high", "excellent"]:
                analysis["sleep_strengths"].append("consistent_sleep_schedule")
        
        # Check for specific sleep issues
        if "issues" in sleep_data and isinstance(sleep_data["issues"], list):
            for issue in sleep_data["issues"]:
                analysis["sleep_issues"].append(issue)
        
        # Analyze impact of stress on sleep
        if "stress_data" in relevant_data:
            stress_data = relevant_data["stress_data"]
            if "level" in stress_data and stress_data["level"] >= 7:
                analysis["sleep_issues"].append("stress_related_sleep_issues")
        
        # Analyze impact of exercise on sleep
        if "exercise_data" in relevant_data:
            exercise_data = relevant_data["exercise_data"]
            weekly_exercise = 0
            
            if "strength_training" in exercise_data:
                weekly_exercise += exercise_data["strength_training"]
            
            if "cardio" in exercise_data:
                weekly_exercise += exercise_data["cardio"]
            
            if weekly_exercise >= 3:
                analysis["sleep_strengths"].append("exercise_supported_sleep")
            else:
                analysis["sleep_issues"].append("insufficient_exercise_for_sleep")
        
        # Assess data completeness
        required_sleep_fields = ["average_duration", "quality", "bedtime_consistency"]
        optional_fields = ["issues", "sleep_preferences", "stress_data", "exercise_data"]
        
        required_count = sum(1 for field in required_sleep_fields if field in sleep_data)
        optional_count = sum(1 for field in optional_fields if field in relevant_data)
        
        if required_count == len(required_sleep_fields) and optional_count >= 2:
            analysis["data_completeness"] = "complete"
        elif required_count >= 2 and optional_count >= 1:
            analysis["data_completeness"] = "substantial"
        elif required_count < 2:
            analysis["data_completeness"] = "minimal"
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate sleep recommendations based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # If data is minimal, recommend collecting more sleep data
        if analysis["data_completeness"] == "minimal":
            recommendations.append({
                "type": "sleep",
                "action": "track_sleep",
                "description": "Start tracking your sleep duration, quality, and consistency for better insights",
                "priority": "high"
            })
            return recommendations
        
        # Sleep duration recommendations
        if "sleep_duration" in analysis and analysis["sleep_duration"] is not None:
            duration = analysis["sleep_duration"]
            if duration < 6:
                recommendations.append({
                    "type": "sleep",
                    "action": "increase_sleep_duration",
                    "description": "Significantly increase sleep duration to at least 7 hours per night",
                    "priority": "high"
                })
            elif duration < 7:
                recommendations.append({
                    "type": "sleep",
                    "action": "increase_sleep_duration",
                    "description": "Slightly increase sleep duration to reach 7-8 hours per night",
                    "priority": "medium"
                })
            elif duration > 9:
                recommendations.append({
                    "type": "sleep",
                    "action": "optimize_sleep_duration",
                    "description": "Consider reducing sleep duration to 7-9 hours for optimal rest",
                    "priority": "low"
                })
        
        # Sleep consistency recommendations
        if "irregular_sleep_schedule" in analysis["sleep_issues"]:
            recommendations.append({
                "type": "sleep",
                "action": "consistent_schedule",
                "description": "Maintain a consistent sleep and wake time, even on weekends",
                "priority": "high"
            })
        
        # Sleep quality recommendations
        if "poor_sleep_quality" in analysis["sleep_issues"]:
            recommendations.append({
                "type": "sleep",
                "action": "improve_sleep_environment",
                "description": "Optimize your bedroom for sleep: dark, quiet, cool, and comfortable",
                "priority": "high"
            })
            
            recommendations.append({
                "type": "sleep",
                "action": "bedtime_routine",
                "description": "Establish a relaxing pre-sleep routine to signal your body it's time to rest",
                "priority": "medium"
            })
        
        # Stress-related sleep recommendations
        if "stress_related_sleep_issues" in analysis["sleep_issues"]:
            recommendations.append({
                "type": "sleep",
                "action": "stress_management_for_sleep",
                "description": "Practice relaxation techniques before bed such as deep breathing or meditation",
                "priority": "high"
            })
        
        # Exercise-related sleep recommendations
        if "insufficient_exercise_for_sleep" in analysis["sleep_issues"]:
            recommendations.append({
                "type": "sleep",
                "action": "exercise_for_sleep",
                "description": "Incorporate regular physical activity, but avoid vigorous exercise close to bedtime",
                "priority": "medium"
            })
        
        # General sleep hygiene recommendations (almost always included)
        recommendations.append({
            "type": "sleep",
            "action": "limit_screen_time",
            "description": "Avoid screens (phones, tablets, computers) at least 1 hour before bedtime",
            "priority": "medium"
        })
        
        recommendations.append({
            "type": "sleep",
            "action": "limit_stimulants",
            "description": "Avoid caffeine and alcohol close to bedtime",
            "priority": "medium"
        })
        
        return recommendations
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate sleep insights based on the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing insights
        """
        insights = []
        
        # Overall sleep quality insight
        sleep_status = "optimal"
        if len(analysis["sleep_issues"]) > 2:
            sleep_status = "poor"
        elif len(analysis["sleep_issues"]) > 0:
            sleep_status = "suboptimal"
        
        insights.append({
            "type": "sleep_pattern",
            "description": f"Overall sleep pattern is {sleep_status}",
            "confidence": "medium" if analysis["data_completeness"] == "partial" else "high"
        })
        
        # Sleep duration insight
        if "sleep_duration" in analysis and analysis["sleep_duration"] is not None:
            duration = analysis["sleep_duration"]
            duration_category = "optimal"
            if duration < 6:
                duration_category = "severely insufficient"
            elif duration < 7:
                duration_category = "slightly insufficient"
            elif duration > 9:
                duration_category = "excessive"
            
            insights.append({
                "type": "sleep_duration",
                "description": f"Average sleep duration of {duration} hours is {duration_category}",
                "confidence": "high"
            })
        
        # Sleep consistency insight
        if "sleep_consistency" in analysis and analysis["sleep_consistency"] is not None:
            consistency = analysis["sleep_consistency"]
            insights.append({
                "type": "sleep_consistency",
                "description": f"Sleep schedule consistency is {consistency}",
                "confidence": "high"
            })
        
        # Sleep issues insight
        if analysis["sleep_issues"]:
            issues_list = ", ".join(analysis["sleep_issues"])
            insights.append({
                "type": "sleep_issues",
                "description": f"Identified sleep issues: {issues_list}",
                "confidence": "medium"
            })
        
        # Sleep strengths insight
        if analysis["sleep_strengths"]:
            strengths_list = ", ".join(analysis["sleep_strengths"])
            insights.append({
                "type": "sleep_strengths",
                "description": f"Positive sleep aspects: {strengths_list}",
                "confidence": "medium"
            })
        
        return insights
    
    def _extract_key_findings(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key sleep findings from the analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of strings containing key findings
        """
        key_findings = []
        
        # Sleep duration finding
        if "sleep_duration" in analysis and analysis["sleep_duration"] is not None:
            key_findings.append(f"Average sleep duration: {analysis['sleep_duration']} hours")
        
        # Sleep quality finding
        if "sleep_quality" in analysis and analysis["sleep_quality"] is not None:
            key_findings.append(f"Sleep quality: {analysis['sleep_quality']}")
        
        # Sleep consistency finding
        if "sleep_consistency" in analysis and analysis["sleep_consistency"] is not None:
            key_findings.append(f"Sleep schedule consistency: {analysis['sleep_consistency']}")
        
        # Sleep issues
        for issue in analysis["sleep_issues"]:
            key_findings.append(f"Sleep issue: {issue}")
        
        # Sleep strengths
        for strength in analysis["sleep_strengths"]:
            key_findings.append(f"Sleep strength: {strength}")
        
        # Data completeness
        key_findings.append(f"Data completeness: {analysis['data_completeness']}")
        
        return key_findings
    
    def _determine_confidence(self, analysis: Dict[str, Any]) -> ConfidenceLevel:
        """
        Determine the confidence level of the sleep analysis
        
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
