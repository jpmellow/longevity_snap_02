"""
Database module for Longevity Snapshot App

This module handles data persistence using SQLite for storing user data,
health assessments, and tracking changes over time.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

class LongevityDatabase:
    """Database handler for Longevity Snapshot App"""
    
    def __init__(self, db_path: str = "longevity_snapshot.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.conn = self._create_connection()
        self._create_tables()
    
    def _create_connection(self) -> sqlite3.Connection:
        """Create a database connection"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Users table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                age INTEGER,
                gender TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            ''')
            
            # Assessments table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id TEXT PRIMARY KEY,
                user_id TEXT,
                timestamp TEXT,
                health_data TEXT,
                recommendations TEXT,
                insights TEXT,
                confidence TEXT,
                longevity_score INTEGER,
                motivation_driver TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            ''')
            
            # Health metrics table for tracking changes
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_metrics (
                metric_id TEXT PRIMARY KEY,
                user_id TEXT,
                timestamp TEXT,
                metric_type TEXT,
                metric_value REAL,
                metric_unit TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
            raise
    
    def add_user(self, user_data: Dict[str, Any]) -> str:
        """
        Add a new user to the database
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            user_id: The ID of the created user
        """
        try:
            cursor = self.conn.cursor()
            
            # Extract user data
            user_id = user_data.get("user_id")
            name = user_data.get("name", "")
            email = user_data.get("email", "")
            age = user_data.get("age", 0)
            gender = user_data.get("gender", "")
            
            # Set timestamps
            now = datetime.now().isoformat()
            
            # Check if user already exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update existing user
                cursor.execute('''
                UPDATE users
                SET name = ?, email = ?, age = ?, gender = ?, updated_at = ?
                WHERE user_id = ?
                ''', (name, email, age, gender, now, user_id))
            else:
                # Insert new user
                cursor.execute('''
                INSERT INTO users (user_id, name, email, age, gender, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, name, email, age, gender, now, now))
            
            self.conn.commit()
            return user_id
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            self.conn.rollback()
            raise
    
    def save_assessment(self, assessment_data: Dict[str, Any]) -> str:
        """
        Save a health assessment to the database
        
        Args:
            assessment_data: Dictionary containing assessment results
            
        Returns:
            assessment_id: The ID of the saved assessment
        """
        try:
            cursor = self.conn.cursor()
            
            # Extract assessment data
            assessment_id = assessment_data.get("assessment_id", f"assessment_{datetime.now().timestamp()}")
            user_id = assessment_data.get("user_id")
            timestamp = assessment_data.get("timestamp", datetime.now().isoformat())
            health_data = json.dumps(assessment_data.get("health_data", {}))
            recommendations = json.dumps(assessment_data.get("recommendations", []))
            insights = json.dumps(assessment_data.get("insights", []))
            confidence = assessment_data.get("confidence", "medium")
            longevity_score = assessment_data.get("longevity_score", 0)
            motivation_driver = assessment_data.get("motivation_driver", "unknown")
            
            # Insert assessment
            cursor.execute('''
            INSERT INTO assessments 
            (assessment_id, user_id, timestamp, health_data, recommendations, 
            insights, confidence, longevity_score, motivation_driver)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (assessment_id, user_id, timestamp, health_data, recommendations, 
                 insights, confidence, longevity_score, motivation_driver))
            
            self.conn.commit()
            return assessment_id
        except sqlite3.Error as e:
            print(f"Error saving assessment: {e}")
            self.conn.rollback()
            raise
    
    def track_metric(self, metric_data: Dict[str, Any]) -> str:
        """
        Track a health metric for a user
        
        Args:
            metric_data: Dictionary containing metric information
            
        Returns:
            metric_id: The ID of the tracked metric
        """
        try:
            cursor = self.conn.cursor()
            
            # Extract metric data
            metric_id = metric_data.get("metric_id", f"metric_{datetime.now().timestamp()}")
            user_id = metric_data.get("user_id")
            timestamp = metric_data.get("timestamp", datetime.now().isoformat())
            metric_type = metric_data.get("metric_type")
            metric_value = metric_data.get("metric_value")
            metric_unit = metric_data.get("metric_unit", "")
            
            # Insert metric
            cursor.execute('''
            INSERT INTO health_metrics 
            (metric_id, user_id, timestamp, metric_type, metric_value, metric_unit)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (metric_id, user_id, timestamp, metric_type, metric_value, metric_unit))
            
            self.conn.commit()
            return metric_id
        except sqlite3.Error as e:
            print(f"Error tracking metric: {e}")
            self.conn.rollback()
            raise
    
    def get_user_assessments(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all assessments for a user
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of assessment dictionaries
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
            SELECT * FROM assessments
            WHERE user_id = ?
            ORDER BY timestamp DESC
            ''', (user_id,))
            
            assessments = []
            for row in cursor.fetchall():
                assessment = {
                    "assessment_id": row[0],
                    "user_id": row[1],
                    "timestamp": row[2],
                    "health_data": json.loads(row[3]),
                    "recommendations": json.loads(row[4]),
                    "insights": json.loads(row[5]),
                    "confidence": row[6],
                    "longevity_score": row[7],
                    "motivation_driver": row[8]
                }
                assessments.append(assessment)
            
            return assessments
        except sqlite3.Error as e:
            print(f"Error getting user assessments: {e}")
            raise
    
    def get_metric_history(self, user_id: str, metric_type: str) -> List[Dict[str, Any]]:
        """
        Get history of a specific metric for a user
        
        Args:
            user_id: The ID of the user
            metric_type: The type of metric to retrieve
            
        Returns:
            List of metric dictionaries
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
            SELECT * FROM health_metrics
            WHERE user_id = ? AND metric_type = ?
            ORDER BY timestamp ASC
            ''', (user_id, metric_type))
            
            metrics = []
            for row in cursor.fetchall():
                metric = {
                    "metric_id": row[0],
                    "user_id": row[1],
                    "timestamp": row[2],
                    "metric_type": row[3],
                    "metric_value": row[4],
                    "metric_unit": row[5]
                }
                metrics.append(metric)
            
            return metrics
        except sqlite3.Error as e:
            print(f"Error getting metric history: {e}")
            raise
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
