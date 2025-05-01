from flask import Flask, request, jsonify
from flask_cors import CORS
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import crud, models, schemas
from database import SessionLocal, engine, Base
from typing import List
import logging
import json
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()
DEFAULT_OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create tables
Base.metadata.create_all(bind=engine)

# Log configuration (without exposing full API key)
if DEFAULT_OPENAI_KEY:
    logger.info(f"Loaded API key from environment (length: {len(DEFAULT_OPENAI_KEY)}, prefix: {DEFAULT_OPENAI_KEY[:7]}...)")
else:
    logger.error("No OpenAI API key found in environment variables!")

# --- OpenAI Integration ---
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_openai_api(api_key: str, messages: list, model: str = "gpt-3.5-turbo") -> str:
    """Call OpenAI API with retry logic."""
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

# --- Routes ---
@app.route('/', methods=['GET'])
def read_root():
    return jsonify({"status": "healthy"}), 200

@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/chat-coach/', methods=['POST'])
def chat_coach():
    """Chat coach endpoint - now with live LLM integration"""
    try:
        # Basic request validation
        data = request.json
        if not data:
            return jsonify({"error": "Bad Request"}), 400

        # Check for required fields
        required = ["assessment", "prompt", "api_key", "llm_model"]
        if any(field not in data for field in required):
            return jsonify({"error": "Missing required fields"}), 400

        # Format messages for OpenAI
        system_message = (
            "You are an expert health coach. Analyze the user's health metrics "
            "and provide personalized, actionable advice."
        )
        user_message = (
            f"Here are my health metrics: {json.dumps(data['assessment'])}\n"
            f"{data['prompt']}"
        )
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user",   "content": user_message}
        ]

        try:
            answer = call_openai_api(
                api_key  = data['api_key'],
                messages = messages,
                model    = data['llm_model']
            )
            return jsonify({ "response": answer }), 200
        except Exception as e:
            logger.error(f"OpenAI API failed: {e}")
            # Fallback demo-stub on error
            return jsonify({
                "note": "OpenAI API error – falling back to demo response",
                "response": "Hello! Here are your next steps to improve your health..."
            }), 200

    except Exception as e:
        logger.error(f"Error in chat_coach: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
