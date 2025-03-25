"""
Patient Management Module
------------------------
This module provides functions for managing patient records and scan data.
"""

import os
import sqlite3
import json
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Define database path
DATABASE_PATH = os.path.join('app', 'database', 'patients.db')

def get_db_connection():
    """
    Get a connection to the SQLite database.
    
    Returns:
        A connection object to the database
    """
    try:
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        # Connect to the database
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def init_db():
    """
    Initialize the database schema if it doesn't exist.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            address TEXT,
            medical_history TEXT,
            registration_date TEXT NOT NULL
        )
        ''')
        
        # Create scans table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            tumor_type TEXT,
            confidence REAL,
            scan_date TEXT NOT NULL,
            doctor_notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def add_patient(name, age, gender, contact=None, email=None, address=None, medical_history=None):
    """
    Add a new patient to the database.
    
    Args:
        name: Patient's full name
        age: Patient's age
        gender: Patient's gender
        contact: Patient's contact number (optional)
        email: Patient's email address (optional)
        address: Patient's address (optional)
        medical_history: Patient's medical history (optional)
        
    Returns:
        The ID of the newly added patient
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current date in YYYY-MM-DD format
        registration_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
        INSERT INTO patients (name, age, gender, contact, email, address, medical_history, registration_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, contact, email, address, medical_history, registration_date))
        
        # Get the ID of the newly inserted patient
        patient_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        logger.info(f"Added patient {name} with ID {patient_id}")
        return patient_id
    
    except Exception as e:
        logger.error(f"Error adding patient: {e}")
        return None

def get_patient(patient_id):
    """
    Get a patient's details by ID.
    
    Args:
        patient_id: The ID of the patient
        
    Returns:
        A dictionary containing the patient's details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        
        conn.close()
        
        if patient:
            # Convert SQLite Row to dict
            return dict(patient)
        else:
            return None
    
    except Exception as e:
        logger.error(f"Error getting patient {patient_id}: {e}")
        return None

def get_all_patients():
    """
    Get all patients from the database.
    
    Returns:
        A list of dictionaries containing patient details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients ORDER BY name')
        patients = cursor.fetchall()
        
        conn.close()
        
        # Convert SQLite Row objects to dictionaries
        return [dict(patient) for patient in patients]
    
    except Exception as e:
        logger.error(f"Error getting all patients: {e}")
        return []

def search_patients(query):
    """
    Search for patients by name, contact, or email.
    
    Args:
        query: The search query
        
    Returns:
        A list of dictionaries containing matching patient details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Use LIKE for case-insensitive search
        search_term = f"%{query}%"
        
        cursor.execute('''
        SELECT * FROM patients 
        WHERE name LIKE ? OR contact LIKE ? OR email LIKE ?
        ORDER BY name
        ''', (search_term, search_term, search_term))
        
        patients = cursor.fetchall()
        
        conn.close()
        
        # Convert SQLite Row objects to dictionaries
        return [dict(patient) for patient in patients]
    
    except Exception as e:
        logger.error(f"Error searching patients: {e}")
        return []

def add_scan(patient_id, image_path, tumor_type=None, confidence=None, doctor_notes=None):
    """
    Add a new scan for a patient.
    
    Args:
        patient_id: The ID of the patient
        image_path: Path to the scan image
        tumor_type: The predicted tumor type
        confidence: The confidence score of the prediction
        doctor_notes: Additional notes from the doctor
        
    Returns:
        The ID of the newly added scan
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current date in YYYY-MM-DD format
        scan_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
        INSERT INTO scans (patient_id, image_path, tumor_type, confidence, scan_date, doctor_notes)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, image_path, tumor_type, confidence, scan_date, doctor_notes))
        
        # Get the ID of the newly inserted scan
        scan_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        logger.info(f"Added scan for patient {patient_id} with scan ID {scan_id}")
        return scan_id
    
    except Exception as e:
        logger.error(f"Error adding scan: {e}")
        return None

def get_scan(scan_id):
    """
    Get a scan's details by ID.
    
    Args:
        scan_id: The ID of the scan
        
    Returns:
        A dictionary containing the scan's details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
        scan = cursor.fetchone()
        
        conn.close()
        
        if scan:
            # Convert SQLite Row to dict
            return dict(scan)
        else:
            return None
    
    except Exception as e:
        logger.error(f"Error getting scan {scan_id}: {e}")
        return None

def get_patient_scans(patient_id):
    """
    Get all scans for a specific patient.
    
    Args:
        patient_id: The ID of the patient
        
    Returns:
        A list of dictionaries containing scan details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM scans WHERE patient_id = ? ORDER BY scan_date DESC', (patient_id,))
        scans = cursor.fetchall()
        
        conn.close()
        
        # Convert SQLite Row objects to dictionaries
        return [dict(scan) for scan in scans]
    
    except Exception as e:
        logger.error(f"Error getting scans for patient {patient_id}: {e}")
        return []

def update_scan(scan_id, doctor_notes=None):
    """
    Update a scan's details.
    
    Args:
        scan_id: The ID of the scan
        doctor_notes: Updated doctor's notes
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE scans SET doctor_notes = ? WHERE id = ?', (doctor_notes, scan_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated scan {scan_id}")
        return True
    
    except Exception as e:
        logger.error(f"Error updating scan {scan_id}: {e}")
        return False 