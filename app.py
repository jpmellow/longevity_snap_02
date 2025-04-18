"""
Longevity Snapshot App - Meta-Cognitive Processing API

This module implements a FastAPI-based API for the Meta-Cognitive Processing system
of the Longevity Snapshot app.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from meta_cognitive_processor import MetaCognitiveProcessor
from agents.medical_agent import MedicalAgent
from agents.sleep_agent import SleepAgent
from agents.medical_reasoning_agent import MedicalReasoningAgent
from agents.personalization_agent import PersonalizationAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("longevity_snapshot_api")

# Initialize FastAPI app
app = FastAPI(
    title="Longevity Snapshot Meta-Cognitive Processing API",
    description="API for processing health data and generating personalized recommendations",
    version="1.0.0"
)

# Initialize Meta-Cognitive Processor
processor = MetaCognitiveProcessor()

# Data models
class HealthMetrics(BaseModel):
    """Health metrics data model"""
    blood_pressure_systolic: Optional[int] = Field(None, description="Systolic blood pressure in mmHg")
    blood_pressure_diastolic: Optional[int] = Field(None, description="Diastolic blood pressure in mmHg")
    heart_rate: Optional[int] = Field(None, description="Resting heart rate in bpm")
    blood_glucose: Optional[float] = Field(None, description="Blood glucose level in mg/dL")
    cholesterol_total: Optional[int] = Field(None, description="Total cholesterol in mg/dL")
    cholesterol_hdl: Optional[int] = Field(None, description="HDL cholesterol in mg/dL")
    cholesterol_ldl: Optional[int] = Field(None, description="LDL cholesterol in mg/dL")
    triglycerides: Optional[int] = Field(None, description="Triglycerides in mg/dL")

class SleepData(BaseModel):
    """Sleep data model"""
    average_duration: float = Field(..., description="Average sleep duration in hours")
    quality: str = Field(..., description="Sleep quality (low, medium, high)")
    bedtime_consistency: str = Field(..., description="Bedtime consistency (low, medium, high)")
    issues: Optional[List[str]] = Field(None, description="List of sleep issues")

class NutritionData(BaseModel):
    """Nutrition data model"""
    calories: int = Field(..., description="Daily calorie intake")
    protein: float = Field(..., description="Daily protein intake in grams")
    carbs: float = Field(..., description="Daily carbohydrate intake in grams")
    fat: float = Field(..., description="Daily fat intake in grams")
    detailed_macros: Optional[bool] = Field(False, description="Whether detailed macronutrient data is available")
    fiber: Optional[float] = Field(None, description="Daily fiber intake in grams")
    sugar: Optional[float] = Field(None, description="Daily sugar intake in grams")
    water: Optional[float] = Field(None, description="Daily water intake in liters")

class StressData(BaseModel):
    """Stress data model"""
    level: int = Field(..., description="Stress level on a scale of 1-10")
    sources: Optional[List[str]] = Field(None, description="Sources of stress")
    coping_mechanisms: Optional[List[str]] = Field(None, description="Stress coping mechanisms")

class ExerciseData(BaseModel):
    """Exercise data model"""
    strength_training: int = Field(..., description="Weekly strength training sessions")
    cardio: int = Field(..., description="Weekly cardio sessions")
    intensity: str = Field(..., description="Exercise intensity (low, medium, high)")
    duration: Optional[int] = Field(None, description="Average exercise duration in minutes")
    types: Optional[List[str]] = Field(None, description="Types of exercises performed")

class Preferences(BaseModel):
    """User preferences model"""
    diet: Optional[str] = Field(None, description="Dietary preference")
    exercise_time: Optional[str] = Field(None, description="Preferred time for exercise")
    sleep_time: Optional[str] = Field(None, description="Preferred sleep time")
    wake_time: Optional[str] = Field(None, description="Preferred wake time")
    goals: Optional[List[str]] = Field(None, description="Health and wellness goals")

class UserHealthData(BaseModel):
    """User health data model"""
    user_id: str = Field(..., description="Unique user identifier")
    age: int = Field(..., description="User age in years")
    gender: str = Field(..., description="User gender")
    height: float = Field(..., description="User height in cm")
    weight: float = Field(..., description="User weight in kg")
    health_metrics: Optional[HealthMetrics] = Field(None, description="Health metrics data")
    sleep_data: Optional[SleepData] = Field(None, description="Sleep data")
    nutrition_data: Optional[NutritionData] = Field(None, description="Nutrition data")
    stress_data: Optional[StressData] = Field(None, description="Stress data")
    exercise_data: Optional[ExerciseData] = Field(None, description="Exercise data")
    preferences: Optional[Preferences] = Field(None, description="User preferences")
    medical_history: Optional[List[str]] = Field(None, description="Medical history items")

class ProcessingResponse(BaseModel):
    """Response model for processed health data"""
    user_id: str = Field(..., description="User ID from the request")
    timestamp: str = Field(..., description="Timestamp of the processing")
    recommendations: List[Dict[str, Any]] = Field(..., description="List of recommendations")
    insights: List[Dict[str, Any]] = Field(..., description="List of insights")
    confidence: str = Field(..., description="Overall confidence level of the analysis")
    agent_contributions: Dict[str, Any] = Field(..., description="Contributions from each agent")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the Longevity Snapshot Meta-Cognitive Processing API"}

@app.post("/process", response_model=ProcessingResponse)
async def process_health_data(user_data: UserHealthData):
    """
    Process user health data and generate personalized recommendations
    
    This endpoint:
    1. Receives user health data
    2. Determines which specialized agents are needed
    3. Routes data to selected agents
    4. Receives analyses back from agents
    5. Synthesizes outputs for the Recommendation Engine
    6. Flags low confidence or contradictions for review
    """
    try:
        logger.info(f"Processing health data for user: {user_data.user_id}")
        
        # Convert Pydantic model to dictionary
        user_data_dict = user_data.dict()
        
        # Process the data using the Meta-Cognitive Processor
        result = processor.process_health_data(user_data_dict)
        
        # Add timestamp and user_id to the response
        result["user_id"] = user_data.user_id
        result["timestamp"] = datetime.now().isoformat()
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing health data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing health data: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the API server
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
