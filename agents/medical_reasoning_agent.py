"""
Medical Reasoning Agent for Longevity Snapshot App

This module implements a specialized Medical Reasoning Agent focused on longevity,
internal medicine, sleep, and obesity. It provides detailed clinical reasoning,
evidence-based assessments, and structured output.
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
import json
from enum import Enum
from .base_agent import BaseAgent, ConfidenceLevel

class EvidenceCategory(Enum):
    """Enum representing categories of medical evidence"""
    CLINICAL_GUIDELINES = "clinical_guidelines"
    SYSTEMATIC_REVIEW = "systematic_review"
    META_ANALYSIS = "meta_analysis"
    RANDOMIZED_TRIAL = "randomized_trial"
    OBSERVATIONAL_STUDY = "observational_study"
    EXPERT_OPINION = "expert_opinion"
    MECHANISTIC_REASONING = "mechanistic_reasoning"

class BiasRiskLevel(Enum):
    """Enum representing levels of algorithm bias risk"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

class MedicalReasoningAgent(BaseAgent):
    """
    Medical Reasoning Agent specializing in longevity, internal medicine, sleep, and obesity.
    Provides detailed clinical reasoning with evidence-based assessments.
    """
    
    def __init__(self):
        """Initialize the Medical Reasoning Agent"""
        super().__init__("MedicalReasoning")
        
        # Clinical guidelines and reference ranges
        self.guidelines = {
            "bmi": {
                "underweight": {"range": (0, 18.5), "risk": "moderate", "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "normal": {"range": (18.5, 25), "risk": "low", "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "overweight": {"range": (25, 30), "risk": "moderate", "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "obese_class_1": {"range": (30, 35), "risk": "high", "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "obese_class_2": {"range": (35, 40), "risk": "very_high", "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "obese_class_3": {"range": (40, float('inf')), "risk": "extremely_high", "evidence": EvidenceCategory.CLINICAL_GUIDELINES}
            },
            "sleep_duration": {
                "adult": {
                    "recommended": {"range": (7, 9), "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                    "may_be_appropriate": [{"range": (6, 7), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}, 
                                          {"range": (9, 10), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}],
                    "not_recommended": [{"range": (0, 6), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}, 
                                       {"range": (10, float('inf')), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}]
                },
                "older_adult": {  # 65+ years
                    "recommended": {"range": (7, 8), "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                    "may_be_appropriate": [{"range": (5, 7), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}, 
                                          {"range": (8, 9), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}],
                    "not_recommended": [{"range": (0, 5), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}, 
                                       {"range": (9, float('inf')), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}]
                }
            },
            "blood_pressure": {
                "normal": {"systolic": {"range": (0, 120)}, "diastolic": {"range": (0, 80)}, 
                          "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "elevated": {"systolic": {"range": (120, 130)}, "diastolic": {"range": (0, 80)}, 
                            "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "hypertension_stage_1": {"systolic": {"range": (130, 140)}, "diastolic": {"range": (80, 90)}, 
                                        "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "hypertension_stage_2": {"systolic": {"range": (140, float('inf'))}, "diastolic": {"range": (90, float('inf'))}, 
                                        "evidence": EvidenceCategory.CLINICAL_GUIDELINES}
            },
            "heart_rate_resting": {
                "bradycardia": {"range": (0, 60), "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "normal": {"range": (60, 100), "evidence": EvidenceCategory.CLINICAL_GUIDELINES},
                "tachycardia": {"range": (100, float('inf')), "evidence": EvidenceCategory.CLINICAL_GUIDELINES}
            },
            "vo2_max": {
                "poor": {"male": {"range": (0, 35)}, "female": {"range": (0, 28)}},
                "fair": {"male": {"range": (35, 42)}, "female": {"range": (28, 34)}},
                "good": {"male": {"range": (42, 46)}, "female": {"range": (34, 40)}},
                "excellent": {"male": {"range": (46, 56)}, "female": {"range": (40, 50)}},
                "superior": {"male": {"range": (56, float('inf'))}, "female": {"range": (50, float('inf'))}}
            },
            "stress_level": {
                "low": {"range": (0, 4), "evidence": EvidenceCategory.EXPERT_OPINION},
                "moderate": {"range": (4, 7), "evidence": EvidenceCategory.EXPERT_OPINION},
                "high": {"range": (7, float('inf')), "evidence": EvidenceCategory.EXPERT_OPINION}
            },
            "physical_activity": {
                "recommended_weekly_minutes": {
                    "moderate_intensity": 150,
                    "vigorous_intensity": 75,
                    "evidence": EvidenceCategory.CLINICAL_GUIDELINES
                },
                "recommended_days": {
                    "minimum": 3,
                    "optimal": 5,
                    "evidence": EvidenceCategory.CLINICAL_GUIDELINES
                }
            }
        }
    
    def _extract_relevant_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data relevant to medical reasoning analysis from the user data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing relevant data for medical reasoning analysis
        """
        relevant_data = {}
        
        # Extract basic demographics
        for key in ["age", "gender", "height", "weight"]:
            if key in user_data:
                relevant_data[key] = user_data[key]
        
        # Extract all health metrics
        if "health_metrics" in user_data:
            relevant_data["health_metrics"] = user_data["health_metrics"]
        
        # Extract all domain data for comprehensive analysis
        for domain in ["sleep_data", "nutrition_data", "stress_data", "exercise_data"]:
            if domain in user_data:
                relevant_data[domain] = user_data[domain]
        
        # Extract VO2 max proxy if available
        if "vo2_max_proxy" in user_data:
            relevant_data["vo2_max_proxy"] = user_data["vo2_max_proxy"]
        
        # Extract medical history if available
        if "medical_history" in user_data:
            relevant_data["medical_history"] = user_data["medical_history"]
        
        # Extract user preferences that might affect medical recommendations
        if "preferences" in user_data:
            relevant_data["preferences"] = user_data["preferences"]
        
        return relevant_data

    def _analyze_data(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the relevant medical data with detailed clinical reasoning
        
        Args:
            relevant_data: Dictionary containing relevant data for medical analysis
            
        Returns:
            Dictionary containing analysis results with clinical reasoning
        """
        analysis = {
            "metrics": {},
            "clinical_reasoning": [],
            "guidelines_assessment": [],
            "health_risks": [],
            "health_strengths": [],
            "areas_of_concern": [],
            "bias_risk_assessment": {},
            "app_usage_risks": [],
            "data_completeness": self._assess_data_completeness(relevant_data)
        }
        
        # Analyze BMI if height and weight are available
        if "height" in relevant_data and "weight" in relevant_data:
            bmi_analysis = self._analyze_bmi(relevant_data["height"], relevant_data["weight"])
            analysis["metrics"]["bmi"] = bmi_analysis["value"]
            analysis["clinical_reasoning"].append(bmi_analysis["reasoning"])
            analysis["guidelines_assessment"].append(bmi_analysis["guideline_assessment"])
            
            # Add BMI-related risks or strengths
            if bmi_analysis["category"] in ["underweight", "overweight", "obese_class_1", "obese_class_2", "obese_class_3"]:
                analysis["health_risks"].append({
                    "type": bmi_analysis["category"],
                    "description": bmi_analysis["description"],
                    "evidence": bmi_analysis["evidence"]
                })
                analysis["areas_of_concern"].append("weight_management")
            elif bmi_analysis["category"] == "normal":
                analysis["health_strengths"].append({
                    "type": "healthy_weight",
                    "description": "BMI within healthy range",
                    "evidence": bmi_analysis["evidence"]
                })
        
        # Analyze sleep health
        if "sleep_data" in relevant_data:
            sleep_analysis = self._analyze_sleep(relevant_data["sleep_data"], relevant_data.get("age", 35))
            analysis["metrics"]["sleep"] = sleep_analysis["metrics"]
            analysis["clinical_reasoning"].append(sleep_analysis["reasoning"])
            analysis["guidelines_assessment"].append(sleep_analysis["guideline_assessment"])
            
            # Add sleep-related risks or strengths
            for risk in sleep_analysis.get("risks", []):
                analysis["health_risks"].append(risk)
                if "sleep" not in analysis["areas_of_concern"]:
                    analysis["areas_of_concern"].append("sleep")
            
            for strength in sleep_analysis.get("strengths", []):
                analysis["health_strengths"].append(strength)
        
        # Analyze stress levels
        if "stress_data" in relevant_data:
            stress_analysis = self._analyze_stress(relevant_data["stress_data"])
            analysis["metrics"]["stress"] = stress_analysis["metrics"]
            analysis["clinical_reasoning"].append(stress_analysis["reasoning"])
            analysis["guidelines_assessment"].append(stress_analysis["guideline_assessment"])
            
            # Add stress-related risks or strengths
            for risk in stress_analysis.get("risks", []):
                analysis["health_risks"].append(risk)
                if "stress_management" not in analysis["areas_of_concern"]:
                    analysis["areas_of_concern"].append("stress_management")
            
            for strength in stress_analysis.get("strengths", []):
                analysis["health_strengths"].append(strength)
        
        # Analyze physical activity
        if "exercise_data" in relevant_data:
            activity_analysis = self._analyze_physical_activity(relevant_data["exercise_data"])
            analysis["metrics"]["physical_activity"] = activity_analysis["metrics"]
            analysis["clinical_reasoning"].append(activity_analysis["reasoning"])
            analysis["guidelines_assessment"].append(activity_analysis["guideline_assessment"])
            
            # Add activity-related risks or strengths
            for risk in activity_analysis.get("risks", []):
                analysis["health_risks"].append(risk)
                if "physical_activity" not in analysis["areas_of_concern"]:
                    analysis["areas_of_concern"].append("physical_activity")
            
            for strength in activity_analysis.get("strengths", []):
                analysis["health_strengths"].append(strength)
        
        # Analyze VO2 max proxy if available
        if "vo2_max_proxy" in relevant_data:
            vo2_analysis = self._analyze_vo2_max(
                relevant_data["vo2_max_proxy"], 
                relevant_data.get("gender", "unknown"),
                relevant_data.get("age", 35)
            )
            analysis["metrics"]["vo2_max"] = vo2_analysis["value"]
            analysis["clinical_reasoning"].append(vo2_analysis["reasoning"])
            analysis["guidelines_assessment"].append(vo2_analysis["guideline_assessment"])
            
            # Add VO2 max-related risks or strengths
            if vo2_analysis["category"] in ["poor", "fair"]:
                analysis["health_risks"].append({
                    "type": "low_cardiorespiratory_fitness",
                    "description": vo2_analysis["description"],
                    "evidence": vo2_analysis["evidence"]
                })
                if "cardiorespiratory_fitness" not in analysis["areas_of_concern"]:
                    analysis["areas_of_concern"].append("cardiorespiratory_fitness")
            elif vo2_analysis["category"] in ["good", "excellent", "superior"]:
                analysis["health_strengths"].append({
                    "type": "good_cardiorespiratory_fitness",
                    "description": vo2_analysis["description"],
                    "evidence": vo2_analysis["evidence"]
                })
        
        # Analyze health metrics if available
        if "health_metrics" in relevant_data:
            metrics_analysis = self._analyze_health_metrics(relevant_data["health_metrics"])
            analysis["metrics"].update(metrics_analysis["metrics"])
            analysis["clinical_reasoning"].append(metrics_analysis["reasoning"])
            analysis["guidelines_assessment"].extend(metrics_analysis["guideline_assessment"])
            
            # Add health metrics-related risks or strengths
            for risk in metrics_analysis.get("risks", []):
                analysis["health_risks"].append(risk)
                if risk["type"] not in analysis["areas_of_concern"]:
                    analysis["areas_of_concern"].append(risk["type"])
            
            for strength in metrics_analysis.get("strengths", []):
                analysis["health_strengths"].append(strength)
        
        # Assess algorithm bias risks
        analysis["bias_risk_assessment"] = self._assess_bias_risks(relevant_data)
        
        # Assess app usage risks
        analysis["app_usage_risks"] = self._assess_app_usage_risks(relevant_data)
        
        return analysis
    
    def _assess_data_completeness(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the completeness of the user data
        
        Args:
            relevant_data: Dictionary containing relevant data for medical analysis
            
        Returns:
            Dictionary with data completeness assessment
        """
        required_fields = ["age", "gender", "height", "weight"]
        important_fields = ["health_metrics", "sleep_data", "exercise_data", "stress_data"]
        optional_fields = ["nutrition_data", "vo2_max_proxy", "medical_history", "preferences"]
        
        # Count available fields
        required_count = sum(1 for field in required_fields if field in relevant_data)
        important_count = sum(1 for field in important_fields if field in relevant_data)
        optional_count = sum(1 for field in optional_fields if field in relevant_data)
        
        # Calculate completeness percentages
        required_pct = (required_count / len(required_fields)) * 100
        important_pct = (important_count / len(important_fields)) * 100
        overall_pct = ((required_count + important_count) / 
                      (len(required_fields) + len(important_fields))) * 100
        
        # Determine completeness level
        if required_pct == 100 and important_pct >= 75:
            level = "complete"
            confidence = ConfidenceLevel.HIGH
        elif required_pct >= 75 and important_pct >= 50:
            level = "substantial"
            confidence = ConfidenceLevel.MEDIUM
        elif required_pct >= 50:
            level = "partial"
            confidence = ConfidenceLevel.MEDIUM
        else:
            level = "minimal"
            confidence = ConfidenceLevel.LOW
        
        # List missing fields
        missing_required = [field for field in required_fields if field not in relevant_data]
        missing_important = [field for field in important_fields if field not in relevant_data]
        
        return {
            "level": level,
            "confidence": confidence.value,
            "overall_percentage": round(overall_pct),
            "missing_required_fields": missing_required,
            "missing_important_fields": missing_important,
            "reasoning": f"Data completeness assessment: {level} ({round(overall_pct)}%). " +
                        (f"Missing required fields: {', '.join(missing_required)}. " if missing_required else "") +
                        (f"Missing important fields: {', '.join(missing_important)}. " if missing_important else "")
        }
    
    def _analyze_bmi(self, height_cm: float, weight_kg: float) -> Dict[str, Any]:
        """
        Analyze BMI with clinical reasoning
        
        Args:
            height_cm: Height in centimeters
            weight_kg: Weight in kilograms
            
        Returns:
            Dictionary with BMI analysis and reasoning
        """
        # Calculate BMI
        height_m = height_cm / 100  # convert cm to m
        bmi = weight_kg / (height_m * height_m)
        bmi_rounded = round(bmi, 1)
        
        # Determine BMI category
        category = None
        for cat, details in self.guidelines["bmi"].items():
            lower, upper = details["range"]
            if lower <= bmi < upper:
                category = cat
                break
        
        # Get evidence category
        evidence = self.guidelines["bmi"][category]["evidence"].value
        
        # Generate description based on category
        descriptions = {
            "underweight": f"BMI of {bmi_rounded} indicates underweight status, which may be associated with nutritional deficiencies and reduced immune function.",
            "normal": f"BMI of {bmi_rounded} is within the healthy weight range, associated with lower risk of weight-related health issues.",
            "overweight": f"BMI of {bmi_rounded} indicates overweight status, which may increase risk for conditions like type 2 diabetes and cardiovascular disease.",
            "obese_class_1": f"BMI of {bmi_rounded} indicates class 1 obesity, associated with increased risk of cardiovascular disease, type 2 diabetes, and all-cause mortality.",
            "obese_class_2": f"BMI of {bmi_rounded} indicates class 2 obesity, associated with high risk of metabolic syndrome, sleep apnea, and joint problems.",
            "obese_class_3": f"BMI of {bmi_rounded} indicates class 3 obesity (severe), associated with very high risk of multiple comorbidities and reduced life expectancy."
        }
        
        description = descriptions.get(category, f"BMI of {bmi_rounded}")
        
        # Generate clinical reasoning
        reasoning = (
            f"User reports height of {height_cm} cm and weight of {weight_kg} kg. "
            f"BMI calculation: {weight_kg} ÷ ({height_m} × {height_m}) = {bmi_rounded}. "
            f"According to clinical guidelines, this BMI falls in the '{category}' category. "
            f"{description} "
            f"Confidence is high for BMI calculation, though BMI has limitations as it doesn't account for muscle mass, body composition, or fat distribution."
        )
        
        # Generate guideline assessment
        guideline_assessment = {
            "metric": "BMI",
            "value": bmi_rounded,
            "category": category,
            "reference_range": f"{self.guidelines['bmi'][category]['range'][0]}-{self.guidelines['bmi'][category]['range'][1]}",
            "guideline_source": "WHO/CDC BMI Classification",
            "evidence_category": evidence
        }
        
        return {
            "value": bmi_rounded,
            "category": category,
            "description": description,
            "reasoning": reasoning,
            "guideline_assessment": guideline_assessment,
            "evidence": evidence
        }
    
    def _analyze_sleep(self, sleep_data: Dict[str, Any], age: int) -> Dict[str, Any]:
        """
        Analyze sleep data with clinical reasoning
        
        Args:
            sleep_data: Dictionary containing sleep data
            age: User age in years
            
        Returns:
            Dictionary with sleep analysis and reasoning
        """
        metrics = {}
        risks = []
        strengths = []
        guideline_assessments = []
        
        # Determine age category for sleep guidelines
        age_category = "older_adult" if age >= 65 else "adult"
        
        # Analyze sleep duration if available
        if "average_duration" in sleep_data:
            duration = sleep_data["average_duration"]
            metrics["average_duration"] = duration
            
            # Determine if duration falls within recommended range
            recommended = self.guidelines["sleep_duration"][age_category]["recommended"]["range"]
            may_be_appropriate = self.guidelines["sleep_duration"][age_category]["may_be_appropriate"]
            not_recommended = self.guidelines["sleep_duration"][age_category]["not_recommended"]
            
            # Check if duration is in recommended range
            if recommended[0] <= duration < recommended[1]:
                category = "optimal"
                description = f"Sleep duration of {duration} hours is within the optimal range for {age_category}s."
                strengths.append({
                    "type": "optimal_sleep_duration",
                    "description": description,
                    "evidence": self.guidelines["sleep_duration"][age_category]["recommended"]["evidence"].value
                })
            else:
                # Check if duration is in "may be appropriate" ranges
                in_may_be_appropriate = False
                for range_dict in may_be_appropriate:
                    if range_dict["range"][0] <= duration < range_dict["range"][1]:
                        category = "acceptable"
                        description = f"Sleep duration of {duration} hours is acceptable but not optimal for {age_category}s."
                        in_may_be_appropriate = True
                        break
                
                # If not in "may be appropriate" ranges, it's in "not recommended" ranges
                if not in_may_be_appropriate:
                    category = "suboptimal"
                    if duration < recommended[0]:
                        description = f"Sleep duration of {duration} hours is below the recommended minimum for {age_category}s."
                        risks.append({
                            "type": "insufficient_sleep",
                            "description": "Insufficient sleep duration increases risk of cognitive impairment, mood disorders, cardiovascular disease, and metabolic dysfunction.",
                            "evidence": self.guidelines["sleep_duration"][age_category]["recommended"]["evidence"].value
                        })
                    else:  # duration >= recommended[1]
                        description = f"Sleep duration of {duration} hours exceeds the recommended maximum for {age_category}s."
                        risks.append({
                            "type": "excessive_sleep",
                            "description": "Excessive sleep duration may be associated with increased mortality risk and could indicate underlying health conditions.",
                            "evidence": self.guidelines["sleep_duration"][age_category]["recommended"]["evidence"].value
                        })
            
            # Add guideline assessment
            guideline_assessments.append({
                "metric": "Sleep Duration",
                "value": duration,
                "category": category,
                "reference_range": f"{recommended[0]}-{recommended[1]} hours",
                "guideline_source": "National Sleep Foundation",
                "evidence_category": self.guidelines["sleep_duration"][age_category]["recommended"]["evidence"].value
            })
        
        # Analyze sleep quality if available
        if "quality" in sleep_data:
            quality = sleep_data["quality"]
            metrics["quality"] = quality
            
            if quality in ["low", "poor"]:
                risks.append({
                    "type": "poor_sleep_quality",
                    "description": "Poor sleep quality is associated with daytime fatigue, cognitive impairment, and increased stress reactivity.",
                    "evidence": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
            elif quality in ["high", "excellent"]:
                strengths.append({
                    "type": "good_sleep_quality",
                    "description": "Good sleep quality supports cognitive function, emotional regulation, and physical recovery.",
                    "evidence": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Analyze sleep consistency if available
        if "bedtime_consistency" in sleep_data:
            consistency = sleep_data["bedtime_consistency"]
            metrics["bedtime_consistency"] = consistency
            
            if consistency in ["low", "poor"]:
                risks.append({
                    "type": "irregular_sleep_schedule",
                    "description": "Irregular sleep schedule disrupts circadian rhythms and is associated with metabolic dysfunction and mood disorders.",
                    "evidence": EvidenceCategory.OBSERVATIONAL_STUDY.value
                })
            elif consistency in ["high", "excellent"]:
                strengths.append({
                    "type": "consistent_sleep_schedule",
                    "description": "Consistent sleep schedule supports healthy circadian rhythms and optimal hormone regulation.",
                    "evidence": EvidenceCategory.OBSERVATIONAL_STUDY.value
                })
        
        # Generate clinical reasoning
        reasoning_parts = []
        
        if "average_duration" in sleep_data:
            reasoning_parts.append(
                f"User reports average sleep duration of {sleep_data['average_duration']} hours. "
                f"Guideline for {age_category}s is {recommended[0]}-{recommended[1]} hours. "
            )
            
            if category == "optimal":
                reasoning_parts.append("Sleep duration is optimal. ")
            elif category == "acceptable":
                reasoning_parts.append("Sleep duration is acceptable but not optimal. ")
            else:
                if duration < recommended[0]:
                    reasoning_parts.append(
                        f"Sleep duration is below recommended minimum, which increases risk of cognitive impairment, "
                        f"mood disorders, and metabolic dysfunction. "
                    )
                else:
                    reasoning_parts.append(
                        f"Sleep duration exceeds recommended maximum, which may be associated with increased mortality "
                        f"risk and could indicate underlying health conditions. "
                    )
        
        if "quality" in sleep_data:
            reasoning_parts.append(
                f"User reports {sleep_data['quality']} sleep quality. "
                f"{'Poor sleep quality is associated with daytime fatigue and cognitive impairment. ' if sleep_data['quality'] in ['low', 'poor'] else ''}"
                f"{'Good sleep quality supports cognitive function and physical recovery. ' if sleep_data['quality'] in ['high', 'excellent'] else ''}"
            )
        
        if "bedtime_consistency" in sleep_data:
            reasoning_parts.append(
                f"User reports {sleep_data['bedtime_consistency']} bedtime consistency. "
                f"{'Irregular sleep schedule disrupts circadian rhythms. ' if sleep_data['bedtime_consistency'] in ['low', 'poor'] else ''}"
                f"{'Consistent sleep schedule supports healthy circadian rhythms. ' if sleep_data['bedtime_consistency'] in ['high', 'excellent'] else ''}"
            )
        
        # Add confidence assessment
        sleep_data_points = len([key for key in ["average_duration", "quality", "bedtime_consistency", "issues"] if key in sleep_data])
        if sleep_data_points >= 3:
            reasoning_parts.append("Confidence is high based on comprehensive sleep data.")
        elif sleep_data_points >= 2:
            reasoning_parts.append("Confidence is medium due to partial sleep data.")
        else:
            reasoning_parts.append("Confidence is low due to limited sleep data.")
        
        reasoning = "".join(reasoning_parts)
        
        return {
            "metrics": metrics,
            "risks": risks,
            "strengths": strengths,
            "reasoning": reasoning,
            "guideline_assessment": guideline_assessments
        }

    def _analyze_stress(self, stress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze stress data with clinical reasoning
        
        Args:
            stress_data: Dictionary containing stress data
            
        Returns:
            Dictionary with stress analysis and reasoning
        """
        metrics = {}
        risks = []
        strengths = []
        
        # Analyze stress level if available
        if "level" in stress_data:
            level = stress_data["level"]
            metrics["level"] = level
            
            # Determine stress category
            for category, details in self.guidelines["stress_level"].items():
                lower, upper = details["range"]
                if lower <= level < upper:
                    stress_category = category
                    evidence = details["evidence"].value
                    break
            
            # Add risks or strengths based on stress level
            if stress_category == "high":
                risks.append({
                    "type": "high_stress",
                    "description": "High stress levels are associated with increased risk of cardiovascular disease, immune dysfunction, and mental health disorders.",
                    "evidence": evidence
                })
            elif stress_category == "low":
                strengths.append({
                    "type": "low_stress",
                    "description": "Low stress levels support overall health and reduce risk of stress-related disorders.",
                    "evidence": evidence
                })
        
        # Analyze stress sources if available
        if "sources" in stress_data and isinstance(stress_data["sources"], list):
            metrics["sources"] = stress_data["sources"]
            
            # Check for chronic stressors
            chronic_stressors = ["financial", "work", "chronic_illness", "caregiving"]
            has_chronic_stressors = any(source in chronic_stressors for source in stress_data["sources"])
            
            if has_chronic_stressors and stress_category in ["moderate", "high"]:
                risks.append({
                    "type": "chronic_stress",
                    "description": "Chronic stressors can lead to allostatic load and increased risk of stress-related disorders.",
                    "evidence": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Analyze coping mechanisms if available
        if "coping_mechanisms" in stress_data and isinstance(stress_data["coping_mechanisms"], list):
            metrics["coping_mechanisms"] = stress_data["coping_mechanisms"]
            
            # Check for healthy coping mechanisms
            healthy_coping = ["meditation", "exercise", "social_support", "therapy", "mindfulness"]
            has_healthy_coping = any(mechanism in healthy_coping for mechanism in stress_data["coping_mechanisms"])
            
            if has_healthy_coping:
                strengths.append({
                    "type": "healthy_stress_coping",
                    "description": "Healthy stress coping mechanisms can buffer the negative effects of stress.",
                    "evidence": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Generate clinical reasoning
        reasoning_parts = []
        
        if "level" in stress_data:
            reasoning_parts.append(
                f"User reports stress level of {stress_data['level']} on a scale of 1-10. "
                f"Guideline categorizes this as {stress_category} stress. "
            )
            
            if stress_category == "high":
                reasoning_parts.append(
                    "High stress is associated with increased risk of cardiovascular disease, immune dysfunction, and mental health disorders. "
                )
            elif stress_category == "moderate":
                reasoning_parts.append(
                    "Moderate stress may have both positive and negative effects depending on duration and coping mechanisms. "
                )
            else:  # low
                reasoning_parts.append(
                    "Low stress levels are generally associated with better health outcomes. "
                )
        
        if "sources" in stress_data:
            sources_str = ", ".join(stress_data["sources"])
            reasoning_parts.append(f"Reported stress sources: {sources_str}. ")
            
            if has_chronic_stressors:
                reasoning_parts.append(
                    "Chronic stressors identified, which can lead to allostatic load and increased health risks. "
                )
        
        if "coping_mechanisms" in stress_data:
            coping_str = ", ".join(stress_data["coping_mechanisms"])
            reasoning_parts.append(f"Reported coping mechanisms: {coping_str}. ")
            
            if has_healthy_coping:
                reasoning_parts.append(
                    "Healthy coping mechanisms identified, which can buffer negative effects of stress. "
                )
        
        # Add confidence assessment
        stress_data_points = len([key for key in ["level", "sources", "coping_mechanisms"] if key in stress_data])
        if stress_data_points >= 3:
            reasoning_parts.append("Confidence is high based on comprehensive stress data.")
        elif stress_data_points >= 2:
            reasoning_parts.append("Confidence is medium due to partial stress data.")
        else:
            reasoning_parts.append("Confidence is low due to limited stress data.")
        
        reasoning = "".join(reasoning_parts)
        
        # Generate guideline assessment
        guideline_assessment = {
            "metric": "Stress Level",
            "value": stress_data.get("level"),
            "category": stress_category if "level" in stress_data else "unknown",
            "reference_range": "0-3 (low), 4-6 (moderate), 7-10 (high)",
            "guideline_source": "Expert consensus on psychological stress assessment",
            "evidence_category": evidence if "level" in stress_data else EvidenceCategory.EXPERT_OPINION.value
        }
        
        return {
            "metrics": metrics,
            "risks": risks,
            "strengths": strengths,
            "reasoning": reasoning,
            "guideline_assessment": guideline_assessment
        }
    
    def _analyze_physical_activity(self, exercise_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze physical activity data with clinical reasoning
        
        Args:
            exercise_data: Dictionary containing exercise data
            
        Returns:
            Dictionary with physical activity analysis and reasoning
        """
        metrics = {}
        risks = []
        strengths = []
        
        # Calculate total weekly exercise sessions
        weekly_sessions = 0
        if "strength_training" in exercise_data:
            weekly_sessions += exercise_data["strength_training"]
            metrics["strength_training_sessions"] = exercise_data["strength_training"]
        
        if "cardio" in exercise_data:
            weekly_sessions += exercise_data["cardio"]
            metrics["cardio_sessions"] = exercise_data["cardio"]
        
        metrics["total_weekly_sessions"] = weekly_sessions
        
        # Estimate weekly minutes (if duration is available)
        weekly_minutes = None
        if "duration" in exercise_data:
            weekly_minutes = weekly_sessions * exercise_data["duration"]
            metrics["estimated_weekly_minutes"] = weekly_minutes
        
        # Analyze against guidelines
        min_recommended_days = self.guidelines["physical_activity"]["recommended_days"]["minimum"]
        optimal_recommended_days = self.guidelines["physical_activity"]["recommended_days"]["optimal"]
        recommended_moderate_minutes = self.guidelines["physical_activity"]["recommended_weekly_minutes"]["moderate_intensity"]
        
        # Assess activity level
        if weekly_sessions < min_recommended_days:
            activity_level = "insufficient"
            risks.append({
                "type": "insufficient_physical_activity",
                "description": "Insufficient physical activity increases risk of cardiovascular disease, type 2 diabetes, and all-cause mortality.",
                "evidence": EvidenceCategory.CLINICAL_GUIDELINES.value
            })
        elif weekly_sessions >= optimal_recommended_days:
            activity_level = "optimal"
            strengths.append({
                "type": "regular_physical_activity",
                "description": "Regular physical activity reduces risk of chronic diseases and supports overall health.",
                "evidence": EvidenceCategory.CLINICAL_GUIDELINES.value
            })
        else:
            activity_level = "adequate"
            strengths.append({
                "type": "moderate_physical_activity",
                "description": "Moderate physical activity provides health benefits, though increased frequency may offer additional benefits.",
                "evidence": EvidenceCategory.CLINICAL_GUIDELINES.value
            })
        
        # Assess balance between strength and cardio
        if "strength_training" in exercise_data and "cardio" in exercise_data:
            if exercise_data["strength_training"] >= 2 and exercise_data["cardio"] >= 2:
                strengths.append({
                    "type": "balanced_exercise_routine",
                    "description": "Balanced exercise routine with both strength and cardiovascular components supports overall fitness.",
                    "evidence": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
            elif exercise_data["strength_training"] < 2 and exercise_data["cardio"] >= 2:
                risks.append({
                    "type": "insufficient_strength_training",
                    "description": "Insufficient strength training may lead to reduced muscle mass, bone density, and metabolic health.",
                    "evidence": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
            elif exercise_data["strength_training"] >= 2 and exercise_data["cardio"] < 2:
                risks.append({
                    "type": "insufficient_cardiovascular_exercise",
                    "description": "Insufficient cardiovascular exercise may lead to reduced cardiorespiratory fitness and increased cardiovascular risk.",
                    "evidence": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
        
        # Generate clinical reasoning
        reasoning_parts = []
        
        reasoning_parts.append(
            f"User reports {weekly_sessions} total exercise sessions per week "
            f"({exercise_data.get('strength_training', 0)} strength, {exercise_data.get('cardio', 0)} cardio). "
        )
        
        reasoning_parts.append(
            f"Guidelines recommend a minimum of {min_recommended_days} days of exercise per week, "
            f"with {recommended_moderate_minutes} minutes of moderate-intensity activity. "
        )
        
        if weekly_minutes is not None:
            reasoning_parts.append(
                f"Estimated weekly exercise: {weekly_minutes} minutes. "
            )
        
        if activity_level == "insufficient":
            reasoning_parts.append(
                "Physical activity level is below recommended guidelines, which increases risk of chronic diseases. "
            )
        elif activity_level == "optimal":
            reasoning_parts.append(
                "Physical activity level meets or exceeds optimal recommendations, which provides substantial health benefits. "
            )
        else:
            reasoning_parts.append(
                "Physical activity level meets minimum recommendations but could be increased for optimal benefits. "
            )
        
        if "intensity" in exercise_data:
            reasoning_parts.append(
                f"User reports {exercise_data['intensity']} exercise intensity. "
            )
        
        # Add confidence assessment
        exercise_data_points = len([key for key in ["strength_training", "cardio", "intensity", "duration", "types"] if key in exercise_data])
        if exercise_data_points >= 4:
            reasoning_parts.append("Confidence is high based on comprehensive exercise data.")
        elif exercise_data_points >= 3:
            reasoning_parts.append("Confidence is medium due to partial exercise data.")
        else:
            reasoning_parts.append("Confidence is low due to limited exercise data.")
        
        reasoning = "".join(reasoning_parts)
        
        # Generate guideline assessment
        guideline_assessment = {
            "metric": "Physical Activity",
            "value": f"{weekly_sessions} sessions/week",
            "category": activity_level,
            "reference_range": f"Minimum: {min_recommended_days} days/week, Optimal: {optimal_recommended_days} days/week",
            "guideline_source": "WHO/ACSM Physical Activity Guidelines",
            "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
        }
        
        return {
            "metrics": metrics,
            "risks": risks,
            "strengths": strengths,
            "reasoning": reasoning,
            "guideline_assessment": guideline_assessment
        }
    
    def _analyze_vo2_max(self, vo2_max: float, gender: str, age: int) -> Dict[str, Any]:
        """
        Analyze VO2 max with clinical reasoning
        
        Args:
            vo2_max: VO2 max value in ml/kg/min
            gender: User gender
            age: User age in years
            
        Returns:
            Dictionary with VO2 max analysis and reasoning
        """
        # Determine VO2 max category based on gender
        category = None
        if gender.lower() in ["male", "m"]:
            for cat, details in self.guidelines["vo2_max"].items():
                lower, upper = details["male"]["range"]
                if lower <= vo2_max < upper:
                    category = cat
                    break
        elif gender.lower() in ["female", "f"]:
            for cat, details in self.guidelines["vo2_max"].items():
                lower, upper = details["female"]["range"]
                if lower <= vo2_max < upper:
                    category = cat
                    break
        else:
            # If gender is unknown, use average of male and female ranges
            for cat, details in self.guidelines["vo2_max"].items():
                male_lower, male_upper = details["male"]["range"]
                female_lower, female_upper = details["female"]["range"]
                avg_lower = (male_lower + female_lower) / 2
                avg_upper = (male_upper + female_upper) / 2
                if avg_lower <= vo2_max < avg_upper:
                    category = cat
                    break
        
        # Generate description based on category
        descriptions = {
            "poor": f"VO2 max of {vo2_max} ml/kg/min indicates poor cardiorespiratory fitness, associated with increased mortality risk.",
            "fair": f"VO2 max of {vo2_max} ml/kg/min indicates fair cardiorespiratory fitness, with room for improvement.",
            "good": f"VO2 max of {vo2_max} ml/kg/min indicates good cardiorespiratory fitness, associated with reduced health risks.",
            "excellent": f"VO2 max of {vo2_max} ml/kg/min indicates excellent cardiorespiratory fitness, associated with significant health benefits.",
            "superior": f"VO2 max of {vo2_max} ml/kg/min indicates superior cardiorespiratory fitness, associated with optimal health outcomes."
        }
        
        description = descriptions.get(category, f"VO2 max of {vo2_max} ml/kg/min")
        
        # Generate clinical reasoning
        gender_specific_range = None
        if gender.lower() in ["male", "m"]:
            lower, upper = self.guidelines["vo2_max"][category]["male"]["range"]
            gender_specific_range = f"{lower}-{upper if upper != float('inf') else '+'} ml/kg/min for males"
        elif gender.lower() in ["female", "f"]:
            lower, upper = self.guidelines["vo2_max"][category]["female"]["range"]
            gender_specific_range = f"{lower}-{upper if upper != float('inf') else '+'} ml/kg/min for females"
        else:
            gender_specific_range = "unknown range due to unspecified gender"
        
        reasoning = (
            f"User reports VO2 max of {vo2_max} ml/kg/min. "
            f"For a {age}-year-old {gender}, this falls in the '{category}' category ({gender_specific_range}). "
            f"{description} "
            f"VO2 max is a strong predictor of cardiovascular health and all-cause mortality. "
            f"Confidence is medium as this is likely a proxy measure rather than a direct laboratory assessment."
        )
        
        # Generate guideline assessment
        guideline_assessment = {
            "metric": "VO2 Max",
            "value": vo2_max,
            "category": category,
            "reference_range": gender_specific_range,
            "guideline_source": "American College of Sports Medicine",
            "evidence_category": EvidenceCategory.SYSTEMATIC_REVIEW.value
        }
        
        return {
            "value": vo2_max,
            "category": category,
            "description": description,
            "reasoning": reasoning,
            "guideline_assessment": guideline_assessment,
            "evidence": EvidenceCategory.SYSTEMATIC_REVIEW.value
        }
    
    def _analyze_health_metrics(self, health_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze health metrics with clinical reasoning
        
        Args:
            health_metrics: Dictionary containing health metrics
            
        Returns:
            Dictionary with health metrics analysis and reasoning
        """
        metrics = {}
        risks = []
        strengths = []
        guideline_assessments = []
        reasoning_parts = []
        
        # Analyze blood pressure if available
        if "blood_pressure_systolic" in health_metrics and "blood_pressure_diastolic" in health_metrics:
            systolic = health_metrics["blood_pressure_systolic"]
            diastolic = health_metrics["blood_pressure_diastolic"]
            metrics["blood_pressure"] = f"{systolic}/{diastolic} mmHg"
            
            # Determine blood pressure category
            bp_category = None
            for category, details in self.guidelines["blood_pressure"].items():
                systolic_range = details["systolic"]["range"]
                diastolic_range = details["diastolic"]["range"]
                
                if (systolic_range[0] <= systolic < systolic_range[1] and 
                    diastolic_range[0] <= diastolic < diastolic_range[1]):
                    bp_category = category
                    break
            
            # If systolic and diastolic fall in different categories, use the higher category
            if bp_category is None:
                for category, details in self.guidelines["blood_pressure"].items():
                    systolic_range = details["systolic"]["range"]
                    diastolic_range = details["diastolic"]["range"]
                    
                    if (systolic_range[0] <= systolic < systolic_range[1] or 
                        diastolic_range[0] <= diastolic < diastolic_range[1]):
                        bp_category = category
                        break
            
            # Add risks or strengths based on blood pressure category
            if bp_category == "normal":
                strengths.append({
                    "type": "normal_blood_pressure",
                    "description": "Normal blood pressure is associated with reduced cardiovascular risk.",
                    "evidence": self.guidelines["blood_pressure"][bp_category]["evidence"].value
                })
            elif bp_category in ["elevated", "hypertension_stage_1", "hypertension_stage_2"]:
                risks.append({
                    "type": bp_category,
                    "description": f"Blood pressure in the {bp_category.replace('_', ' ')} range increases risk of cardiovascular disease.",
                    "evidence": self.guidelines["blood_pressure"][bp_category]["evidence"].value
                })
            
            # Add to reasoning
            reasoning_parts.append(
                f"User reports blood pressure of {systolic}/{diastolic} mmHg. "
                f"This falls in the '{bp_category.replace('_', ' ')}' category. "
            )
            
            if bp_category == "normal":
                reasoning_parts.append("Normal blood pressure is associated with reduced cardiovascular risk. ")
            elif bp_category == "elevated":
                reasoning_parts.append("Elevated blood pressure may progress to hypertension without intervention. ")
            elif bp_category in ["hypertension_stage_1", "hypertension_stage_2"]:
                reasoning_parts.append("Hypertension significantly increases risk of cardiovascular disease, stroke, and kidney disease. ")
            
            # Add guideline assessment
            guideline_assessments.append({
                "metric": "Blood Pressure",
                "value": f"{systolic}/{diastolic} mmHg",
                "category": bp_category,
                "reference_range": "Normal: <120/<80 mmHg",
                "guideline_source": "American Heart Association",
                "evidence_category": self.guidelines["blood_pressure"][bp_category]["evidence"].value
            })
        
        # Analyze heart rate if available
        if "heart_rate" in health_metrics:
            heart_rate = health_metrics["heart_rate"]
            metrics["heart_rate"] = f"{heart_rate} bpm"
            
            # Determine heart rate category
            hr_category = None
            for category, details in self.guidelines["heart_rate_resting"].items():
                lower, upper = details["range"]
                if lower <= heart_rate < upper:
                    hr_category = category
                    break
            
            # Add risks or strengths based on heart rate category
            if hr_category == "normal":
                strengths.append({
                    "type": "normal_heart_rate",
                    "description": "Normal resting heart rate indicates good cardiovascular function.",
                    "evidence": self.guidelines["heart_rate_resting"][hr_category]["evidence"].value
                })
            elif hr_category in ["bradycardia", "tachycardia"]:
                risks.append({
                    "type": hr_category,
                    "description": f"Resting heart rate in the {hr_category} range may indicate underlying cardiovascular issues.",
                    "evidence": self.guidelines["heart_rate_resting"][hr_category]["evidence"].value
                })
            
            # Add to reasoning
            reasoning_parts.append(
                f"User reports resting heart rate of {heart_rate} bpm. "
                f"This falls in the '{hr_category}' category. "
            )
            
            if hr_category == "normal":
                reasoning_parts.append("Normal resting heart rate indicates good cardiovascular function. ")
            elif hr_category == "bradycardia":
                reasoning_parts.append("Bradycardia may be normal in athletes but could indicate underlying issues in others. ")
            elif hr_category == "tachycardia":
                reasoning_parts.append("Tachycardia at rest may indicate stress, dehydration, or underlying cardiovascular issues. ")
            
            # Add guideline assessment
            guideline_assessments.append({
                "metric": "Resting Heart Rate",
                "value": f"{heart_rate} bpm",
                "category": hr_category,
                "reference_range": "Normal: 60-100 bpm",
                "guideline_source": "American Heart Association",
                "evidence_category": self.guidelines["heart_rate_resting"][hr_category]["evidence"].value
            })
        
        # Add confidence assessment
        health_metrics_count = len(health_metrics)
        if health_metrics_count >= 4:
            reasoning_parts.append("Confidence is high based on comprehensive health metrics.")
        elif health_metrics_count >= 2:
            reasoning_parts.append("Confidence is medium due to partial health metrics.")
        else:
            reasoning_parts.append("Confidence is low due to limited health metrics.")
        
        reasoning = "".join(reasoning_parts)
        
        return {
            "metrics": metrics,
            "risks": risks,
            "strengths": strengths,
            "reasoning": reasoning,
            "guideline_assessment": guideline_assessments
        }
    
    def _assess_bias_risks(self, relevant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess potential algorithm bias risks based on input data patterns
        
        Args:
            relevant_data: Dictionary containing relevant data for medical analysis
            
        Returns:
            Dictionary with bias risk assessment
        """
        bias_risks = []
        
        # Check for demographic representation
        if "gender" in relevant_data:
            gender = relevant_data["gender"].lower()
            if gender not in ["male", "female", "m", "f"]:
                bias_risks.append({
                    "type": "gender_representation",
                    "risk_level": BiasRiskLevel.MEDIUM.value,
                    "description": "Non-binary gender data may not be well-represented in medical reference ranges and guidelines."
                })
        
        # Check for age representation
        if "age" in relevant_data:
            age = relevant_data["age"]
            if age < 18 or age > 80:
                bias_risks.append({
                    "type": "age_representation",
                    "risk_level": BiasRiskLevel.MEDIUM.value,
                    "description": f"Age {age} may be under-represented in reference data for some health metrics."
                })
        
        # Check for BMI limitations
        if "height" in relevant_data and "weight" in relevant_data:
            height_m = relevant_data["height"] / 100
            weight_kg = relevant_data["weight"]
            bmi = weight_kg / (height_m * height_m)
            
            if bmi < 18.5 or bmi > 35:
                bias_risks.append({
                    "type": "bmi_representation",
                    "risk_level": BiasRiskLevel.MEDIUM.value,
                    "description": "Extreme BMI values may not be well-represented in reference data for some health metrics."
                })
            
            # Check for athletic body composition
            if "exercise_data" in relevant_data:
                exercise_data = relevant_data["exercise_data"]
                if (exercise_data.get("strength_training", 0) >= 4 or 
                    exercise_data.get("cardio", 0) >= 5) and bmi >= 25:
                    bias_risks.append({
                        "type": "athletic_body_composition",
                        "risk_level": BiasRiskLevel.HIGH.value,
                        "description": "BMI may overestimate health risks in athletic individuals with high muscle mass."
                    })
        
        # Check for data completeness bias
        completeness = self._assess_data_completeness(relevant_data)
        if completeness["level"] in ["minimal", "partial"]:
            bias_risks.append({
                "type": "incomplete_data",
                "risk_level": BiasRiskLevel.HIGH.value,
                "description": "Incomplete data may lead to biased assessments due to missing context."
            })
        
        # Generate summary assessment
        if not bias_risks:
            overall_risk = BiasRiskLevel.LOW.value
            summary = "No significant algorithm bias risks identified based on available data."
        elif any(risk["risk_level"] == BiasRiskLevel.HIGH.value for risk in bias_risks):
            overall_risk = BiasRiskLevel.HIGH.value
            summary = "High risk of algorithm bias detected. Recommendations should be interpreted with caution."
        elif any(risk["risk_level"] == BiasRiskLevel.MEDIUM.value for risk in bias_risks):
            overall_risk = BiasRiskLevel.MEDIUM.value
            summary = "Moderate risk of algorithm bias detected. Consider individual context when interpreting recommendations."
        else:
            overall_risk = BiasRiskLevel.LOW.value
            summary = "Low risk of algorithm bias detected."
        
        return {
            "overall_risk": overall_risk,
            "summary": summary,
            "specific_risks": bias_risks
        }
    
    def _assess_app_usage_risks(self, relevant_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Assess potential risks of using the app based on the user's profile
        
        Args:
            relevant_data: Dictionary containing relevant data for medical analysis
            
        Returns:
            List of dictionaries with app usage risk assessments
        """
        app_risks = []
        
        # Check for serious health conditions that require professional care
        if "health_metrics" in relevant_data:
            health_metrics = relevant_data["health_metrics"]
            
            # Check for severe hypertension
            if ("blood_pressure_systolic" in health_metrics and 
                health_metrics["blood_pressure_systolic"] >= 180) or \
               ("blood_pressure_diastolic" in health_metrics and 
                health_metrics["blood_pressure_diastolic"] >= 120):
                app_risks.append({
                    "type": "severe_hypertension",
                    "risk_level": "high",
                    "description": "Severe hypertension detected. User should seek immediate medical attention rather than relying on app recommendations."
                })
            
            # Check for extreme heart rate
            if "heart_rate" in health_metrics:
                heart_rate = health_metrics["heart_rate"]
                if heart_rate < 40 or heart_rate > 120:
                    app_risks.append({
                        "type": "abnormal_heart_rate",
                        "risk_level": "high",
                        "description": "Abnormal resting heart rate detected. User should consult a healthcare provider rather than relying on app recommendations."
                    })
        
        # Check for extreme BMI that requires medical supervision
        if "height" in relevant_data and "weight" in relevant_data:
            height_m = relevant_data["height"] / 100
            weight_kg = relevant_data["weight"]
            bmi = weight_kg / (height_m * height_m)
            
            if bmi < 16 or bmi > 40:
                app_risks.append({
                    "type": "extreme_bmi",
                    "risk_level": "high",
                    "description": "Extreme BMI detected. Weight management should be supervised by healthcare professionals rather than app recommendations alone."
                })
        
        # Check for severe sleep disorders
        if "sleep_data" in relevant_data:
            sleep_data = relevant_data["sleep_data"]
            if "average_duration" in sleep_data and sleep_data["average_duration"] < 4:
                app_risks.append({
                    "type": "severe_sleep_deprivation",
                    "risk_level": "medium",
                    "description": "Severe sleep deprivation detected. User should consult a healthcare provider for proper evaluation."
                })
            
            if "issues" in sleep_data and isinstance(sleep_data["issues"], list):
                serious_issues = ["sleep_apnea", "insomnia", "narcolepsy"]
                has_serious_issues = any(issue in serious_issues for issue in sleep_data["issues"])
                if has_serious_issues:
                    app_risks.append({
                        "type": "sleep_disorder",
                        "risk_level": "medium",
                        "description": "Potential sleep disorder detected. User should consult a sleep specialist for proper diagnosis and treatment."
                    })
        
        # Check for severe stress
        if "stress_data" in relevant_data:
            stress_data = relevant_data["stress_data"]
            if "level" in stress_data and stress_data["level"] >= 9:
                app_risks.append({
                    "type": "severe_stress",
                    "risk_level": "medium",
                    "description": "Severe stress detected. User may benefit from professional mental health support in addition to app recommendations."
                })
        
        # Check for data completeness
        completeness = self._assess_data_completeness(relevant_data)
        if completeness["level"] == "minimal":
            app_risks.append({
                "type": "insufficient_data",
                "risk_level": "medium",
                "description": "Insufficient data for reliable recommendations. User should provide more complete health information or consult healthcare providers."
            })
        
        return app_risks

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate medical recommendations based on the detailed clinical analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing recommendations
        """
        recommendations = []
        
        # Add recommendations based on BMI
        if "metrics" in analysis and "bmi" in analysis["metrics"]:
            bmi = analysis["metrics"]["bmi"]
            
            if bmi < 18.5:
                recommendations.append({
                    "type": "medical",
                    "category": "weight_management",
                    "action": "healthy_weight_gain",
                    "description": "Consult with a healthcare provider about healthy weight gain strategies",
                    "priority": "medium",
                    "reasoning": "BMI below 18.5 indicates underweight status, which may be associated with nutritional deficiencies",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
            elif bmi >= 30:
                recommendations.append({
                    "type": "medical",
                    "category": "weight_management",
                    "action": "obesity_management",
                    "description": "Consult with a healthcare provider about evidence-based weight management strategies",
                    "priority": "high",
                    "reasoning": "BMI of 30 or higher indicates obesity, which significantly increases risk of multiple chronic diseases",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
            elif bmi >= 25:
                recommendations.append({
                    "type": "medical",
                    "category": "weight_management",
                    "action": "weight_management",
                    "description": "Consider implementing a moderate weight management plan focusing on balanced nutrition and regular physical activity",
                    "priority": "medium",
                    "reasoning": "BMI between 25-30 indicates overweight status, which moderately increases risk of chronic diseases",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
        
        # Add recommendations based on sleep analysis
        if "metrics" in analysis and "sleep" in analysis["metrics"]:
            sleep_metrics = analysis["metrics"]["sleep"]
            
            if "average_duration" in sleep_metrics:
                duration = sleep_metrics["average_duration"]
                
                if duration < 7:
                    recommendations.append({
                        "type": "medical",
                        "category": "sleep",
                        "action": "improve_sleep_duration",
                        "description": "Aim for 7-9 hours of quality sleep per night for optimal health",
                        "priority": "high",
                        "reasoning": "Insufficient sleep duration increases risk of cognitive impairment, mood disorders, and metabolic dysfunction",
                        "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                    })
            
            if "bedtime_consistency" in sleep_metrics and sleep_metrics["bedtime_consistency"] in ["low", "poor"]:
                recommendations.append({
                    "type": "medical",
                    "category": "sleep",
                    "action": "improve_sleep_consistency",
                    "description": "Maintain a consistent sleep and wake schedule, even on weekends",
                    "priority": "high",
                    "reasoning": "Irregular sleep schedules disrupt circadian rhythms and are associated with metabolic dysfunction",
                    "evidence_category": EvidenceCategory.OBSERVATIONAL_STUDY.value
                })
        
        # Add recommendations based on stress analysis
        if "metrics" in analysis and "stress" in analysis["metrics"]:
            stress_metrics = analysis["metrics"]["stress"]
            
            if "level" in stress_metrics and stress_metrics["level"] >= 7:
                recommendations.append({
                    "type": "medical",
                    "category": "stress_management",
                    "action": "stress_reduction",
                    "description": "Implement evidence-based stress management techniques such as mindfulness meditation, deep breathing exercises, or professional counseling",
                    "priority": "high",
                    "reasoning": "High stress levels are associated with increased risk of cardiovascular disease, immune dysfunction, and mental health disorders",
                    "evidence_category": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Add recommendations based on physical activity analysis
        if "metrics" in analysis and "physical_activity" in analysis["metrics"]:
            activity_metrics = analysis["metrics"]["physical_activity"]
            
            if "total_weekly_sessions" in activity_metrics:
                sessions = activity_metrics["total_weekly_sessions"]
                
                if sessions < 3:
                    recommendations.append({
                        "type": "medical",
                        "category": "physical_activity",
                        "action": "increase_physical_activity",
                        "description": "Gradually increase physical activity to at least 150 minutes of moderate-intensity exercise per week",
                        "priority": "high",
                        "reasoning": "Insufficient physical activity increases risk of cardiovascular disease, type 2 diabetes, and all-cause mortality",
                        "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                    })
            
            if "strength_training_sessions" in activity_metrics and activity_metrics["strength_training_sessions"] < 2:
                recommendations.append({
                    "type": "medical",
                    "category": "physical_activity",
                    "action": "add_strength_training",
                    "description": "Incorporate strength training exercises at least twice per week",
                    "priority": "medium",
                    "reasoning": "Strength training improves muscle mass, bone density, and metabolic health",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
            
            if "cardio_sessions" in activity_metrics and activity_metrics["cardio_sessions"] < 2:
                recommendations.append({
                    "type": "medical",
                    "category": "physical_activity",
                    "action": "add_cardiovascular_exercise",
                    "description": "Incorporate cardiovascular exercise at least twice per week",
                    "priority": "medium",
                    "reasoning": "Cardiovascular exercise improves cardiorespiratory fitness and reduces cardiovascular risk",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
        
        # Add recommendations based on VO2 max analysis
        if "metrics" in analysis and "vo2_max" in analysis["metrics"]:
            vo2_max = analysis["metrics"]["vo2_max"]
            
            # Check if any health risk related to cardiorespiratory fitness exists
            has_cardio_fitness_risk = any(
                risk["type"] == "low_cardiorespiratory_fitness" 
                for risk in analysis["health_risks"]
            )
            
            if has_cardio_fitness_risk:
                recommendations.append({
                    "type": "medical",
                    "category": "cardiorespiratory_fitness",
                    "action": "improve_cardiorespiratory_fitness",
                    "description": "Gradually increase aerobic exercise frequency and intensity to improve cardiorespiratory fitness",
                    "priority": "high",
                    "reasoning": "Low cardiorespiratory fitness is associated with increased mortality risk",
                    "evidence_category": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Add recommendations based on health metrics analysis
        if "metrics" in analysis:
            metrics = analysis["metrics"]
            
            if "blood_pressure" in metrics and any(
                risk["type"] in ["elevated", "hypertension_stage_1", "hypertension_stage_2"] 
                for risk in analysis["health_risks"]
            ):
                recommendations.append({
                    "type": "medical",
                    "category": "cardiovascular_health",
                    "action": "monitor_blood_pressure",
                    "description": "Regularly monitor blood pressure and consult with a healthcare provider if consistently elevated",
                    "priority": "high",
                    "reasoning": "Elevated blood pressure increases risk of cardiovascular disease, stroke, and kidney disease",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
                
                # Add lifestyle recommendations for blood pressure management
                recommendations.append({
                    "type": "medical",
                    "category": "cardiovascular_health",
                    "action": "dash_diet",
                    "description": "Consider following the DASH diet (Dietary Approaches to Stop Hypertension), which emphasizes fruits, vegetables, whole grains, and low-fat dairy",
                    "priority": "medium",
                    "reasoning": "The DASH diet has been shown to reduce blood pressure in clinical trials",
                    "evidence_category": EvidenceCategory.RANDOMIZED_TRIAL.value
                })
        
        # Add general preventive care recommendation (almost always included)
        recommendations.append({
            "type": "medical",
            "category": "preventive_care",
            "action": "regular_checkup",
            "description": "Schedule a regular health check-up with your primary care physician",
            "priority": "medium",
            "reasoning": "Regular preventive care can identify health issues early when they are most treatable",
            "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
        })
        
        # Add recommendation based on data completeness
        if analysis["data_completeness"]["level"] in ["minimal", "partial"]:
            recommendations.append({
                "type": "medical",
                "category": "data_collection",
                "action": "complete_health_profile",
                "description": "Complete your health profile with additional metrics for more accurate assessment",
                "priority": "high",
                "reasoning": f"Current data completeness is {analysis['data_completeness']['level']} ({analysis['data_completeness']['overall_percentage']}%)",
                "evidence_category": EvidenceCategory.EXPERT_OPINION.value
            })
        
        # Add recommendations based on app usage risks
        if analysis["app_usage_risks"]:
            high_risks = [risk for risk in analysis["app_usage_risks"] if risk["risk_level"] == "high"]
            
            if high_risks:
                recommendations.append({
                    "type": "medical",
                    "category": "medical_consultation",
                    "action": "seek_medical_advice",
                    "description": "Consult with a healthcare provider before implementing any health recommendations from this app",
                    "priority": "high",
                    "reasoning": "Your health profile indicates conditions that require professional medical evaluation",
                    "evidence_category": EvidenceCategory.EXPERT_OPINION.value
                })
        
        return recommendations
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate medical insights based on the detailed clinical analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of dictionaries containing insights
        """
        insights = []
        
        # Generate overall health status insight
        health_risks_count = len(analysis["health_risks"])
        health_strengths_count = len(analysis["health_strengths"])
        
        if health_risks_count == 0 and health_strengths_count >= 3:
            health_status = "excellent"
        elif health_risks_count <= 1 and health_strengths_count >= 2:
            health_status = "good"
        elif health_risks_count <= 3:
            health_status = "fair"
        else:
            health_status = "concerning"
        
        insights.append({
            "type": "overall_health_status",
            "description": f"Overall health status appears to be {health_status} based on available data",
            "confidence": analysis["data_completeness"]["confidence"],
            "reasoning": f"Assessment based on {health_risks_count} identified health risks and {health_strengths_count} health strengths",
            "evidence_category": EvidenceCategory.EXPERT_OPINION.value
        })
        
        # Generate insights for each health domain
        
        # BMI insight
        if "metrics" in analysis and "bmi" in analysis["metrics"]:
            bmi = analysis["metrics"]["bmi"]
            bmi_category = None
            
            if bmi < 18.5:
                bmi_category = "underweight"
            elif bmi < 25:
                bmi_category = "healthy weight"
            elif bmi < 30:
                bmi_category = "overweight"
            else:
                bmi_category = "obese"
            
            insights.append({
                "type": "bmi",
                "description": f"BMI of {bmi} indicates {bmi_category}",
                "confidence": "high",
                "reasoning": f"BMI calculation based on reported height and weight",
                "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
            })
        
        # Sleep insight
        if "metrics" in analysis and "sleep" in analysis["metrics"]:
            sleep_metrics = analysis["metrics"]["sleep"]
            sleep_issues = []
            
            if "average_duration" in sleep_metrics and sleep_metrics["average_duration"] < 7:
                sleep_issues.append("insufficient duration")
            
            if "quality" in sleep_metrics and sleep_metrics["quality"] in ["low", "poor"]:
                sleep_issues.append("poor quality")
            
            if "bedtime_consistency" in sleep_metrics and sleep_metrics["bedtime_consistency"] in ["low", "poor"]:
                sleep_issues.append("irregular schedule")
            
            if sleep_issues:
                insights.append({
                    "type": "sleep_pattern",
                    "description": f"Sleep pattern shows {', '.join(sleep_issues)}",
                    "confidence": "medium" if len(sleep_metrics) >= 2 else "low",
                    "reasoning": "Sleep quality and consistency significantly impact overall health and longevity",
                    "evidence_category": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
            else:
                insights.append({
                    "type": "sleep_pattern",
                    "description": "Sleep pattern appears healthy",
                    "confidence": "medium" if len(sleep_metrics) >= 2 else "low",
                    "reasoning": "Adequate sleep duration and quality support cognitive function and physical recovery",
                    "evidence_category": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Physical activity insight
        if "metrics" in analysis and "physical_activity" in analysis["metrics"]:
            activity_metrics = analysis["metrics"]["physical_activity"]
            
            if "total_weekly_sessions" in activity_metrics:
                sessions = activity_metrics["total_weekly_sessions"]
                
                if sessions < 3:
                    activity_level = "insufficient"
                elif sessions < 5:
                    activity_level = "adequate"
                else:
                    activity_level = "optimal"
                
                insights.append({
                    "type": "physical_activity",
                    "description": f"Physical activity level is {activity_level} with {sessions} sessions per week",
                    "confidence": "medium",
                    "reasoning": "Regular physical activity reduces risk of chronic diseases and supports longevity",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
        
        # Stress insight
        if "metrics" in analysis and "stress" in analysis["metrics"]:
            stress_metrics = analysis["metrics"]["stress"]
            
            if "level" in stress_metrics:
                level = stress_metrics["level"]
                
                if level >= 7:
                    stress_impact = "significant negative"
                elif level >= 4:
                    stress_impact = "moderate"
                else:
                    stress_impact = "minimal"
                
                insights.append({
                    "type": "stress_impact",
                    "description": f"Stress appears to have a {stress_impact} impact on health",
                    "confidence": "medium",
                    "reasoning": "Chronic stress affects cardiovascular, immune, and metabolic health",
                    "evidence_category": EvidenceCategory.SYSTEMATIC_REVIEW.value
                })
        
        # Cardiovascular health insight
        if "metrics" in analysis and any(key in analysis["metrics"] for key in ["blood_pressure", "heart_rate", "vo2_max"]):
            cardio_risks = []
            
            if "blood_pressure" in analysis["metrics"] and any(
                risk["type"] in ["elevated", "hypertension_stage_1", "hypertension_stage_2"] 
                for risk in analysis["health_risks"]
            ):
                cardio_risks.append("elevated blood pressure")
            
            if "heart_rate" in analysis["metrics"] and any(
                risk["type"] in ["bradycardia", "tachycardia"] 
                for risk in analysis["health_risks"]
            ):
                cardio_risks.append("abnormal resting heart rate")
            
            if "vo2_max" in analysis["metrics"] and any(
                risk["type"] == "low_cardiorespiratory_fitness" 
                for risk in analysis["health_risks"]
            ):
                cardio_risks.append("low cardiorespiratory fitness")
            
            if cardio_risks:
                insights.append({
                    "type": "cardiovascular_health",
                    "description": f"Cardiovascular health shows risk factors: {', '.join(cardio_risks)}",
                    "confidence": "medium",
                    "reasoning": "Cardiovascular health is a key determinant of longevity",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
            else:
                insights.append({
                    "type": "cardiovascular_health",
                    "description": "Cardiovascular health indicators appear within normal ranges",
                    "confidence": "medium",
                    "reasoning": "Healthy cardiovascular metrics are associated with reduced disease risk and increased longevity",
                    "evidence_category": EvidenceCategory.CLINICAL_GUIDELINES.value
                })
        
        # Algorithm bias insight
        if analysis["bias_risk_assessment"]["overall_risk"] != BiasRiskLevel.LOW.value:
            insights.append({
                "type": "algorithm_bias",
                "description": analysis["bias_risk_assessment"]["summary"],
                "confidence": "medium",
                "reasoning": "Health algorithms may have limitations when applied to certain populations or unusual health profiles",
                "evidence_category": EvidenceCategory.EXPERT_OPINION.value
            })
        
        # Data completeness insight
        insights.append({
            "type": "data_completeness",
            "description": f"Data completeness is {analysis['data_completeness']['level']} ({analysis['data_completeness']['overall_percentage']}%)",
            "confidence": "high",
            "reasoning": analysis["data_completeness"]["reasoning"],
            "evidence_category": EvidenceCategory.EXPERT_OPINION.value
        })
        
        return insights
    
    def _extract_key_findings(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key medical findings from the detailed clinical analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            List of strings containing key findings
        """
        key_findings = []
        
        # Add data completeness finding
        key_findings.append(f"Data completeness: {analysis['data_completeness']['level']} ({analysis['data_completeness']['overall_percentage']}%)")
        
        # Add key metrics
        if "metrics" in analysis:
            metrics = analysis["metrics"]
            
            if "bmi" in metrics:
                key_findings.append(f"BMI: {metrics['bmi']}")
            
            if "sleep" in metrics and "average_duration" in metrics["sleep"]:
                key_findings.append(f"Sleep duration: {metrics['sleep']['average_duration']} hours")
            
            if "physical_activity" in metrics and "total_weekly_sessions" in metrics["physical_activity"]:
                key_findings.append(f"Physical activity: {metrics['physical_activity']['total_weekly_sessions']} sessions/week")
            
            if "stress" in metrics and "level" in metrics["stress"]:
                key_findings.append(f"Stress level: {metrics['stress']['level']}/10")
            
            if "vo2_max" in metrics:
                key_findings.append(f"VO2 max: {metrics['vo2_max']} ml/kg/min")
            
            if "blood_pressure" in metrics:
                key_findings.append(f"Blood pressure: {metrics['blood_pressure']}")
            
            if "heart_rate" in metrics:
                key_findings.append(f"Heart rate: {metrics['heart_rate']}")
        
        # Add health risks
        for risk in analysis["health_risks"]:
            key_findings.append(f"Health risk: {risk['type']}")
        
        # Add health strengths
        for strength in analysis["health_strengths"]:
            key_findings.append(f"Health strength: {strength['type']}")
        
        # Add algorithm bias risk
        key_findings.append(f"Algorithm bias risk: {analysis['bias_risk_assessment']['overall_risk']}")
        
        # Add app usage risks if any
        if analysis["app_usage_risks"]:
            high_risks = [risk for risk in analysis["app_usage_risks"] if risk["risk_level"] == "high"]
            if high_risks:
                key_findings.append(f"App usage high risk: {high_risks[0]['type']}")
        
        return key_findings
    
    def _determine_confidence(self, analysis: Dict[str, Any]) -> ConfidenceLevel:
        """
        Determine the overall confidence level of the medical analysis
        
        Args:
            analysis: Dictionary containing analysis results
            
        Returns:
            ConfidenceLevel enum representing the confidence level
        """
        # Base confidence on data completeness
        data_completeness = analysis["data_completeness"]["level"]
        
        if data_completeness == "complete":
            base_confidence = ConfidenceLevel.HIGH
        elif data_completeness == "substantial":
            base_confidence = ConfidenceLevel.MEDIUM
        elif data_completeness == "partial":
            base_confidence = ConfidenceLevel.MEDIUM
        else:  # minimal
            base_confidence = ConfidenceLevel.LOW
        
        # Adjust confidence based on algorithm bias risk
        bias_risk = analysis["bias_risk_assessment"]["overall_risk"]
        
        if bias_risk == BiasRiskLevel.HIGH.value and base_confidence == ConfidenceLevel.HIGH:
            return ConfidenceLevel.MEDIUM
        elif bias_risk == BiasRiskLevel.HIGH.value and base_confidence == ConfidenceLevel.MEDIUM:
            return ConfidenceLevel.LOW
        elif bias_risk == BiasRiskLevel.MEDIUM.value and base_confidence == ConfidenceLevel.HIGH:
            return ConfidenceLevel.MEDIUM
        
        return base_confidence
