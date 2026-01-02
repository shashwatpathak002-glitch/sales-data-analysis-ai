"""Database Module - SQLite user and data management"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Database:
    """
    SQLite database management for users and their sales data.
    """
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User data uploads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                data_json TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Forecasts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                data_id INTEGER NOT NULL,
                forecast_json TEXT NOT NULL,
                model_metrics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (data_id) REFERENCES user_data(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Register a new user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))
            
            conn.commit()
            conn.close()
            return True, "User registered successfully!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[int], str]:
        """Authenticate user and return user_id if successful."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                SELECT id FROM users WHERE username = ? AND password_hash = ?
            """, (username, password_hash))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return True, result[0], "Login successful!"
            else:
                return False, None, "Invalid username or password"
        except Exception as e:
            return False, None, f"Login error: {str(e)}"
    
    def save_user_data(self, user_id: int, filename: str, dataframe) -> Tuple[bool, str, Optional[int]]:
        """Save user's uploaded data to database."""
        try:
            data_json = dataframe.to_json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_data (user_id, filename, data_json)
                VALUES (?, ?, ?)
            """, (user_id, filename, data_json))
            
            data_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "Data saved successfully!", data_id
        except Exception as e:
            return False, f"Save error: {str(e)}", None
    
    def get_user_data(self, user_id: int) -> List[Dict]:
        """Get all uploaded data for a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, filename, upload_date FROM user_data
                WHERE user_id = ? ORDER BY upload_date DESC
            """, (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [{
                'id': r[0],
                'filename': r[1],
                'upload_date': r[2]
            } for r in results]
        except Exception as e:
            print(f"Error retrieving data: {str(e)}")
            return []
    
    def delete_user_data(self, user_id: int, data_id: int) -> bool:
        """Delete user's data record."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM user_data WHERE id = ? AND user_id = ?
            """, (data_id, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting data: {str(e)}")
            return False
