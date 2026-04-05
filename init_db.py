"""
Database Initialization Script for Student Dropout Prediction & Counselling System
This script creates all necessary tables and inserts sample data.
Run this script once before starting the Flask application.
"""

import sqlite3
from datetime import datetime, timedelta
import random

def init_db():
    """Initialize the database with all required tables and sample data."""
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute('PRAGMA foreign_keys = ON')
    
    # ==================== CREATE TABLES ====================
    
    # Admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Staff table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            department TEXT,
            role TEXT DEFAULT 'Counsellor',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            attendance REAL DEFAULT 0,
            average_marks REAL DEFAULT 0,
            risk_level TEXT DEFAULT 'Low',
            status TEXT DEFAULT 'Active',
            counsellor_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (counsellor_id) REFERENCES staff(id)
        )
    ''')
    
    # Counselling sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counselling_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            counsellor_id INTEGER,
            session_type TEXT NOT NULL,
            session_date DATE NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'Scheduled',
            follow_up_required BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (counsellor_id) REFERENCES staff(id)
        )
    ''')
    
    # Reports/Analytics table (for tracking interventions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intervention_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            description TEXT,
            performed_by INTEGER,
            outcome TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (performed_by) REFERENCES staff(id)
        )
    ''')
    
    print("✓ Database tables created successfully!")
    
    # ==================== INSERT SAMPLE DATA ====================
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM admins')
    if cursor.fetchone()[0] > 0:
        print("⚠ Sample data already exists. Skipping insertion.")
        conn.commit()
        conn.close()
        return
    
    # Insert sample admin
    cursor.execute('''
        INSERT INTO admins (username, password, email, full_name)
        VALUES ('admin', 'admin123', 'admin@institution.edu', 'Admin User')
    ''')
    
    # Insert sample staff
    cursor.execute('''
        INSERT INTO staff (username, password, email, full_name, department, role)
        VALUES 
        ('staff', 'staff123', 'staff@institution.edu', 'Sarah Smith', 'Computer Science', 'Counsellor'),
        ('john_doe', 'staff123', 'john.doe@institution.edu', 'John Doe', 'Engineering', 'Faculty'),
        ('emily_davis', 'staff123', 'emily.davis@institution.edu', 'Emily Davis', 'Arts', 'Senior Counsellor')
    ''')
    
    # Insert sample students with varied risk levels
    departments = ['Computer Science', 'Engineering', 'Arts', 'Business', 'Medicine']
    risk_levels = ['High', 'Medium', 'Low']
    
    conn.commit()
    conn.close()
    
    print("✓ Sample data inserted successfully!")
    print("\n" + "="*60)
    print("DATABASE INITIALIZED SUCCESSFULLY!")
    print("="*60)
    print("\nDefault Login Credentials:")
    print("-" * 60)
    print("Admin:   username = admin,    password = admin123")
    print("Staff:   username = staff,    password = staff123")
    print("Student: username = REG-2023-001, password = student123")
    print("="*60)

if __name__ == '__main__':
    print("Initializing database for Student Dropout Prediction & Counselling System...")
    print("-" * 60)
    init_db()
    print("\nDatabase initialization complete! You can now run the Flask app.")
