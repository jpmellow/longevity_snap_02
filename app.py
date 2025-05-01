"""
Longevity Snapshot App - Meta-Cognitive Processing API

This module implements a Flask-based API for the Meta-Cognitive Processing system
of the Longevity Snapshot app.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from meta_cognitive_processor import MetaCognitiveProcessor
from agents.medical_agent import MedicalAgent
from agents.sleep_agent import SleepAgent
from agents.medical_reasoning_agent import MedicalReasoningAgent
from agents.personalization_agent import PersonalizationAgent

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("longevity_snapshot_api")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Meta-Cognitive Processor
processor = MetaCognitiveProcessor()

# Data models
class HealthMetrics:
    """Health metrics data model"""
    def __init__(self, 
                 blood_pressure_systolic: Optional[int] = None, 
                 blood_pressure_diastolic: Optional[int] = None, 
                 heart_rate: Optional[int] = None, 
                 blood_glucose: Optional[float] = None, 
                 cholesterol_total: Optional[int] = None, 
                 cholesterol_hdl: Optional[int] = None, 
                 cholesterol_ldl: Optional[int] = None, 
                 triglycerides: Optional[int] = None):
        self.blood_pressure_systolic = blood_pressure_systolic
        self.blood_pressure_diastolic = blood_pressure_diastolic
        self.heart_rate = heart_rate
        self.blood_glucose = blood_glucose
        self.cholesterol_total = cholesterol_total
        self.cholesterol_hdl = cholesterol_hdl
        self.cholesterol_ldl = cholesterol_ldl
        self.triglycerides = triglycerides

class SleepData:
    """Sleep data model"""
    def __init__(self, 
                 average_duration: float, 
                 quality: str, 
                 bedtime_consistency: str, 
                 issues: Optional[List[str]] = None, 
                 narrative: Optional[str] = None):
        self.average_duration = average_duration
        self.quality = quality
        self.bedtime_consistency = bedtime_consistency
        self.issues = issues
        self.narrative = narrative

class NutritionData:
    """Nutrition data model"""
    def __init__(self, 
                 calories: int, 
                 protein: float, 
                 carbs: float, 
                 fat: float, 
                 detailed_macros: Optional[bool] = False, 
                 fiber: Optional[float] = None, 
                 sugar: Optional[float] = None, 
                 water: Optional[float] = None):
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.detailed_macros = detailed_macros
        self.fiber = fiber
        self.sugar = sugar
        self.water = water

class StressData:
    """Stress data model"""
    def __init__(self, 
                 level: int, 
                 sources: Optional[List[str]] = None, 
                 coping_mechanisms: Optional[List[str]] = None):
        self.level = level
        self.sources = sources
        self.coping_mechanisms = coping_mechanisms

class ExerciseData:
    """Exercise data model"""
    def __init__(self, 
                 strength_training: int, 
                 cardio: int, 
                 intensity: str, 
                 duration: Optional[int] = None, 
                 types: Optional[List[str]] = None):
        self.strength_training = strength_training
        self.cardio = cardio
        self.intensity = intensity
        self.duration = duration
        self.types = types

class Preferences:
    """User preferences model"""
    def __init__(self, 
                 diet: Optional[str] = None, 
                 exercise_time: Optional[str] = None, 
                 sleep_time: Optional[str] = None, 
                 wake_time: Optional[str] = None, 
                 goals: Optional[List[str]] = None):
        self.diet = diet
        self.exercise_time = exercise_time
        self.sleep_time = sleep_time
        self.wake_time = wake_time
        self.goals = goals

class UserHealthData:
    """User health data model"""
    def __init__(self, 
                 user_id: str, 
                 age: int, 
                 gender: str, 
                 height: float, 
                 weight: float, 
                 health_metrics: Optional[HealthMetrics] = None, 
                 sleep_data: Optional[SleepData] = None, 
                 nutrition_data: Optional[NutritionData] = None, 
                 stress_data: Optional[StressData] = None, 
                 exercise_data: Optional[ExerciseData] = None, 
                 preferences: Optional[Preferences] = None, 
                 medical_history: Optional[List[str]] = None):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.health_metrics = health_metrics
        self.sleep_data = sleep_data
        self.nutrition_data = nutrition_data
        self.stress_data = stress_data
        self.exercise_data = exercise_data
        self.preferences = preferences
        self.medical_history = medical_history

class ProcessingResponse:
    """Response model for processed health data"""
    def __init__(self, 
                 user_id: str, 
                 timestamp: str, 
                 recommendations: List[Dict[str, Any]], 
                 insights: List[Dict[str, Any]], 
                 confidence: str, 
                 agent_contributions: Dict[str, Any], 
                 nlp_area: str, 
                 nlp_recommendation: str):
        self.user_id = user_id
        self.timestamp = timestamp
        self.recommendations = recommendations
        self.insights = insights
        self.confidence = confidence
        self.agent_contributions = agent_contributions
        self.nlp_area = nlp_area
        self.nlp_recommendation = nlp_recommendation

def analyze_sleep_narrative(narrative: str) -> Dict[str, str]:
    """
    Analyze sleep narrative using NLTK and TextBlob to extract key insights and generate recommendations.
    """
    if not narrative:
        return {
            "area": "unknown",
            "recommendation": "Please provide more details about your sleep patterns for personalized recommendations."
        }
    
    # Convert to lowercase and tokenize
    tokens = word_tokenize(narrative.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Define sleep-related keywords and their associated areas
    sleep_issues = {
        "stress": ["stress", "anxiety", "worried", "restless", "tense"],
        "schedule": ["schedule", "routine", "irregular", "inconsistent", "late", "early"],
        "environment": ["noise", "light", "temperature", "uncomfortable", "room"],
        "quality": ["quality", "deep", "light", "interrupted", "wake", "waking"],
        "duration": ["hours", "long", "short", "enough", "oversleep", "undersleep"]
    }
    
    # Count mentions of each area
    area_counts = {area: sum(1 for word in tokens if word in keywords) 
                  for area, keywords in sleep_issues.items()}
    
    # Get sentiment from TextBlob
    sentiment = TextBlob(narrative).sentiment.polarity
    
    # Get the most mentioned area
    primary_area = max(area_counts.items(), key=lambda x: x[1])[0] if any(area_counts.values()) else "general"
    
    # Generate recommendation based on the area and sentiment
    recommendations = {
        "stress": "Consider incorporating relaxation techniques like deep breathing or meditation before bedtime.",
        "schedule": "Try to maintain a consistent sleep schedule, even on weekends.",
        "environment": "Optimize your sleep environment by controlling light, noise, and temperature.",
        "quality": "Focus on sleep hygiene practices and avoid screens before bedtime.",
        "duration": "Aim for 7-9 hours of sleep per night for optimal health.",
        "general": "Consider keeping a sleep diary to identify patterns affecting your sleep quality."
    }
    
    # Add sentiment-based context to recommendation
    sentiment_context = ""
    if sentiment < -0.2:
        sentiment_context = " It seems you're experiencing some challenges. Start with small changes and be patient with yourself."
    elif sentiment > 0.2:
        sentiment_context = " You're on the right track! Keep building on your positive habits."
    
    return {
        "area": primary_area,
        "recommendation": recommendations[primary_area] + sentiment_context
    }

@app.route("/")
def root():
    """Root endpoint"""
    return {"status": "ok", "message": "Longevity Snapshot Meta-Cognitive Processing API"}

@app.route("/process", methods=["POST"])
def process_health_data():
    """
    Process user health data and generate personalized recommendations
    """
    try:
        user_data = request.json
        timestamp = datetime.now().isoformat()
        
        # Convert JSON data to UserHealthData object
        user_health_data = UserHealthData(**user_data)
        
        # Analyze sleep narrative if available
        sleep_narrative = user_health_data.sleep_data.narrative if user_health_data.sleep_data else None
        nlp_analysis = analyze_sleep_narrative(sleep_narrative or "")
        
        # Process data with existing logic...
        processed_data = processor.process_health_data(user_health_data.__dict__)
        
        return jsonify(ProcessingResponse(
            user_id=user_health_data.user_id,
            timestamp=timestamp,
            recommendations=processed_data["recommendations"],
            insights=processed_data["insights"],
            confidence=processed_data["confidence"],
            agent_contributions=processed_data["agent_contributions"],
            nlp_area=nlp_analysis["area"],
            nlp_recommendation=nlp_analysis["recommendation"]
        ).__dict__)
    
    except Exception as e:
        logger.error(f"Error processing health data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
