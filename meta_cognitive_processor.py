"""
Meta-Cognitive Processor for Longevity Snapshot App

This module serves as the central processing system that:
1. Receives user health data
2. Determines which specialized agents are needed
3. Routes data to selected agents
4. Receives analyses back from agents
5. Synthesizes outputs for the Recommendation Engine
6. Flags low confidence or contradictions for review
"""

from typing import Dict, List, Any, Optional, Set
from enum import Enum
import logging
import json

# Import the specialized agents
from agents.medical_reasoning_agent import MedicalReasoningAgent
from agents.personalization_agent import PersonalizationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("meta_cognitive_processor")

class AgentType(Enum):
    """Enum representing the different specialized agents available in the system"""
    MEDICAL = "medical"
    MEDICAL_REASONING = "medical_reasoning"
    NUTRITION = "nutrition"
    SLEEP = "sleep"
    STRESS = "stress"
    EXERCISE = "exercise"
    PERSONALIZATION = "personalization"
    CRITICAL_EVALUATION = "critical_evaluation"

class ConfidenceLevel(Enum):
    """Enum representing confidence levels for agent analyses"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"

class MetaCognitiveProcessor:
    """
    Central processing system that coordinates specialized agents,
    routes data, and synthesizes outputs for the Longevity Snapshot app.
    """
    
    def __init__(self):
        """Initialize the Meta-Cognitive Processor"""
        self.agents = {
            AgentType.MEDICAL: self._medical_agent,
            AgentType.MEDICAL_REASONING: self._medical_reasoning_agent,
            AgentType.NUTRITION: self._nutrition_agent,
            AgentType.SLEEP: self._sleep_agent,
            AgentType.STRESS: self._stress_agent,
            AgentType.EXERCISE: self._exercise_agent,
            AgentType.PERSONALIZATION: self._personalization_agent,
            AgentType.CRITICAL_EVALUATION: self._critical_evaluation_agent
        }
        
        # Initialize specialized agent instances
        self.medical_reasoning_agent = MedicalReasoningAgent()
        self.personalization_agent = PersonalizationAgent()
        
        logger.info("Meta-Cognitive Processor initialized")
    
    def process_health_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing function that handles user health data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary containing synthesized recommendations and analyses
        """
        logger.info(f"Processing health data for user: {user_data.get('user_id', 'unknown')}")
        
        # Step 1: Determine which agents to activate based on the data
        selected_agents = self._select_agents(user_data)
        logger.info(f"Selected agents: {[agent.value for agent in selected_agents]}")
        
        # Step 2: Route data to selected agents and collect their analyses
        agent_analyses = self._route_to_agents(selected_agents, user_data)
        
        # Step 3: Check for contradictions or low confidence analyses
        flagged_analyses = self._flag_issues(agent_analyses)
        
        # Step 4: If there are flagged issues, route to critical evaluation
        if flagged_analyses:
            logger.warning(f"Flagged {len(flagged_analyses)} analyses for review")
            critical_evaluation = self._critical_evaluation_agent(user_data, agent_analyses, flagged_analyses)
            # Update analyses with critical evaluation results
            for agent_type, evaluation in critical_evaluation.items():
                if agent_type in agent_analyses:
                    agent_analyses[agent_type]["evaluation_notes"] = evaluation
        
        # Step 5: Synthesize final output for the recommendation engine
        synthesized_output = self._synthesize_output(agent_analyses)
        
        return synthesized_output
    
    def _select_agents(self, user_data: Dict[str, Any]) -> Set[AgentType]:
        """
        Determine which specialized agents should be activated based on input data
        
        Args:
            user_data: Dictionary containing user health data
            
        Returns:
            Set of AgentType enums representing the selected agents
        """
        selected_agents = set()
        
        # Always include Medical Reasoning Agent for comprehensive health assessment
        selected_agents.add(AgentType.MEDICAL_REASONING)
        
        # Include regular Medical Agent only if Medical Reasoning Agent is not selected
        if AgentType.MEDICAL_REASONING not in selected_agents:
            selected_agents.add(AgentType.MEDICAL)
        
        # Decision logic for activating specific agents
        if "sleep_data" in user_data and user_data["sleep_data"]:
            selected_agents.add(AgentType.SLEEP)
            
        if "nutrition_data" in user_data and user_data["nutrition_data"]:
            # Check if nutrition data is complex (has detailed macros or multiple days)
            nutrition_data = user_data["nutrition_data"]
            if (isinstance(nutrition_data, list) and len(nutrition_data) > 3) or \
               (isinstance(nutrition_data, dict) and nutrition_data.get("detailed_macros")):
                selected_agents.add(AgentType.NUTRITION)
        
        if "stress_data" in user_data and user_data["stress_data"]:
            # Check if stress levels are high
            stress_data = user_data["stress_data"]
            if isinstance(stress_data, dict) and stress_data.get("level", 0) > 7:
                selected_agents.add(AgentType.STRESS)
            elif isinstance(stress_data, list) and any(item.get("level", 0) > 7 for item in stress_data):
                selected_agents.add(AgentType.STRESS)
        
        if "exercise_data" in user_data and user_data["exercise_data"]:
            selected_agents.add(AgentType.EXERCISE)
        
        # Always include Personalization Agent if user preferences exist
        if "preferences" in user_data and user_data["preferences"]:
            selected_agents.add(AgentType.PERSONALIZATION)
        
        return selected_agents
    
    def _route_to_agents(self, selected_agents: Set[AgentType], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route data to selected agents and collect their analyses
        
        Args:
            selected_agents: Set of AgentType enums representing the selected agents
            user_data: Dictionary containing user health data
            
        Returns:
            Dictionary mapping agent types to their analysis results
        """
        agent_analyses = {}
        
        for agent_type in selected_agents:
            agent_function = self.agents[agent_type]
            try:
                analysis = agent_function(user_data)
                agent_analyses[agent_type] = analysis
                logger.info(f"Received analysis from {agent_type.value} agent")
            except Exception as e:
                logger.error(f"Error processing data with {agent_type.value} agent: {str(e)}")
        
        return agent_analyses
    
    def _flag_issues(self, agent_analyses: Dict[AgentType, Any]) -> List[Dict[str, Any]]:
        """
        Identify contradictions or low confidence analyses
        
        Args:
            agent_analyses: Dictionary mapping agent types to their analysis results
            
        Returns:
            List of dictionaries containing flagged issues
        """
        flagged_issues = []
        
        # Check for low confidence
        for agent_type, analysis in agent_analyses.items():
            if "confidence" in analysis and analysis["confidence"] in [ConfidenceLevel.LOW.value, ConfidenceLevel.UNCERTAIN.value]:
                flagged_issues.append({
                    "agent": agent_type,
                    "issue_type": "low_confidence",
                    "details": analysis
                })
        
        # Check for contradictions between agents
        # Example: Medical agent recommends one thing but Nutrition agent contradicts
        if AgentType.MEDICAL in agent_analyses and AgentType.NUTRITION in agent_analyses:
            medical = agent_analyses[AgentType.MEDICAL]
            nutrition = agent_analyses[AgentType.NUTRITION]
            
            if "recommendations" in medical and "recommendations" in nutrition:
                med_rec_set = set(json.dumps(r) for r in medical["recommendations"])
                nut_rec_set = set(json.dumps(r) for r in nutrition["recommendations"])
                
                # Check for potential contradictions (simplified example)
                if any("reduce_calories" in r for r in med_rec_set) and any("increase_calories" in r for r in nut_rec_set):
                    flagged_issues.append({
                        "agent": [AgentType.MEDICAL, AgentType.NUTRITION],
                        "issue_type": "contradiction",
                        "details": "Conflicting recommendations about calorie intake"
                    })
        
        # Similar checks can be implemented for other agent combinations
        
        return flagged_issues
    
    def _synthesize_output(self, agent_analyses: Dict[AgentType, Any]) -> Dict[str, Any]:
        """
        Synthesize agent analyses into a final output for the recommendation engine
        
        Args:
            agent_analyses: Dictionary mapping agent types to their analysis results
            
        Returns:
            Dictionary containing synthesized recommendations and analyses
        """
        synthesized_output = {
            "recommendations": [],
            "insights": [],
            "confidence": ConfidenceLevel.HIGH.value,
            "agent_contributions": {}
        }
        
        # Combine recommendations from all agents
        for agent_type, analysis in agent_analyses.items():
            if "recommendations" in analysis:
                for rec in analysis["recommendations"]:
                    # Add source information to each recommendation
                    rec["source_agent"] = agent_type.value
                    synthesized_output["recommendations"].append(rec)
            
            if "insights" in analysis:
                for insight in analysis["insights"]:
                    # Add source information to each insight
                    insight["source_agent"] = agent_type.value
                    synthesized_output["insights"].append(insight)
            
            # Record agent contribution summary
            synthesized_output["agent_contributions"][agent_type.value] = {
                "confidence": analysis.get("confidence", ConfidenceLevel.MEDIUM.value),
                "key_findings": analysis.get("key_findings", [])
            }
        
        # Determine overall confidence level (lowest confidence among all agents)
        confidence_levels = [
            ConfidenceLevel(analysis.get("confidence", ConfidenceLevel.MEDIUM.value))
            for analysis in agent_analyses.values()
            if "confidence" in analysis
        ]
        
        if confidence_levels:
            # Sort confidence levels from lowest to highest
            sorted_confidence = sorted(confidence_levels, key=lambda x: [
                ConfidenceLevel.UNCERTAIN,
                ConfidenceLevel.LOW,
                ConfidenceLevel.MEDIUM,
                ConfidenceLevel.HIGH
            ].index(x))
            
            # Overall confidence is the lowest confidence among all agents
            synthesized_output["confidence"] = sorted_confidence[0].value
        
        return synthesized_output
    
    # Agent implementation stubs - in a real system these would call actual agent services
    
    def _medical_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Medical Agent for overall health assessment"""
        logger.info("Processing data with Medical Agent")
        # In a real system, this would call the actual Medical Agent service
        return {
            "confidence": ConfidenceLevel.HIGH.value,
            "recommendations": [
                {"type": "medical", "action": "regular_checkup", "priority": "medium"}
            ],
            "insights": [
                {"type": "health_status", "description": "Overall health indicators within normal range"}
            ],
            "key_findings": ["Blood pressure normal", "Heart rate normal"]
        }
    
    def _medical_reasoning_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Medical Reasoning Agent for detailed clinical analysis"""
        logger.info("Processing data with Medical Reasoning Agent")
        # Call the actual Medical Reasoning Agent
        return self.medical_reasoning_agent.process(user_data)
    
    def _nutrition_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Nutrition Agent for dietary analysis"""
        logger.info("Processing data with Nutrition Agent")
        # In a real system, this would call the actual Nutrition Agent service
        return {
            "confidence": ConfidenceLevel.MEDIUM.value,
            "recommendations": [
                {"type": "nutrition", "action": "increase_protein", "priority": "high"}
            ],
            "insights": [
                {"type": "diet_pattern", "description": "Protein intake below recommended levels"}
            ],
            "key_findings": ["Low protein intake", "Adequate hydration"]
        }
    
    def _sleep_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sleep Agent for sleep pattern analysis"""
        logger.info("Processing data with Sleep Agent")
        # In a real system, this would call the actual Sleep Agent service
        return {
            "confidence": ConfidenceLevel.HIGH.value,
            "recommendations": [
                {"type": "sleep", "action": "consistent_schedule", "priority": "high"}
            ],
            "insights": [
                {"type": "sleep_pattern", "description": "Irregular sleep schedule detected"}
            ],
            "key_findings": ["Inconsistent bedtime", "Average 6.5 hours of sleep"]
        }
    
    def _stress_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stress Agent for stress level analysis"""
        logger.info("Processing data with Stress Agent")
        # In a real system, this would call the actual Stress Agent service
        return {
            "confidence": ConfidenceLevel.MEDIUM.value,
            "recommendations": [
                {"type": "stress", "action": "meditation", "priority": "high"}
            ],
            "insights": [
                {"type": "stress_pattern", "description": "Elevated stress levels during weekdays"}
            ],
            "key_findings": ["High work-related stress", "Low stress during weekends"]
        }
    
    def _exercise_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Exercise Agent for physical activity analysis"""
        logger.info("Processing data with Exercise Agent")
        # In a real system, this would call the actual Exercise Agent service
        return {
            "confidence": ConfidenceLevel.HIGH.value,
            "recommendations": [
                {"type": "exercise", "action": "increase_cardio", "priority": "medium"}
            ],
            "insights": [
                {"type": "activity_pattern", "description": "Good strength training, limited cardiovascular exercise"}
            ],
            "key_findings": ["Regular strength training", "Insufficient cardio"]
        }
    
    def _personalization_agent(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Personalization Agent for customizing recommendations"""
        logger.info("Processing data with Personalization Agent")
        
        # Process data with the Personalization Agent
        return self.personalization_agent.process(user_data)
    
    def _critical_evaluation_agent(self, user_data: Dict[str, Any], agent_analyses: Dict[AgentType, Any], 
                                 flagged_issues: List[Dict[str, Any]]) -> Dict[AgentType, Any]:
        """
        Critical Evaluation Agent for resolving contradictions and low confidence analyses
        
        Args:
            user_data: Dictionary containing user health data
            agent_analyses: Dictionary mapping agent types to their analysis results
            flagged_issues: List of dictionaries containing flagged issues
            
        Returns:
            Dictionary mapping agent types to evaluation notes
        """
        logger.info("Processing with Critical Evaluation Agent")
        # In a real system, this would call the actual Critical Evaluation Agent service
        
        evaluation_results = {}
        
        for issue in flagged_issues:
            if issue["issue_type"] == "low_confidence":
                agent = issue["agent"]
                evaluation_results[agent] = {
                    "evaluation": "Reviewed low confidence analysis and confirmed findings",
                    "confidence_adjustment": "Confidence remains low due to insufficient data"
                }
            elif issue["issue_type"] == "contradiction":
                agents = issue["agent"]
                for agent in agents:
                    evaluation_results[agent] = {
                        "evaluation": "Resolved contradiction with other agent",
                        "resolution": "Prioritized medical recommendation over nutrition recommendation"
                    }
        
        return evaluation_results


# Example usage
if __name__ == "__main__":
    # Sample user data
    sample_user_data = {
        "user_id": "user123",
        "age": 35,
        "gender": "female",
        "height": 165,  # cm
        "weight": 65,   # kg
        "sleep_data": {
            "average_duration": 6.5,  # hours
            "quality": "medium",
            "bedtime_consistency": "low"
        },
        "nutrition_data": {
            "calories": 1800,
            "protein": 60,  # grams
            "carbs": 220,   # grams
            "fat": 65,      # grams
            "detailed_macros": True
        },
        "stress_data": {
            "level": 8,     # scale 1-10
            "sources": ["work", "financial"]
        },
        "exercise_data": {
            "strength_training": 3,  # times per week
            "cardio": 1,            # times per week
            "intensity": "medium"
        },
        "preferences": {
            "diet": "vegetarian",
            "exercise_time": "morning",
            "goals": ["weight_maintenance", "stress_reduction"]
        }
    }
    
    # Initialize and run the processor
    processor = MetaCognitiveProcessor()
    result = processor.process_health_data(sample_user_data)
    
    # Print the result
    print(json.dumps(result, indent=2))
