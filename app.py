import streamlit as st
import pandas as pd
from PIL import Image
import sqlite3
from datetime import datetime, timedelta
import hashlib
import json
from dataclasses import dataclass
from typing import List, Optional, Dict
import plotly.express as px
import plotly.graph_objects as go
import secrets
import string

# ==================== CONFIG ====================
st.set_page_config(
    page_title="KIC Innovation Hub",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== INFO OF AUTHOR ====================
__author__ = "Alisher Beisembekov"
__version__ = "1.0.0"
__email__ = "alisherbeisembekov2002@gmail.com"
__copyright__ = "Copyright 2025, Alisher Beisembekov"
__linkedin__ = "https://linkedin.com/in/alisher-beisembekov"
__github__ = "https://github.com/damn_glitch"

# ==================== DATABASE ====================
class Database:
    def __init__(self, db_path="innovate_hub_ultimate.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Enhanced database schema with all features"""
        cursor = self.conn.cursor()

        try:
            # Enhanced users table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS users
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               email
                               TEXT
                               UNIQUE
                               NOT
                               NULL,
                               password_hash
                               TEXT
                               NOT
                               NULL,
                               name
                               TEXT
                               NOT
                               NULL,
                               user_type
                               TEXT
                               NOT
                               NULL,
                               organization
                               TEXT,
                               bio
                               TEXT,
                               location
                               TEXT,
                               profile_image
                               TEXT,
                               phone
                               TEXT,
                               linkedin_url
                               TEXT,
                               website_url
                               TEXT,
                               kic_balance
                               INTEGER
                               DEFAULT
                               1000,
                               total_projects_completed
                               INTEGER
                               DEFAULT
                               0,
                               reputation_score
                               INTEGER
                               DEFAULT
                               0,
                               is_verified
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               is_active
                               BOOLEAN
                               DEFAULT
                               TRUE,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )''')

            # Universities table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS universities
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               name
                               TEXT
                               NOT
                               NULL,
                               location
                               TEXT
                               NOT
                               NULL,
                               country
                               TEXT
                               DEFAULT
                               'UAE',
                               website
                               TEXT,
                               contact_email
                               TEXT,
                               contact_phone
                               TEXT,
                               description
                               TEXT,
                               established_year
                               INTEGER,
                               total_students
                               INTEGER
                               DEFAULT
                               0,
                               total_faculty
                               INTEGER
                               DEFAULT
                               0,
                               ranking_national
                               INTEGER,
                               is_verified
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )''')

            # Companies table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS companies
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               name
                               TEXT
                               NOT
                               NULL,
                               description
                               TEXT,
                               industry
                               TEXT,
                               size
                               TEXT,
                               location
                               TEXT,
                               website
                               TEXT,
                               logo_url
                               TEXT,
                               founded_year
                               INTEGER,
                               kic_balance
                               INTEGER
                               DEFAULT
                               5000,
                               total_projects_posted
                               INTEGER
                               DEFAULT
                               0,
                               rating
                               REAL
                               DEFAULT
                               0,
                               is_verified
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )''')

            # Enhanced labs table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS labs
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               name
                               TEXT
                               NOT
                               NULL,
                               university_id
                               INTEGER,
                               location
                               TEXT
                               NOT
                               NULL,
                               specialty
                               TEXT
                               NOT
                               NULL,
                               available_from
                               DATE,
                               equipment
                               TEXT,
                               description
                               TEXT,
                               contact
                               TEXT,
                               price_per_day
                               INTEGER,
                               kic_price_per_day
                               INTEGER,
                               rating
                               REAL
                               DEFAULT
                               0,
                               image_url
                               TEXT,
                               capacity
                               INTEGER,
                               amenities
                               TEXT,
                               total_bookings
                               INTEGER
                               DEFAULT
                               0,
                               is_featured
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               access_requirements
                               TEXT,
                               safety_protocols
                               TEXT,
                               FOREIGN
                               KEY
                           (
                               university_id
                           ) REFERENCES universities
                           (
                               id
                           )
                               )''')

            # Lab access credentials table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS lab_access
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               lab_id
                               INTEGER
                               NOT
                               NULL,
                               user_id
                               INTEGER
                               NOT
                               NULL,
                               access_level
                               TEXT
                               DEFAULT
                               'basic',
                               username
                               TEXT
                               NOT
                               NULL,
                               password_hash
                               TEXT
                               NOT
                               NULL,
                               valid_from
                               DATE,
                               valid_until
                               DATE,
                               is_active
                               BOOLEAN
                               DEFAULT
                               TRUE,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               lab_id
                           ) REFERENCES labs
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Enhanced talents table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS talents
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER,
                               title
                               TEXT
                               NOT
                               NULL,
                               location
                               TEXT
                               NOT
                               NULL,
                               experience
                               TEXT,
                               education
                               TEXT,
                               skills
                               TEXT,
                               availability
                               TEXT,
                               bio
                               TEXT,
                               hourly_rate
                               INTEGER,
                               kic_hourly_rate
                               INTEGER,
                               portfolio_url
                               TEXT,
                               linkedin_url
                               TEXT,
                               rating
                               REAL
                               DEFAULT
                               0,
                               total_projects
                               INTEGER
                               DEFAULT
                               0,
                               total_earnings
                               INTEGER
                               DEFAULT
                               0,
                               specializations
                               TEXT,
                               certifications
                               TEXT,
                               languages
                               TEXT,
                               is_featured
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Enhanced projects table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS projects
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               title
                               TEXT
                               NOT
                               NULL,
                               organization
                               TEXT
                               NOT
                               NULL,
                               company_id
                               INTEGER,
                               location
                               TEXT
                               NOT
                               NULL,
                               deadline
                               DATE,
                               posted
                               DATE
                               DEFAULT
                               CURRENT_DATE,
                               description
                               TEXT,
                               requirements
                               TEXT,
                               tags
                               TEXT,
                               budget_min
                               INTEGER,
                               budget_max
                               INTEGER,
                               kic_budget_min
                               INTEGER,
                               kic_budget_max
                               INTEGER,
                               status
                               TEXT
                               DEFAULT
                               'Active',
                               contact
                               TEXT,
                               views
                               INTEGER
                               DEFAULT
                               0,
                               applications
                               INTEGER
                               DEFAULT
                               0,
                               project_type
                               TEXT
                               DEFAULT
                               'Research',
                               urgency
                               TEXT
                               DEFAULT
                               'Medium',
                               remote_possible
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               created_by
                               INTEGER,
                               FOREIGN
                               KEY
                           (
                               company_id
                           ) REFERENCES companies
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               created_by
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # User projects table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS user_projects
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER
                               NOT
                               NULL,
                               project_id
                               INTEGER
                               NOT
                               NULL,
                               role
                               TEXT
                               DEFAULT
                               'participant',
                               status
                               TEXT
                               DEFAULT
                               'active',
                               joined_date
                               DATE
                               DEFAULT
                               CURRENT_DATE,
                               completion_date
                               DATE,
                               contribution_description
                               TEXT,
                               rating_received
                               REAL,
                               payment_received
                               INTEGER,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               project_id
                           ) REFERENCES projects
                           (
                               id
                           )
                               )''')

            # Project applications table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS project_applications
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               project_id
                               INTEGER
                               NOT
                               NULL,
                               user_id
                               INTEGER
                               NOT
                               NULL,
                               application_text
                               TEXT,
                               proposed_rate
                               INTEGER,
                               proposed_kic_rate
                               INTEGER,
                               status
                               TEXT
                               DEFAULT
                               'pending',
                               applied_date
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               response_date
                               TIMESTAMP,
                               response_message
                               TEXT,
                               FOREIGN
                               KEY
                           (
                               project_id
                           ) REFERENCES projects
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Messages table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS messages
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               sender_id
                               INTEGER
                               NOT
                               NULL,
                               receiver_id
                               INTEGER
                               NOT
                               NULL,
                               message
                               TEXT
                               NOT
                               NULL,
                               message_type
                               TEXT
                               DEFAULT
                               'text',
                               is_read
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               sender_id
                           ) REFERENCES users
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               receiver_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Connections table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS connections
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               requester_id
                               INTEGER
                               NOT
                               NULL,
                               addressee_id
                               INTEGER
                               NOT
                               NULL,
                               status
                               TEXT
                               DEFAULT
                               'pending',
                               message
                               TEXT,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               accepted_at
                               TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               requester_id
                           ) REFERENCES users
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               addressee_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Activities table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS activities
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER
                               NOT
                               NULL,
                               activity_type
                               TEXT
                               NOT
                               NULL,
                               title
                               TEXT
                               NOT
                               NULL,
                               description
                               TEXT,
                               related_id
                               INTEGER,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # KIC transactions table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS kic_transactions
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER
                               NOT
                               NULL,
                               transaction_type
                               TEXT
                               NOT
                               NULL,
                               amount
                               INTEGER
                               NOT
                               NULL,
                               description
                               TEXT,
                               related_id
                               INTEGER,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Bookings table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS bookings
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER,
                               lab_id
                               INTEGER,
                               start_date
                               DATE,
                               end_date
                               DATE,
                               purpose
                               TEXT,
                               status
                               TEXT
                               DEFAULT
                               'Pending',
                               total_cost
                               INTEGER,
                               kic_cost
                               INTEGER,
                               payment_method
                               TEXT
                               DEFAULT
                               'AED',
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               lab_id
                           ) REFERENCES labs
                           (
                               id
                           )
                               )''')

            # Reviews table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS reviews
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER,
                               item_type
                               TEXT,
                               item_id
                               INTEGER,
                               rating
                               INTEGER,
                               comment
                               TEXT,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            # Notifications table
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS notifications
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               user_id
                               INTEGER,
                               title
                               TEXT,
                               message
                               TEXT,
                               type
                               TEXT,
                               is_read
                               BOOLEAN
                               DEFAULT
                               FALSE,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP,
                               FOREIGN
                               KEY
                           (
                               user_id
                           ) REFERENCES users
                           (
                               id
                           )
                               )''')

            self.conn.commit()
            print("Database tables created successfully")

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            st.error(f"Database error: {e}")

    def seed_comprehensive_data(self):
        """Seed comprehensive data for all features"""
        cursor = self.conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            return

        try:
            # Seed universities
            universities = [
                ("United Arab Emirates University", "Al Ain", "UAE", "https://uaeu.ac.ae",
                 "info@uaeu.ac.ae", "+971-3-713-5555",
                 "The oldest university in the UAE, established in 1976", 1976, 14000, 700, 1, True),
                ("American University of Sharjah", "Sharjah", "UAE", "https://aus.edu",
                 "info@aus.edu", "+971-6-515-5555",
                 "Leading American-style university in the Middle East", 1997, 6000, 400, 2, True),
                ("Khalifa University", "Abu Dhabi", "UAE", "https://ku.ac.ae",
                 "info@ku.ac.ae", "+971-2-312-3456",
                 "Research-intensive university focusing on science and engineering", 2007, 4000, 500, 3, True),
                ("NYU Abu Dhabi", "Abu Dhabi", "UAE", "https://nyuad.nyu.edu",
                 "nyuad.info@nyu.edu", "+971-2-628-4000",
                 "Liberal arts and science college bringing together NYU and Abu Dhabi", 2010, 2000, 300, 4, True),
                ("Masdar Institute", "Abu Dhabi", "UAE", "https://masdar.ac.ae",
                 "info@masdar.ac.ae", "+971-2-810-9999",
                 "Graduate-level research university focused on alternative energy", 2007, 800, 150, 5, True)
            ]

            for uni in universities:
                cursor.execute('''
                               INSERT INTO universities (name, location, country, website, contact_email,
                                                         contact_phone, description, established_year, total_students,
                                                         total_faculty, ranking_national, is_verified)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', uni)

            # Seed companies
            companies = [
                ("Dubai Future Foundation", "Leading government organization driving future innovation in UAE",
                 "Government", "Large", "Dubai", "https://dubaifuture.gov.ae", None, 2016, 50000, 15, 4.8, True),
                ("Mubadala Investment Company", "Strategic investment company creating lasting value",
                 "Investment", "Large", "Abu Dhabi", "https://mubadala.com", None, 2002, 75000, 22, 4.9, True),
                ("ADNOC", "Leading energy and petrochemicals company",
                 "Energy", "Large", "Abu Dhabi", "https://adnoc.ae", None, 1971, 60000, 18, 4.7, True),
                ("Noon", "E-commerce platform and technology company",
                 "Technology", "Large", "Dubai", "https://noon.com", None, 2016, 40000, 12, 4.6, True),
                ("Emaar Properties", "Leading real estate development company",
                 "Real Estate", "Large", "Dubai", "https://emaar.com", None, 1997, 45000, 20, 4.5, True),
                ("Careem", "Revolutionary ride-hailing and delivery platform",
                 "Technology", "Medium", "Dubai", "https://careem.com", None, 2012, 35000, 10, 4.7, True),
                ("Etisalat", "Leading telecommunications provider",
                 "Telecommunications", "Large", "Abu Dhabi", "https://etisalat.ae", None, 1976, 55000, 25, 4.6, True)
            ]

            cursor.executemany('''
                               INSERT INTO companies (name, description, industry, size, location, website,
                                                      logo_url, founded_year, kic_balance, total_projects_posted,
                                                      rating, is_verified)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', companies)

            # Seed users
            users = [
                ("ahmed.mansouri@example.com", hashlib.sha256("password123".encode()).hexdigest(),
                 "Ahmed Al Mansouri", "talent", "Tech Innovations LLC",
                 "Robotics Engineer specializing in AI-driven automation systems. 5+ years experience in industrial robotics.",
                 "Abu Dhabi", None, "+971501234567", "https://linkedin.com/in/ahmed-mansouri",
                 "https://robotics-portfolio.ae", 1500, 15, 450, True, True),
                ("fatima.zaabi@example.com", hashlib.sha256("password123".encode()).hexdigest(),
                 "Dr. Fatima Al Zaabi", "talent", "Analytics Solutions",
                 "Data Scientist and Machine Learning expert with focus on healthcare applications.",
                 "Dubai", None, "+971507654321", "https://linkedin.com/in/fatima-zaabi",
                 "https://ml-portfolio.ae", 2200, 25, 780, True, True),
                ("sara.hassan@example.com", hashlib.sha256("password123".encode()).hexdigest(),
                 "Sara Hassan", "company", "Dubai Future Foundation",
                 "Innovation Manager at Dubai Future Foundation, leading emerging technology initiatives.",
                 "Dubai", None, "+971509876543", "https://linkedin.com/in/sara-hassan", None,
                 5000, 8, 320, True, True),
                ("mohammed.rashid@uaeu.ac.ae", hashlib.sha256("password123".encode()).hexdigest(),
                 "Dr. Mohammed Al Rashid", "researcher", "UAE University",
                 "Professor of Computer Science specializing in AI and Machine Learning research.",
                 "Al Ain", None, "+971501112233", "https://linkedin.com/in/mohammed-rashid",
                 "https://uaeu.ac.ae/dr-rashid", 3000, 20, 650, True, True),
                ("layla.ibrahim@example.com", hashlib.sha256("password123".encode()).hexdigest(),
                 "Layla Ibrahim", "talent", "Biotech Solutions",
                 "Biotechnology researcher with expertise in genomics and pharmaceutical development.",
                 "Sharjah", None, "+971502223344", "https://linkedin.com/in/layla-ibrahim", None,
                 1800, 12, 380, True, True)
            ]

            for user in users:
                cursor.execute('''
                               INSERT INTO users (email, password_hash, name, user_type, organization, bio, location,
                                                  profile_image, phone, linkedin_url, website_url, kic_balance,
                                                  total_projects_completed, reputation_score, is_verified, is_active)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', user)

            # Seed talents
            talents_data = [
                (1, "Senior Robotics Engineer", "Abu Dhabi", "5-10 years", "MSc Robotics Engineering",
                 "Python,C++,ROS,Machine Learning,Computer Vision,MATLAB", "Full-time",
                 "Expert in autonomous systems and industrial automation", 200, 100,
                 "https://portfolio.ae/ahmed", "https://linkedin.com/in/ahmed", 4.8, 15, 45000,
                 "Industrial Automation,Autonomous Systems", "ROS Certified,AWS ML Certified",
                 "English,Arabic", True),
                (2, "Lead Data Scientist", "Dubai", "10+ years", "PhD Computer Science",
                 "Python,R,TensorFlow,PyTorch,SQL,Spark,Tableau", "Full-time",
                 "Specializing in healthcare AI and predictive analytics", 250, 125,
                 "https://portfolio.ae/fatima", "https://linkedin.com/in/fatima", 4.9, 25, 72000,
                 "Healthcare AI,Predictive Analytics", "Google ML Engineer,AWS Data Analytics",
                 "English,Arabic,French", True),
                (5, "Biotechnology Research Consultant", "Sharjah", "5-10 years", "PhD Biotechnology",
                 "Gene Sequencing,CRISPR,Cell Culture,Bioinformatics,Python", "Part-time",
                 "Expert in genomics and pharmaceutical research", 180, 90,
                 None, "https://linkedin.com/in/layla", 4.7, 12, 28000,
                 "Genomics,Drug Discovery", "Certified Clinical Research", "English,Arabic", False)
            ]

            cursor.executemany('''
                               INSERT INTO talents (user_id, title, location, experience, education, skills,
                                                    availability, bio, hourly_rate, kic_hourly_rate, portfolio_url,
                                                    linkedin_url, rating, total_projects, total_earnings,
                                                    specializations, certifications, languages, is_featured)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', talents_data)

            # Seed labs
            labs = [
                ("AI & Machine Learning Lab", 1, "Al Ain", "Artificial Intelligence",
                 "2024-03-01", "GPU Clusters,Python Environment,TensorFlow,PyTorch,CUDA Workstations",
                 "State-of-the-art AI research facility with latest GPU clusters", "ai.lab@uaeu.ac.ae",
                 800, 400, 4.8, None, 20, "High-speed Internet,Coffee Station,Whiteboards,24/7 Access",
                 45, True, "PhD or Masters in AI/ML required", "Safety briefing mandatory"),
                ("Robotics Engineering Lab", 2, "Sharjah", "Robotics",
                 "2024-03-01", "Industrial Robots,3D Printers,Sensors,Actuators,Motion Capture System",
                 "Comprehensive robotics research and development facility", "robotics@aus.edu",
                 1200, 600, 4.7, None, 15, "Tool Workshop,Testing Arena,Storage,VR Equipment",
                 38, True, "Engineering background required", "Protective equipment mandatory"),
                ("Biotechnology Research Lab", 3, "Abu Dhabi", "Biotechnology",
                 "2024-03-01", "PCR Machines,Microscopes,Centrifuges,Incubators,Flow Cytometer",
                 "Advanced biotechnology facility for cutting-edge research", "biolab@ku.ac.ae",
                 1500, 750, 4.9, None, 12, "Clean Room,Chemical Storage,Emergency Shower,Fume Hoods",
                 52, True, "Biology/Chemistry degree required", "Biosafety level 2 protocols"),
                ("Nanotechnology Lab", 4, "Abu Dhabi", "Nanotechnology",
                 "2024-03-01", "Electron Microscope,AFM,Cleanroom,Lithography Equipment",
                 "Advanced nanoscale research and fabrication facility", "nanolab@nyuad.nyu.edu",
                 2000, 1000, 4.9, None, 8, "Cleanroom,Gas Storage,Chemical Storage",
                 28, True, "Nanotechnology training required", "Cleanroom protocols mandatory"),
                ("Renewable Energy Lab", 5, "Abu Dhabi", "Energy",
                 "2024-03-01", "Solar Panels,Wind Turbines,Battery Storage,Power Analyzers",
                 "Renewable energy testing and development facility", "energy@masdar.ac.ae",
                 1000, 500, 4.7, None, 25, "Outdoor Testing Area,Workshop,Conference Room",
                 35, True, "Energy engineering background", "Electrical safety training required")
            ]

            for lab in labs:
                cursor.execute('''
                               INSERT INTO labs (name, university_id, location, specialty, available_from, equipment,
                                                 description, contact, price_per_day, kic_price_per_day, rating,
                                                 image_url, capacity, amenities, total_bookings, is_featured,
                                                 access_requirements, safety_protocols)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', lab)

            # Seed projects
            projects = [
                ("AI-Powered Smart City Infrastructure", "Dubai Future Foundation", 1, "Dubai",
                 "2024-08-15", "2024-02-01",
                 "Develop AI systems for smart traffic management, energy optimization, and citizen services integration.",
                 "AI/ML expertise, smart city experience, IoT knowledge, Arabic language preferred",
                 "AI,Smart City,IoT,Machine Learning,Arabic", 80000, 120000, 4000, 6000, "Active",
                 "projects@dubaifuture.gov.ae", 234, 18, "Innovation", "High", True, 3),
                ("Blockchain Supply Chain Transparency", "Mubadala Investment Company", 2, "Abu Dhabi",
                 "2024-07-30", "2024-02-05",
                 "Create blockchain solution for supply chain transparency in healthcare and pharmaceuticals.",
                 "Blockchain development, smart contracts, healthcare domain knowledge",
                 "Blockchain,Healthcare,Supply Chain,Smart Contracts", 60000, 90000, 3000, 4500, "Active",
                 "blockchain@mubadala.ae", 156, 12, "Research", "Medium", False, 3),
                ("Renewable Energy Grid Optimization", "ADNOC", 3, "Abu Dhabi",
                 "2024-09-01", "2024-02-10",
                 "Optimize energy distribution using AI and IoT sensors for renewable energy integration.",
                 "Energy systems, AI/ML, IoT, electrical engineering background",
                 "Energy,AI,IoT,Sustainability,Grid Systems", 100000, 150000, 5000, 7500, "Active",
                 "energy@adnoc.ae", 189, 15, "Innovation", "High", True, 3),
                ("E-commerce Personalization Engine", "Noon", 4, "Dubai",
                 "2024-06-30", "2024-02-12",
                 "Build advanced ML models for personalized shopping experiences and recommendations.",
                 "Machine Learning, recommendation systems, e-commerce experience",
                 "ML,E-commerce,Python,Recommendation Systems", 70000, 100000, 3500, 5000, "Active",
                 "tech@noon.com", 203, 22, "Development", "Medium", True, 3),
                ("Smart Building Management System", "Emaar Properties", 5, "Dubai",
                 "2024-08-01", "2024-02-15",
                 "Develop IoT-based building management system for energy efficiency and tenant comfort.",
                 "IoT development, building automation, energy management",
                 "IoT,Smart Buildings,Energy,Automation", 85000, 125000, 4250, 6250, "Active",
                 "innovation@emaar.com", 145, 10, "Development", "Medium", False, 3)
            ]

            cursor.executemany('''
                               INSERT INTO projects (title, organization, company_id, location, deadline, posted,
                                                     description, requirements, tags, budget_min, budget_max,
                                                     kic_budget_min, kic_budget_max, status, contact, views,
                                                     applications, project_type, urgency, remote_possible, created_by)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', projects)

            # Seed user projects
            user_projects = [
                (1, 1, "lead_engineer", "active", "2024-02-01", None,
                 "Leading the robotics and automation team", None, None),
                (2, 2, "data_scientist", "active", "2024-02-05", None,
                 "Developing predictive models for supply chain", None, None),
                (1, 3, "consultant", "completed", "2024-01-15", "2024-02-28",
                 "Consulted on industrial automation solutions", 4.8, 4000),
                (2, 4, "ml_engineer", "active", "2024-02-12", None,
                 "Building recommendation algorithms", None, None),
                (5, 2, "researcher", "active", "2024-02-08", None,
                 "Researching blockchain applications in pharma", None, None)
            ]

            cursor.executemany('''
                               INSERT INTO user_projects (user_id, project_id, role, status, joined_date,
                                                          completion_date, contribution_description, rating_received,
                                                          payment_received)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', user_projects)

            # Seed connections
            connections = [
                (1, 2, "accepted", "Would love to connect and discuss AI projects",
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                (1, 4, "accepted", "Great to connect with fellow researchers",
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                (2, 5, "accepted", "Looking forward to collaborating",
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                (3, 1, "pending", "Would like to discuss potential projects",
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None),
                (4, 5, "accepted", "Fellow researcher in biotech",
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ]

            cursor.executemany('''
                               INSERT INTO connections (requester_id, addressee_id, status, message, created_at, accepted_at)
                               VALUES (?, ?, ?, ?, ?, ?)
                               ''', connections)

            # Seed messages
            messages = [
                (1, 2, "Hi Fatima! I saw your work on healthcare AI. Would love to discuss potential collaboration.",
                 "text", False),
                (2, 1, "Hi Ahmed! Thanks for reaching out. I'd be happy to discuss. When are you available?", "text",
                 True),
                (1, 2, "I'm free this Thursday afternoon or Friday morning. What works for you?", "text", False),
                (2, 1, "Thursday afternoon works great! Let's meet at 3 PM?", "text", True),
                (3, 1, "Ahmed, we have an exciting robotics project coming up. Are you interested?", "text", False)
            ]

            cursor.executemany('''
                               INSERT INTO messages (sender_id, receiver_id, message, message_type, is_read)
                               VALUES (?, ?, ?, ?, ?)
                               ''', messages)

            # Seed activities
            activities = [
                (1, "project_completed", "Completed Robotics Automation Project",
                 "Successfully delivered industrial automation solution for manufacturing company", 3),
                (2, "skill_certified", "Earned AI/ML Certification",
                 "Completed advanced certification in Machine Learning from Stanford Online", None),
                (1, "connection_made", "Connected with Dr. Fatima Al Zaabi",
                 "New professional connection in Data Science field", 2),
                (2, "project_started", "Started Healthcare Analytics Project",
                 "Beginning new project on predictive analytics for patient outcomes", 2),
                (4, "university_project", "Published Research Paper",
                 "Co-authored paper on AI applications in smart cities", None),
                (5, "lab_booking", "Booked Biotechnology Lab",
                 "Reserved lab for genomics research project", 3)
            ]

            cursor.executemany('''
                               INSERT INTO activities (user_id, activity_type, title, description, related_id)
                               VALUES (?, ?, ?, ?, ?)
                               ''', activities)

            # Seed KIC transactions
            kic_transactions = [
                (1, "project_payment", 4000, "Payment for completed robotics project", 3),
                (2, "lab_booking", -750, "Paid for AI lab booking using KIC", 1),
                (1, "bonus", 500, "Performance bonus for high-rated project delivery", None),
                (2, "talent_fee", 1200, "Received payment for consulting work", 2),
                (4, "research_grant", 2000, "Research grant for smart city project", 1),
                (5, "lab_booking", -500, "Biotech lab booking payment", 3)
            ]

            cursor.executemany('''
                               INSERT INTO kic_transactions (user_id, transaction_type, amount, description, related_id)
                               VALUES (?, ?, ?, ?, ?)
                               ''', kic_transactions)

            # Seed project applications
            applications = [
                (1, 1,
                 "I have extensive experience in robotics and AI integration. My recent project involved developing autonomous systems for industrial automation. I can bring valuable expertise to your smart city initiative.",
                 100000, 5000, "pending", None, None),
                (1, 2,
                 "With my background in IoT and blockchain, I can contribute to building secure and transparent supply chain solutions.",
                 85000, 4250, "accepted", datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 "Great experience! Welcome to the team."),
                (2, 4,
                 "As a ML expert specializing in recommendation systems, I have built similar solutions for e-commerce platforms.",
                 95000, 4750, "pending", None, None)
            ]

            for app in applications:
                cursor.execute('''
                               INSERT INTO project_applications (project_id, user_id, application_text,
                                                                 proposed_rate, proposed_kic_rate, status,
                                                                 response_date, response_message)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                               ''', app)

            # Seed bookings
            bookings = [
                (1, 1, "2024-03-15", "2024-03-17", "Testing AI models for robotics project",
                 "Confirmed", 2400, 1200, "KIC"),
                (2, 1, "2024-03-20", "2024-03-22", "Machine learning experiments",
                 "Pending", 2400, 1200, "AED"),
                (5, 3, "2024-03-25", "2024-03-30", "Genomics research project",
                 "Confirmed", 7500, 3750, "KIC")
            ]

            cursor.executemany('''
                               INSERT INTO bookings (user_id, lab_id, start_date, end_date, purpose,
                                                     status, total_cost, kic_cost, payment_method)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', bookings)

            # Seed notifications
            notifications = [
                (1, "New Connection Request", "Sara Hassan wants to connect with you", "connection", False),
                (2, "Project Application Update", "Your application for 'Blockchain Supply Chain' was accepted!",
                 "application", True),
                (1, "Lab Booking Confirmed", "Your booking for AI Lab on March 15-17 is confirmed", "booking", True),
                (2, "New Message", "You have a new message from Ahmed Al Mansouri", "message", False),
                (4, "Research Grant Approved", "Your research grant of 2000 KIC has been approved", "grant", True)
            ]

            cursor.executemany('''
                               INSERT INTO notifications (user_id, title, message, type, is_read)
                               VALUES (?, ?, ?, ?, ?)
                               ''', notifications)

            self.conn.commit()
            print("Comprehensive sample data seeded successfully")

        except sqlite3.Error as e:
            print(f"Error seeding data: {e}")
            self.conn.rollback()

    def reset_database(self):
        """Reset database completely"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

            self.conn.commit()
            print("Database reset successfully")
            self.create_tables()

        except sqlite3.Error as e:
            print(f"Error resetting database: {e}")


# ==================== ENHANCED STYLES ====================
def load_ultimate_css():
    st.markdown("""
    <style>
        /* Modern light theme with LinkedIn-inspired design */
        .main {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1e293b;
        }

        /* Enhanced gradient text */
        .gradient-text {
            background: linear-gradient(-45deg, #0077b5, #00a0dc, #0073e6, #005582);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Modern card design */
        .modern-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            border: 1px solid rgba(0, 119, 181, 0.1);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px -1px rgba(0, 119, 181, 0.1), 0 2px 4px -1px rgba(0, 119, 181, 0.06);
            backdrop-filter: blur(8px);
        }

        .modern-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 119, 181, 0.15), 0 10px 10px -5px rgba(0, 119, 181, 0.04);
            border-color: rgba(0, 119, 181, 0.2);
        }

        /* Premium navigation bar */
        .nav-container {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 119, 181, 0.1);
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 6px -1px rgba(0, 119, 181, 0.05);
        }

        /* Profile card styling */
        .profile-card {
            background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
            color: white;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }

        .profile-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 0.8; }
        }

        .profile-avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            margin: 0 auto 1rem auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: bold;
            position: relative;
            z-index: 1;
            border: 3px solid rgba(255, 255, 255, 0.3);
        }

        /* KIC Balance styling */
        .kic-balance {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 24px;
            font-weight: bold;
            display: inline-block;
            box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.3);
        }

        /* Message bubble styling */
        .message-bubble {
            border-radius: 18px;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            max-width: 70%;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message-bubble.sent {
            background: linear-gradient(135deg, #0077b5 0%, #005582 100%);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }

        .message-bubble.received {
            background: #f1f5f9;
            color: #1e293b;
            border-bottom-left-radius: 4px;
        }

        /* Activity feed styling */
        .activity-item {
            background: white;
            border-left: 4px solid transparent;
            border-image: linear-gradient(to bottom, #0077b5, #00a0dc) 1;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 4px rgba(0, 119, 181, 0.1);
            transition: all 0.2s ease;
        }

        .activity-item:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 8px rgba(0, 119, 181, 0.15);
        }

        /* Status badges */
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin: 0.2rem;
            transition: all 0.2s ease;
        }

        .status-online {
            background: rgba(34, 197, 94, 0.1);
            color: #16a34a;
            border: 1px solid #16a34a;
        }

        .status-verified {
            background: rgba(59, 130, 246, 0.1);
            color: #2563eb;
            border: 1px solid #2563eb;
        }

        .status-featured {
            background: rgba(251, 191, 36, 0.1);
            color: #d97706;
            border: 1px solid #d97706;
        }

        /* Professional skill tags */
        .skill-tag {
            background: rgba(0, 119, 181, 0.08);
            color: #0077b5;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            margin: 0.2rem;
            display: inline-block;
            border: 1px solid rgba(0, 119, 181, 0.2);
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .skill-tag:hover {
            background: rgba(0, 119, 181, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 119, 181, 0.2);
        }

        /* Enhanced metrics */
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(0, 119, 181, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #0077b5, #00a0dc);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .metric-card:hover::before {
            transform: scaleX(1);
        }

        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0, 119, 181, 0.1);
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }

        /* Chat interface */
        .chat-container {
            height: 500px;
            overflow-y: auto;
            border: 1px solid rgba(0, 119, 181, 0.1);
            border-radius: 12px;
            padding: 1rem;
            background: linear-gradient(to bottom, #f8fafc, #ffffff);
        }

        /* Project cards */
        .project-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(0, 119, 181, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .project-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--urgency-color, #0077b5), transparent);
            opacity: 0.7;
        }

        /* Project urgency indicators */
        .urgency-high {
            color: #dc2626;
            font-weight: bold;
            --urgency-color: #dc2626;
        }

        .urgency-medium {
            color: #d97706;
            font-weight: bold;
            --urgency-color: #d97706;
        }

        .urgency-low {
            color: #16a34a;
            font-weight: bold;
            --urgency-color: #16a34a;
        }

        /* Professional buttons */
        .professional-btn {
            background: linear-gradient(135deg, #0077b5 0%, #005582 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            display: inline-block;
            position: relative;
            overflow: hidden;
        }

        .professional-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .professional-btn:hover::before {
            width: 300px;
            height: 300px;
        }

        .professional-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 119, 181, 0.3);
        }

        /* Lab cards */
        .lab-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(0, 119, 181, 0.1);
            position: relative;
            transition: all 0.3s ease;
        }

        .lab-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 119, 181, 0.15);
        }

        /* Access credentials card */
        .credentials-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            font-family: 'Monaco', 'Consolas', monospace;
            position: relative;
            overflow: hidden;
        }

        .credentials-card::before {
            content: '🔐';
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 3rem;
            opacity: 0.1;
        }

        /* Enhanced form styling */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 1px solid rgba(0, 119, 181, 0.2);
            transition: all 0.2s ease;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #0077b5;
            box-shadow: 0 0 0 3px rgba(0, 119, 181, 0.1);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: rgba(255, 255, 255, 0.5);
            padding: 0.5rem;
            border-radius: 12px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
            border-radius: 5px;
            transition: all 0.2s ease;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #005582 0%, #0077b5 100%);
        }

        /* Notification badge */
        .notification-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #dc2626;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: bold;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }

        /* Success animation */
        @keyframes successPulse {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }

        .success-animation {
            animation: successPulse 0.5s ease-out;
        }
    </style>
    """, unsafe_allow_html=True)


# ==================== AUTHENTICATION & MANAGERS ====================
class AuthManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def login(email: str, password: str, db: Database):
        cursor = db.conn.cursor()
        try:
            cursor.execute("""
                           SELECT *
                           FROM users
                           WHERE email = ?
                             AND password_hash = ?
                             AND is_active = TRUE
                           """, (email, AuthManager.hash_password(password)))

            user = cursor.fetchone()
            if user:
                return dict(user)
            return None
        except sqlite3.Error as e:
            st.error(f"Login error: {e}")
            return None

    @staticmethod
    def register(email: str, password: str, name: str, user_type: str,
                 organization: str, location: str, phone: str, db: Database) -> bool:
        try:
            cursor = db.conn.cursor()
            cursor.execute("""
                           INSERT INTO users (email, password_hash, name, user_type,
                                              organization, location, phone, kic_balance)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                           """, (email, AuthManager.hash_password(password),
                                 name, user_type, organization, location, phone, 1000))
            db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            st.error(f"Registration error: {e}")
            return False


class SocialManager:
    @staticmethod
    def send_connection_request(requester_id: int, addressee_id: int, message: str, db: Database):
        cursor = db.conn.cursor()
        cursor.execute("""
                       INSERT INTO connections (requester_id, addressee_id, message)
                       VALUES (?, ?, ?)
                       """, (requester_id, addressee_id, message))
        db.conn.commit()

    @staticmethod
    def accept_connection(connection_id: int, db: Database):
        cursor = db.conn.cursor()
        cursor.execute("""
                       UPDATE connections
                       SET status      = 'accepted',
                           accepted_at = CURRENT_TIMESTAMP
                       WHERE id = ?
                       """, (connection_id,))
        db.conn.commit()

    @staticmethod
    def send_message(sender_id: int, receiver_id: int, message: str, db: Database):
        cursor = db.conn.cursor()
        cursor.execute("""
                       INSERT INTO messages (sender_id, receiver_id, message)
                       VALUES (?, ?, ?)
                       """, (sender_id, receiver_id, message))
        db.conn.commit()

    @staticmethod
    def get_conversations(user_id: int, db: Database):
        cursor = db.conn.cursor()
        cursor.execute("""
                       SELECT DISTINCT CASE WHEN sender_id = ? THEN receiver_id ELSE sender_id END as other_user_id,
                                       u.name,
                                       u.user_type,
                                       MAX(m.created_at)                                           as last_message_time
                       FROM messages m
                                JOIN users u ON u.id = CASE WHEN m.sender_id = ? THEN m.receiver_id ELSE m.sender_id END
                       WHERE ? IN (sender_id, receiver_id)
                       GROUP BY other_user_id, u.name, u.user_type
                       ORDER BY last_message_time DESC
                       """, (user_id, user_id, user_id))
        return cursor.fetchall()

    @staticmethod
    def get_messages(user1_id: int, user2_id: int, db: Database):
        cursor = db.conn.cursor()
        cursor.execute("""
                       SELECT m.*, u.name as sender_name
                       FROM messages m
                                JOIN users u ON m.sender_id = u.id
                       WHERE (sender_id = ? AND receiver_id = ?)
                          OR (sender_id = ? AND receiver_id = ?)
                       ORDER BY created_at ASC
                       """, (user1_id, user2_id, user2_id, user1_id))
        return cursor.fetchall()


class KICManager:
    @staticmethod
    def transfer_kic(from_user_id: int, to_user_id: int, amount: int,
                     description: str, db: Database) -> bool:
        cursor = db.conn.cursor()

        cursor.execute("SELECT kic_balance FROM users WHERE id = ?", (from_user_id,))
        balance = cursor.fetchone()[0]

        if balance >= amount:
            cursor.execute("""
                           UPDATE users
                           SET kic_balance = kic_balance - ?
                           WHERE id = ?
                           """, (amount, from_user_id))

            cursor.execute("""
                           UPDATE users
                           SET kic_balance = kic_balance + ?
                           WHERE id = ?
                           """, (amount, to_user_id))

            cursor.execute("""
                           INSERT INTO kic_transactions (user_id, transaction_type, amount, description)
                           VALUES (?, 'sent', ?, ?)
                           """, (from_user_id, -amount, description))

            cursor.execute("""
                           INSERT INTO kic_transactions (user_id, transaction_type, amount, description)
                           VALUES (?, 'received', ?, ?)
                           """, (to_user_id, amount, description))

            db.conn.commit()
            return True
        return False

    @staticmethod
    def get_kic_balance(user_id: int, db: Database) -> int:
        cursor = db.conn.cursor()
        cursor.execute("SELECT kic_balance FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0]

    @staticmethod
    def get_kic_transactions(user_id: int, db: Database, limit: int = 10):
        cursor = db.conn.cursor()
        cursor.execute("""
                       SELECT *
                       FROM kic_transactions
                       WHERE user_id = ?
                       ORDER BY created_at DESC LIMIT ?
                       """, (user_id, limit))
        return cursor.fetchall()


class LabAccessManager:
    @staticmethod
    def generate_credentials():
        username = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        return username, password

    @staticmethod
    def grant_lab_access(lab_id: int, user_id: int, access_level: str,
                         valid_from: str, valid_until: str, db: Database):
        username, password = LabAccessManager.generate_credentials()
        password_hash = AuthManager.hash_password(password)

        cursor = db.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO lab_access 
                (lab_id, user_id, access_level, username, password_hash, valid_from, valid_until)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (lab_id, user_id, access_level, username, password_hash, valid_from, valid_until))
            db.conn.commit()
            return username, password
        except sqlite3.Error as e:
            st.error(f"Error granting lab access: {e}")
            return None, None

    @staticmethod
    def verify_lab_access(lab_id: int, username: str, password: str, db: Database):
        cursor = db.conn.cursor()
        password_hash = AuthManager.hash_password(password)

        try:
            cursor.execute("""
                           SELECT la.*, u.name as user_name, l.name as lab_name
                           FROM lab_access la
                                    JOIN users u ON la.user_id = u.id
                                    JOIN labs l ON la.lab_id = l.id
                           WHERE la.lab_id = ?
                             AND la.username = ?
                             AND la.password_hash = ?
                             AND la.is_active = TRUE
                             AND DATE ('now') BETWEEN la.valid_from
                             AND la.valid_until
                           """, (lab_id, username, password_hash))

            access = cursor.fetchone()
            return dict(access) if access else None
        except sqlite3.Error as e:
            st.error(f"Error verifying access: {e}")
            return None

    @staticmethod
    def get_user_lab_access(user_id: int, db: Database):
        cursor = db.conn.cursor()
        try:
            cursor.execute("""
                           SELECT la.*, l.name as lab_name, u.name as university_name
                           FROM lab_access la
                                    JOIN labs l ON la.lab_id = l.id
                                    JOIN universities u ON l.university_id = u.id
                           WHERE la.user_id = ?
                             AND la.is_active = TRUE
                           ORDER BY la.created_at DESC
                           """, (user_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            st.error(f"Error getting lab access: {e}")
            return []


class ProjectManager:
    @staticmethod
    def get_user_projects(user_id: int, db: Database):
        cursor = db.conn.cursor()
        try:
            cursor.execute("""
                           SELECT p.*,
                                  up.role,
                                  up.status as participation_status,
                                  up.joined_date,
                                  up.completion_date,
                                  up.rating_received,
                                  up.payment_received,
                                  up.contribution_description
                           FROM projects p
                                    JOIN user_projects up ON p.id = up.project_id
                           WHERE up.user_id = ?
                           ORDER BY up.joined_date DESC
                           """, (user_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            st.error(f"Error getting user projects: {e}")
            return []

    @staticmethod
    def apply_to_project(project_id: int, user_id: int, application_text: str,
                         proposed_rate: int, proposed_kic_rate: int, db: Database) -> bool:
        try:
            cursor = db.conn.cursor()
            cursor.execute("""
                           INSERT INTO project_applications (project_id, user_id, application_text,
                                                             proposed_rate, proposed_kic_rate)
                           VALUES (?, ?, ?, ?, ?)
                           """, (project_id, user_id, application_text, proposed_rate, proposed_kic_rate))

            cursor.execute("""
                           UPDATE projects
                           SET applications = applications + 1
                           WHERE id = ?
                           """, (project_id,))

            db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            st.error(f"Error applying to project: {e}")
            return False

    @staticmethod
    def get_project_applications(user_id: int, db: Database):
        cursor = db.conn.cursor()
        try:
            cursor.execute("""
                           SELECT pa.*, p.title, p.organization, p.kic_budget_min, p.kic_budget_max
                           FROM project_applications pa
                                    JOIN projects p ON pa.project_id = p.id
                           WHERE pa.user_id = ?
                           ORDER BY pa.applied_date DESC
                           """, (user_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            st.error(f"Error getting applications: {e}")
            return []


# ==================== PAGES ====================
def show_ultimate_login_page(db: Database):
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('''
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 class="gradient-text" style="font-size: 3.5rem; margin-bottom: 0.5rem;">
                🔬 UAE Innovate Hub
            </h1>
            <p style="font-size: 1.3rem; color: #64748b; margin-bottom: 0.5rem;">
                Knowledge & Innovation Connected
            </p>
            <p style="color: #94a3b8; font-size: 1.1rem;">
                Connect • Collaborate • Create • Transform
            </p>
        </div>
        ''', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Sign In", "🚀 Join the Network"])

        with tab1:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)

            # Demo accounts quick access
            st.markdown("### 🎯 Quick Demo Access")
            demo_accounts = [
                ("ahmed.mansouri@example.com", "Robotics Engineer", "talent", "🤖"),
                ("fatima.zaabi@example.com", "Data Scientist", "talent", "📊"),
                ("sara.hassan@example.com", "Innovation Manager", "company", "🏢"),
                ("mohammed.rashid@uaeu.ac.ae", "AI Professor", "researcher", "🎓")
            ]

            cols = st.columns(2)
            for idx, (email, role, user_type, icon) in enumerate(demo_accounts):
                with cols[idx % 2]:
                    if st.button(f"{icon} {role}", key=f"demo_{email}", use_container_width=True):
                        user = AuthManager.login(email, "password123", db)
                        if user:
                            st.session_state.user = user
                            st.success(f"Welcome, {user['name']}! 🎉")
                            st.balloons()
                            st.rerun()

            st.markdown("---")
            st.markdown("### Or Sign In With Your Account")

            with st.form("login_form"):
                email = st.text_input("Email", placeholder="your.name@company.com")
                password = st.text_input("Password", type="password", value="password123")

                col1, col2 = st.columns(2)
                with col1:
                    remember_me = st.checkbox("Keep me signed in")
                with col2:
                    st.markdown('<a href="#" style="float: right; color: #0077b5;">Forgot password?</a>',
                                unsafe_allow_html=True)

                if st.form_submit_button("Sign In", use_container_width=True):
                    user = AuthManager.login(email, password, db)
                    if user:
                        st.session_state.user = user
                        st.success(f"Welcome back, {user['name']}! 🎉")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")

            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            with st.form("register_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name *")
                    email = st.text_input("Email *")
                    phone = st.text_input("Phone *", placeholder="+971 50 123 4567")
                    location = st.selectbox("Location",
                                            ["Abu Dhabi", "Dubai", "Sharjah", "Ajman",
                                             "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"])

                with col2:
                    password = st.text_input("Password *", type="password")
                    confirm_password = st.text_input("Confirm Password *", type="password")
                    user_type = st.selectbox("I'm joining as",
                                             ["talent", "company", "researcher"])
                    organization = st.text_input("Organization/University *")

                st.markdown("#### What brings you here?")
                interests = st.multiselect("Select your interests:",
                                           ["Find talented professionals", "Discover research opportunities",
                                            "Access testing facilities", "Collaborate on projects",
                                            "Share knowledge", "Build professional network",
                                            "Find investment opportunities", "Learn new skills"])

                terms = st.checkbox("I agree to the Terms of Service and Privacy Policy *")

                if st.form_submit_button("Create Account", use_container_width=True):
                    if password != confirm_password:
                        st.error("Passwords don't match")
                    elif not terms:
                        st.error("Please accept the terms")
                    elif not all([name, email, password, organization, phone]):
                        st.error("Please fill in all required fields")
                    else:
                        success = AuthManager.register(email, password, name, user_type,
                                                       organization, location, phone, db)
                        if success:
                            st.success("🎉 Welcome to UAE Innovate Hub! Please sign in.")
                            st.balloons()
                        else:
                            st.error("Email already exists. Please try signing in.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Database management
        st.markdown("---")
        with st.expander("🔧 Database Management"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Reset Database", type="secondary", use_container_width=True):
                    db.reset_database()
                    db.seed_comprehensive_data()
                    st.success("Database reset successfully!")
                    st.rerun()
            with col2:
                if st.button("🌱 Reseed Data", use_container_width=True):
                    db.seed_comprehensive_data()
                    st.success("Data reseeded successfully!")


def show_ultimate_dashboard(db: Database):
    user = st.session_state.user

    # Welcome header
    st.markdown(f'''
    <div style="margin-bottom: 2rem;">
        <h1 class="gradient-text">Welcome back, {user['name']}! 👋</h1>
        <p style="font-size: 1.1rem; color: #64748b;">
            {user['user_type'].title()} at {user['organization']} • 
            {user['total_projects_completed']} projects completed • 
            <span class="kic-balance">💰 {user['kic_balance']} KIC</span>
        </p>
    </div>
    ''', unsafe_allow_html=True)

    # Get notifications count
    cursor = db.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = FALSE", (user['id'],))
    unread_notifications = cursor.fetchone()[0]

    # Metrics row
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_type = 'talent'")
        talent_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{talent_count}+</div>
            <div style="color: #64748b; font-weight: 600;">Talents</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        cursor.execute("SELECT COUNT(*) FROM companies")
        company_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{company_count}+</div>
            <div style="color: #64748b; font-weight: 600;">Companies</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'Active'")
        active_projects = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{active_projects}</div>
            <div style="color: #64748b; font-weight: 600;">Active Projects</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        cursor.execute("SELECT COUNT(*) FROM labs")
        lab_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{lab_count}+</div>
            <div style="color: #64748b; font-weight: 600;">Research Labs</div>
        </div>
        ''', unsafe_allow_html=True)

    with col5:
        cursor.execute("SELECT COUNT(*) FROM universities")
        uni_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{uni_count}</div>
            <div style="color: #64748b; font-weight: 600;">Universities</div>
        </div>
        ''', unsafe_allow_html=True)

    with col6:
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM connections
                       WHERE (requester_id = ? OR addressee_id = ?)
                         AND status = 'accepted'
                       """, (user['id'], user['id']))
        network_size = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{network_size}</div>
            <div style="color: #64748b; font-weight: 600;">My Network</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        # Notifications
        if unread_notifications > 0:
            st.markdown(f'''
            <div class="modern-card" style="border-left: 4px solid #f59e0b; background: rgba(251, 191, 36, 0.05);">
                <h4>🔔 You have {unread_notifications} new notifications</h4>
            </div>
            ''', unsafe_allow_html=True)

        # My Active Projects
        st.markdown("### 📋 My Active Projects")
        user_projects = ProjectManager.get_user_projects(user['id'], db)
        active_projects = [p for p in user_projects if p['participation_status'] == 'active']

        if active_projects:
            for project in active_projects[:3]:
                urgency_class = f"urgency-{project['urgency'].lower()}"
                st.markdown(f'''
                <div class="project-card">
                    <h4>{project['title']}</h4>
                    <div style="color: #0077b5; font-weight: 600;">
                        Role: {project['role'].replace('_', ' ').title()}
                    </div>
                    <div style="color: #64748b; margin: 0.5rem 0;">
                        📍 {project['location']} • 
                        <span class="{urgency_class}">⚡ {project['urgency']} Priority</span> •
                        📅 Joined: {project['joined_date']}
                    </div>
                    <div style="color: #475569; margin-bottom: 1rem;">
                        {project['description'][:150]}...
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: #16a34a; font-weight: bold;">
                            💰 {project['kic_budget_min']:,} - {project['kic_budget_max']:,} KIC
                        </div>
                        <button class="professional-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                            View Details
                        </button>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No active projects. Browse available projects to get started!")

        # Activity Feed
        st.markdown("### 📈 Network Activity")
        cursor.execute("""
                       SELECT a.*, u.name, u.user_type
                       FROM activities a
                                JOIN users u ON a.user_id = u.id
                       ORDER BY a.created_at DESC LIMIT 10
                       """)
        activities = cursor.fetchall()

        for activity in activities:
            icon_map = {
                "project_completed": "✅",
                "skill_certified": "🎓",
                "connection_made": "🤝",
                "project_started": "🚀",
                "lab_booking": "🔬",
                "university_project": "🎓"
            }

            icon = icon_map.get(activity['activity_type'], "📋")

            st.markdown(f'''
            <div class="activity-item">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="font-size: 1.5rem;">{icon}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1e293b;">{activity['name']}</div>
                        <div style="color: #0077b5; font-weight: 500;">{activity['title']}</div>
                        <div style="color: #64748b; font-size: 0.9rem;">{activity['description']}</div>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">
                        {activity['created_at'][:10]}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

        # Trending Projects
        st.markdown("### 🔥 Trending Projects")
        cursor.execute("""
                       SELECT *
                       FROM projects
                       WHERE status = 'Active'
                       ORDER BY views DESC, applications DESC LIMIT 3
                       """)
        trending_projects = cursor.fetchall()

        for project in trending_projects:
            urgency_class = f"urgency-{project['urgency'].lower()}"

            st.markdown(f'''
            <div class="modern-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4 style="margin-bottom: 0.5rem;">{project['title']}</h4>
                        <div style="color: #0077b5; font-weight: 600; margin-bottom: 0.5rem;">
                            {project['organization']}
                        </div>
                        <div style="color: #64748b; margin-bottom: 1rem;">
                            📍 {project['location']} • 
                            <span class="{urgency_class}">⚡ {project['urgency']} Priority</span> •
                            👁️ {project['views']} views • 
                            📝 {project['applications']} applications
                        </div>
                        <div style="color: #475569;">
                            {project['description'][:120]}...
                        </div>
                    </div>
                    <div style="text-align: right; margin-left: 1rem;">
                        <div style="color: #16a34a; font-weight: bold; font-size: 1.1rem;">
                            💰 {project['kic_budget_min']:,} - {project['kic_budget_max']:,} KIC
                        </div>
                        <div style="color: #64748b; font-size: 0.9rem;">
                            AED {project['budget_min']:,} - {project['budget_max']:,}
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

    with col2:
        # Personal Profile Card
        st.markdown(f'''
        <div class="profile-card">
            <div class="profile-avatar">{user['name'][0].upper()}</div>
            <h3 style="margin-bottom: 0.5rem;">{user['name']}</h3>
            <div style="opacity: 0.9; margin-bottom: 1rem;">{user['organization']}</div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="font-size: 0.9rem; opacity: 0.8;">Reputation Score</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{user['reputation_score']}</div>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px;">
                <div style="font-size: 0.9rem; opacity: 0.8;">Projects Completed</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{user['total_projects_completed']}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # KIC Balance and Recent Transactions
        st.markdown("### 💰 KIC Wallet")

        kic_transactions = KICManager.get_kic_transactions(user['id'], db, 5)

        st.markdown(f'''
        <div class="modern-card">
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: #f59e0b;">
                    {user['kic_balance']} KIC
                </div>
                <div style="color: #64748b;">Available Balance</div>
            </div>
        ''', unsafe_allow_html=True)

        if kic_transactions:
            st.markdown("**Recent Transactions:**")
            for txn in kic_transactions:
                color = "#16a34a" if txn['amount'] > 0 else "#dc2626"
                sign = "+" if txn['amount'] > 0 else ""

                st.markdown(f'''
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;">
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 500;">{txn['transaction_type'].title()}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">{txn['description']}</div>
                    </div>
                    <div style="color: {color}; font-weight: bold;">
                        {sign}{txn['amount']} KIC
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Quick Actions
        st.markdown("### ⚡ Quick Actions")

        actions = [
            ("💬 Messages", "Messages", unread_notifications > 0),
            ("🔍 Find Talent", "Talents", False),
            ("📋 Browse Projects", "Projects", False),
            ("🏢 Explore Labs", "Labs", False),
            ("🎓 Universities", "Universities", False),
            ("💰 KIC Hub", "KIC Hub", False)
        ]

        for label, page, has_notification in actions:
            col = st.container()
            if col.button(label, use_container_width=True, key=f"qa_{page}"):
                st.session_state.current_page = page
                st.rerun()
            if has_notification:
                st.markdown(f'''
                <div style="position: relative; margin-top: -2.5rem; margin-bottom: 0.5rem;">
                    <span class="notification-badge" style="position: absolute; right: 10px;">
                        {unread_notifications}
                    </span>
                </div>
                ''', unsafe_allow_html=True)


def show_talents_page(db: Database):
    st.markdown('<h1 class="gradient-text">👥 Talent Network</h1>', unsafe_allow_html=True)
    st.markdown("Connect with UAE's top innovators, researchers, and industry experts")

    # Search and filters
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        search_query = st.text_input("🔍 Search talents...",
                                     placeholder="Search by name, skills, title, or expertise")

    with col2:
        sort_option = st.selectbox("Sort by",
                                   ["Best Match", "Reputation Score", "Project Count",
                                    "Rating", "Recently Active"])

    with col3:
        view_mode = st.radio("View", ["Professional", "Compact"], horizontal=True)

    # Advanced filters
    with st.expander("🔧 Advanced Filters", expanded=False):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cursor = db.conn.cursor()
            cursor.execute("SELECT DISTINCT location FROM talents")
            locations = [row[0] for row in cursor.fetchall()]
            selected_locations = st.multiselect("Locations", locations)

        with col2:
            availability_options = ["Full-time", "Part-time", "Contract", "Remote"]
            selected_availability = st.multiselect("Availability", availability_options)

        with col3:
            rate_range = st.slider("KIC Hourly rate", 0, 500, (0, 500))

        with col4:
            min_projects = st.slider("Min. projects completed", 0, 50, 0)

    # Fetch talents
    query = """
            SELECT t.*, \
                   u.name, \
                   u.email, \
                   u.location as user_location, \
                   u.is_verified,
                   u.reputation_score, \
                   u.total_projects_completed, \
                   u.phone
            FROM talents t
                     JOIN users u ON t.user_id = u.id
            WHERE 1 = 1 \
            """
    params = []

    if search_query:
        query += " AND (u.name LIKE ? OR t.title LIKE ? OR t.skills LIKE ? OR t.bio LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param] * 4)

    if selected_locations:
        query += f" AND t.location IN ({','.join(['?'] * len(selected_locations))})"
        params.extend(selected_locations)

    if selected_availability:
        query += f" AND t.availability IN ({','.join(['?'] * len(selected_availability))})"
        params.extend(selected_availability)

    query += " AND t.kic_hourly_rate BETWEEN ? AND ?"
    params.extend([rate_range[0], rate_range[1]])

    query += " AND u.total_projects_completed >= ?"
    params.append(min_projects)

    # Sorting
    if sort_option == "Reputation Score":
        query += " ORDER BY u.reputation_score DESC"
    elif sort_option == "Project Count":
        query += " ORDER BY u.total_projects_completed DESC"
    elif sort_option == "Rating":
        query += " ORDER BY t.rating DESC"
    else:
        query += " ORDER BY u.is_verified DESC, u.reputation_score DESC"

    cursor.execute(query, params)
    talents = cursor.fetchall()

    st.markdown(f"### Found {len(talents)} talented professionals")

    # Display talents
    if view_mode == "Professional":
        for talent in talents:
            st.markdown(f'''
            <div class="modern-card">
                <div style="display: flex; gap: 1.5rem;">
                    <div style="flex-shrink: 0;">
                        <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #0077b5, #00a0dc); 
                                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                    color: white; font-size: 1.8rem; font-weight: bold;">
                            {talent['name'][0].upper()}
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                            <h3 style="margin: 0;">{talent['name']}</h3>
                            {f'<span class="status-badge status-verified">✓ Verified</span>' if talent['is_verified'] else ''}
                            <span class="status-badge status-online">🟢 Active</span>
                        </div>
                        <div style="color: #0077b5; font-weight: 600; margin-bottom: 0.5rem;">
                            {talent['title']}
                        </div>
                        <div style="color: #64748b; margin-bottom: 1rem;">
                            📍 {talent['location']} • 💼 {talent['experience']} • 
                            🎓 {talent['education']} • 
                            📊 {talent['reputation_score']} reputation • 
                            ✅ {talent['total_projects_completed']} projects completed
                        </div>
                        <div style="color: #475569; margin-bottom: 1rem;">
                            {talent['bio'][:200]}{'...' if len(talent['bio']) > 200 else ''}
                        </div>
                        <div style="margin-bottom: 1rem;">
                            {' '.join([f'<span class="skill-tag">{skill.strip()}</span>'
                                       for skill in talent['skills'].split(',')[:6]])}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="color: #16a34a; font-weight: bold; font-size: 1.1rem;">
                                    💰 {talent['kic_hourly_rate']} KIC/hr
                                </span>
                                <span style="color: #64748b; margin-left: 1rem;">
                                    AED {talent['hourly_rate']}/hr
                                </span>
                            </div>
                            <div style="display: flex; gap: 0.5rem;">
                                <span class="status-badge status-featured">{talent['availability']}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👤 View Profile", key=f"view_{talent['id']}"):
                    st.session_state.selected_talent_id = talent['id']
                    st.session_state.current_page = "Talent Profile"
                    st.rerun()
            with col2:
                if st.button("🤝 Connect", key=f"connect_{talent['id']}"):
                    st.session_state.connect_talent_id = talent['id']
                    st.rerun()
            with col3:
                if st.button("💬 Message", key=f"message_{talent['id']}"):
                    st.session_state.message_talent_id = talent['id']
                    st.session_state.current_page = "Messages"
                    st.rerun()
            with col4:
                if st.button("💼 Hire", key=f"hire_{talent['id']}"):
                    st.session_state.hire_talent_id = talent['id']
                    st.rerun()

    else:  # Compact view
        for talent in talents:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])

            with col1:
                verified_badge = "✓" if talent['is_verified'] else ""
                st.markdown(f"**{talent['name']} {verified_badge}**  \n{talent['title']}")
            with col2:
                st.markdown(f"{talent['location']} • {talent['availability']}")
            with col3:
                st.markdown(f"**{talent['total_projects_completed']}** projects")
            with col4:
                st.markdown(f"**{talent['kic_hourly_rate']} KIC**/hr")
            with col5:
                if st.button("→", key=f"compact_{talent['id']}"):
                    st.session_state.selected_talent_id = talent['id']
                    st.session_state.current_page = "Talent Profile"
                    st.rerun()


def show_companies_page(db: Database):
    st.markdown('<h1 class="gradient-text">🏢 Partner Companies</h1>', unsafe_allow_html=True)
    st.markdown("Discover innovative companies driving UAE's future")

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM companies ORDER BY rating DESC, total_projects_posted DESC")
    companies = cursor.fetchall()

    # Company metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(companies)}</div>
            <div style="color: #64748b; font-weight: 600;">Partner Companies</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        total_projects = sum(company['total_projects_posted'] for company in companies)
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_projects}</div>
            <div style="color: #64748b; font-weight: 600;">Projects Posted</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        verified_companies = sum(1 for company in companies if company['is_verified'])
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{verified_companies}</div>
            <div style="color: #64748b; font-weight: 600;">Verified</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        avg_rating = sum(company['rating'] for company in companies) / len(companies) if companies else 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f}⭐</div>
            <div style="color: #64748b; font-weight: 600;">Avg. Rating</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # Industry filter
    industries = list(set(company['industry'] for company in companies))
    selected_industry = st.selectbox("Filter by Industry", ["All Industries"] + industries)

    # Display companies
    filtered_companies = companies
    if selected_industry != "All Industries":
        filtered_companies = [c for c in companies if c['industry'] == selected_industry]

    for company in filtered_companies:
        st.markdown(f'''
        <div class="modern-card">
            <div style="display: flex; gap: 1.5rem;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #0077b5, #00a0dc); 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center;
                            color: white; font-size: 1.5rem; font-weight: bold;">
                    {company['name'][:2].upper()}
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                        <h3 style="margin: 0;">{company['name']}</h3>
                        {f'<span class="status-badge status-verified">✓ Verified</span>' if company['is_verified'] else ''}
                        <span class="status-badge status-featured">{company['industry']}</span>
                    </div>
                    <div style="color: #64748b; margin-bottom: 1rem;">
                        📍 {company['location']} • 
                        👥 {company['size']} • 
                        📅 Founded {company['founded_year']} • 
                        ⭐ {company['rating']:.1f} rating • 
                        📋 {company['total_projects_posted']} projects posted
                    </div>
                    <div style="color: #475569; margin-bottom: 1rem;">
                        {company['description']}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: #16a34a; font-weight: bold;">
                                💰 {company['kic_balance']:,} KIC Available
                            </span>
                        </div>
                        <div>
                            <a href="{company['website']}" target="_blank" style="color: #0077b5;">
                                🌐 Visit Website
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 View Projects", key=f"projects_{company['id']}"):
                st.session_state.company_projects_id = company['id']
                st.session_state.current_page = "Projects"
                st.rerun()
        with col2:
            if st.button("💬 Contact", key=f"contact_{company['id']}"):
                st.session_state.contact_company_id = company['id']
                st.rerun()
        with col3:
            if st.button("🤝 Follow", key=f"follow_{company['id']}"):
                st.success("Now following!")


def show_projects_page(db: Database):
    st.markdown('<h1 class="gradient-text">🚀 Innovation Projects</h1>', unsafe_allow_html=True)
    st.markdown("Discover cutting-edge projects and collaboration opportunities")

    # Project metrics
    col1, col2, col3, col4 = st.columns(4)

    cursor = db.conn.cursor()

    with col1:
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'Active'")
        active_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{active_count}</div>
            <div style="color: #64748b; font-weight: 600;">Active Projects</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        cursor.execute("SELECT SUM(kic_budget_max) FROM projects WHERE status = 'Active'")
        total_kic = cursor.fetchone()[0] or 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_kic:,}</div>
            <div style="color: #64748b; font-weight: 600;">Total KIC Available</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        cursor.execute("SELECT COUNT(DISTINCT organization) FROM projects")
        org_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{org_count}</div>
            <div style="color: #64748b; font-weight: 600;">Partner Organizations</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        cursor.execute("SELECT AVG(applications) FROM projects WHERE status = 'Active'")
        avg_applications = cursor.fetchone()[0] or 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{avg_applications:.1f}</div>
            <div style="color: #64748b; font-weight: 600;">Avg. Applications</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # Project tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Active Projects", "⚡ Urgent", "💰 High Value", "🎯 My Applications"])

    with tab1:
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_query = st.text_input("🔍 Search projects...",
                                         placeholder="Search by title, organization, or tags")
        with col2:
            urgency_filter = st.selectbox("Urgency", ["All", "High", "Medium", "Low"])
        with col3:
            remote_filter = st.checkbox("Remote possible", value=False)

        # Fetch projects
        query = """
                SELECT p.*, \
                       c.name                                 as company_name, \
                       c.industry, \
                       c.is_verified                          as company_verified,
                       julianday(deadline) - julianday('now') as days_left
                FROM projects p
                         LEFT JOIN companies c ON p.company_id = c.id
                WHERE p.status = 'Active' \
                """
        params = []

        if search_query:
            query += " AND (p.title LIKE ? OR p.organization LIKE ? OR p.tags LIKE ?)"
            search_param = f"%{search_query}%"
            params.extend([search_param] * 3)

        if urgency_filter != "All":
            query += " AND p.urgency = ?"
            params.append(urgency_filter)

        if remote_filter:
            query += " AND p.remote_possible = TRUE"

        query += " ORDER BY p.views DESC, p.posted DESC"

        cursor.execute(query, params)
        projects = cursor.fetchall()

        if projects:
            for project in projects:
                days_left = int(project['days_left']) if project['days_left'] else 0
                urgency_class = f"urgency-{project['urgency'].lower()}"

                st.markdown(f'''
                <div class="project-card" style="--urgency-color: {'#dc2626' if project['urgency'] == 'High' else '#d97706' if project['urgency'] == 'Medium' else '#16a34a'};">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <div>
                            <h3 style="margin-bottom: 0.5rem;">{project['title']}</h3>
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <span style="color: #0077b5; font-weight: 600;">{project['organization']}</span>
                                {f'<span class="status-badge status-verified">✓ Verified</span>' if project.get('company_verified') else ''}
                                <span class="status-badge status-featured">{project.get('industry', 'Technology')}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #16a34a; font-weight: bold; font-size: 1.3rem;">
                                💰 {project['kic_budget_min']:,} - {project['kic_budget_max']:,} KIC
                            </div>
                            <div style="color: #64748b;">
                                AED {project['budget_min']:,} - {project['budget_max']:,}
                            </div>
                        </div>
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <span>📍 {project['location']}</span> • 
                        <span class="{urgency_class}">⚡ {project['urgency']} Priority</span> • 
                        <span>⏰ {days_left} days left</span> • 
                        <span>👁️ {project['views']} views</span> • 
                        <span>📝 {project['applications']} applications</span>
                        {f" • 🌐 Remote OK" if project['remote_possible'] else ""}
                    </div>

                    <div style="color: #475569; margin-bottom: 1.5rem; line-height: 1.6;">
                        {project['description']}
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <strong style="color: #1e293b;">Requirements:</strong>
                        <div style="color: #64748b; margin-top: 0.5rem;">{project['requirements']}</div>
                    </div>

                    <div style="margin-bottom: 1rem;">
                        {' '.join([f'<span class="skill-tag">{tag.strip()}</span>' for tag in project['tags'].split(',')])}
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("📋 View Details", key=f"view_proj_{project['id']}"):
                        cursor.execute("UPDATE projects SET views = views + 1 WHERE id = ?", (project['id'],))
                        db.conn.commit()
                        st.session_state.selected_project_id = project['id']
                        st.session_state.current_page = "Project Details"
                        st.rerun()

                with col2:
                    if st.button("🚀 Apply Now", key=f"apply_proj_{project['id']}"):
                        st.session_state.apply_project_id = project['id']
                        st.rerun()

                with col3:
                    if st.button("💬 Ask Question", key=f"question_proj_{project['id']}"):
                        st.session_state.question_project_id = project['id']
                        st.rerun()

                with col4:
                    if st.button("⭐ Save", key=f"save_proj_{project['id']}"):
                        st.success("Project saved!")
        else:
            st.info("No projects found matching your criteria.")

    with tab2:  # Urgent Projects
        cursor.execute("""
                       SELECT p.*,
                              c.name                                 as company_name,
                              c.industry,
                              julianday(deadline) - julianday('now') as days_left
                       FROM projects p
                                LEFT JOIN companies c ON p.company_id = c.id
                       WHERE p.urgency = 'High'
                         AND p.status = 'Active'
                       ORDER BY p.deadline ASC
                       """)

        urgent_projects = cursor.fetchall()

        if urgent_projects:
            st.markdown("### ⚡ High Priority Projects - Act Fast!")

            for project in urgent_projects:
                days_left = int(project['days_left']) if project['days_left'] else 0

                st.markdown(f'''
                <div class="modern-card" style="border-left: 4px solid #dc2626;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="color: #dc2626; margin-bottom: 0.5rem;">
                                🚨 {project['title']}
                            </h4>
                            <div style="color: #64748b;">
                                {project['organization']} • {project['location']} • ⏰ {days_left} days left
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #16a34a; font-weight: bold;">
                                💰 {project['kic_budget_max']:,} KIC
                            </div>
                            <button class="professional-btn" style="font-size: 0.9rem;">
                                Apply Now ⚡
                            </button>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No urgent projects at the moment.")

    with tab3:  # High Value Projects
        cursor.execute("""
                       SELECT p.*, c.name as company_name, c.industry
                       FROM projects p
                                LEFT JOIN companies c ON p.company_id = c.id
                       WHERE p.kic_budget_max >= 5000
                         AND p.status = 'Active'
                       ORDER BY p.kic_budget_max DESC
                       """)

        high_value_projects = cursor.fetchall()

        st.markdown("### 💎 Premium Projects - High Value Opportunities")

        for project in high_value_projects:
            st.markdown(f'''
            <div class="modern-card" style="border: 2px solid #f59e0b; background: linear-gradient(135deg, rgba(251, 191, 36, 0.05), rgba(245, 158, 11, 0.05));">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <span style="font-size: 2rem;">💎</span>
                    <div>
                        <h3 style="margin: 0; color: #d97706;">{project['title']}</h3>
                        <div style="color: #0077b5; font-weight: 600;">{project['organization']}</div>
                    </div>
                    <div style="margin-left: auto; text-align: right;">
                        <div style="background: #f59e0b; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                            💰 {project['kic_budget_max']:,} KIC
                        </div>
                    </div>
                </div>
                <div style="color: #475569; margin-bottom: 1rem;">
                    {project['description'][:200]}...
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        📍 {project['location']} • 👁️ {project['views']} views
                    </div>
                    <button class="professional-btn">
                        Apply for Premium Project 💎
                    </button>
                </div>
            </div>
            ''', unsafe_allow_html=True)

    with tab4:  # My Applications
        user = st.session_state.user
        applications = ProjectManager.get_project_applications(user['id'], db)

        st.markdown("### 📋 My Project Applications")

        if applications:
            for app in applications:
                status_color = "#16a34a" if app['status'] == "accepted" else "#f59e0b" if app[
                                                                                              'status'] == "pending" else "#dc2626"
                status_icon = "✅" if app['status'] == "accepted" else "⏳" if app['status'] == "pending" else "❌"

                st.markdown(f'''
                <div class="modern-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin-bottom: 0.5rem;">{app['title']}</h4>
                            <div style="color: #64748b;">
                                {app['organization']} • Applied on {app['applied_date'][:10]}
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <strong>Your Proposal:</strong> {app['proposed_kic_rate']} KIC
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: {status_color}; font-weight: bold; margin-bottom: 0.5rem;">
                                {status_icon} {app['status'].title()}
                            </div>
                            <div style="color: #16a34a; font-weight: bold;">
                                💰 {app['kic_budget_min']:,} - {app['kic_budget_max']:,} KIC
                            </div>
                        </div>
                    </div>
                    {f'<div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 8px;"><strong>Response:</strong> {app["response_message"]}</div>' if app['response_message'] else ''}
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("You haven't applied to any projects yet. Browse active projects to get started!")

        # Application handler
        if hasattr(st.session_state, 'apply_project_id'):
            project_id = st.session_state.apply_project_id

            with st.form("project_application"):
                st.markdown("### 📝 Submit Application")

                application_text = st.text_area("Why are you the perfect fit for this project?",
                                                placeholder="Describe your relevant experience, skills, and approach...")

                col1, col2 = st.columns(2)
                with col1:
                    proposed_rate = st.number_input("Proposed Rate (AED)", min_value=0, value=5000)
                with col2:
                    proposed_kic_rate = st.number_input("Proposed Rate (KIC)", min_value=0, value=250)

                if st.form_submit_button("Submit Application", use_container_width=True):
                    success = ProjectManager.apply_to_project(project_id, user['id'], application_text,
                                                              proposed_rate, proposed_kic_rate, db)
                    if success:
                        st.success("Application submitted successfully!")
                        del st.session_state.apply_project_id
                        st.rerun()
                    else:
                        st.error("You have already applied to this project.")


def show_labs_page(db: Database):
    st.markdown('<h1 class="gradient-text">🔬 Research Labs</h1>', unsafe_allow_html=True)
    st.markdown("Access cutting-edge research facilities across the UAE")

    # Lab metrics
    col1, col2, col3, col4 = st.columns(4)

    cursor = db.conn.cursor()

    with col1:
        cursor.execute("SELECT COUNT(*) FROM labs")
        total_labs = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_labs}</div>
            <div style="color: #64748b; font-weight: 600;">Available Labs</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        cursor.execute("SELECT AVG(rating) FROM labs")
        avg_rating = cursor.fetchone()[0] or 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f}⭐</div>
            <div style="color: #64748b; font-weight: 600;">Average Rating</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        cursor.execute("SELECT COUNT(DISTINCT specialty) FROM labs")
        specialties = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{specialties}</div>
            <div style="color: #64748b; font-weight: 600;">Specializations</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        cursor.execute("SELECT SUM(total_bookings) FROM labs")
        total_bookings = cursor.fetchone()[0] or 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_bookings}</div>
            <div style="color: #64748b; font-weight: 600;">Total Bookings</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # Search and filters
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        search_query = st.text_input("🔍 Search labs...",
                                     placeholder="Search by name, equipment, or specialty")

    with col2:
        sort_by = st.selectbox("Sort by", ["Rating", "Price", "KIC Price", "Availability"])

    with col3:
        payment_method = st.radio("Payment", ["Both", "AED", "KIC"], horizontal=True)

    # Advanced filters
    with st.expander("🔧 Advanced Filters", expanded=False):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cursor.execute("SELECT DISTINCT specialty FROM labs")
            specialties = [row[0] for row in cursor.fetchall()]
            selected_specialties = st.multiselect("Specialties", specialties)

        with col2:
            cursor.execute("SELECT DISTINCT location FROM labs")
            locations = [row[0] for row in cursor.fetchall()]
            selected_locations = st.multiselect("Locations", locations)

        with col3:
            if payment_method in ["Both", "AED"]:
                aed_range = st.slider("AED Price per day", 0, 3000, (0, 3000))
            else:
                aed_range = (0, 10000)

        with col4:
            if payment_method in ["Both", "KIC"]:
                kic_range = st.slider("KIC Price per day", 0, 1500, (0, 1500))
            else:
                kic_range = (0, 5000)

    # Build query
    query = """
            SELECT l.*, u.name as university_name
            FROM labs l
                     JOIN universities u ON l.university_id = u.id
            WHERE 1 = 1 \
            """
    params = []

    if search_query:
        query += " AND (l.name LIKE ? OR l.description LIKE ? OR l.equipment LIKE ? OR l.specialty LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param] * 4)

    if selected_specialties:
        query += f" AND l.specialty IN ({','.join(['?'] * len(selected_specialties))})"
        params.extend(selected_specialties)

    if selected_locations:
        query += f" AND l.location IN ({','.join(['?'] * len(selected_locations))})"
        params.extend(selected_locations)

    query += " AND l.price_per_day BETWEEN ? AND ?"
    params.extend([aed_range[0], aed_range[1]])

    query += " AND l.kic_price_per_day BETWEEN ? AND ?"
    params.extend([kic_range[0], kic_range[1]])

    # Sorting
    if sort_by == "Rating":
        query += " ORDER BY l.rating DESC"
    elif sort_by == "Price":
        query += " ORDER BY l.price_per_day ASC"
    elif sort_by == "KIC Price":
        query += " ORDER BY l.kic_price_per_day ASC"
    else:
        query += " ORDER BY l.available_from ASC"

    cursor.execute(query, params)
    labs = cursor.fetchall()

    st.markdown(f"### Found {len(labs)} laboratories")

    # Display labs
    for lab in labs:
        st.markdown(f'''
        <div class="lab-card">
            <div style="display: flex; gap: 1.5rem;">
                <div style="flex-shrink: 0;">
                    <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #0077b5, #00a0dc); 
                                border-radius: 12px; display: flex; align-items: center; justify-content: center;
                                color: white; font-size: 2rem;">
                        🔬
                    </div>
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 0.5rem;">
                        <div style="flex: 1;">
                            <h3 style="margin-bottom: 0.5rem;">{lab['name']}</h3>
                            <div style="color: #0077b5; font-weight: 600; margin-bottom: 0.5rem;">
                                {lab['university_name']}
                            </div>
                            <div style="color: #64748b; margin-bottom: 1rem;">
                                📍 {lab['location']} • 
                                🧪 {lab['specialty']} • 
                                👥 Capacity: {lab['capacity']} • 
                                ⭐ {lab['rating']:.1f} rating • 
                                📅 {lab['total_bookings']} bookings
                            </div>
                            <div style="color: #475569; margin-bottom: 1rem; line-height: 1.6;">
                                {lab['description']}
                            </div>
                            <div style="margin-bottom: 1rem;">
                                <strong>Equipment:</strong>
                                <div style="margin-top: 0.5rem;">
                                    {' '.join([f'<span class="skill-tag">{eq.strip()}</span>'
                                               for eq in lab['equipment'].split(',')[:4]])}
                                </div>
                            </div>
                            <div style="margin-bottom: 1rem;">
                                <strong>Amenities:</strong>
                                <div style="margin-top: 0.5rem;">
                                    {' '.join([f'<span class="skill-tag">{amenity.strip()}</span>'
                                               for amenity in lab['amenities'].split(',')[:3]])}
                                </div>
                            </div>
                        </div>
                        <div style="text-align: right; margin-left: 2rem;">
                            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0;">
                                <div style="margin-bottom: 1rem;">
                                    <div style="color: #16a34a; font-weight: bold; font-size: 1.3rem;">
                                        💰 {lab['kic_price_per_day']} KIC/day
                                    </div>
                                    <div style="color: #64748b; font-size: 0.9rem;">
                                        or AED {lab['price_per_day']}/day
                                    </div>
                                </div>
                                <div style="color: #64748b; font-size: 0.9rem; margin-bottom: 1rem;">
                                    Available from: {lab['available_from']}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📋 View Details", key=f"view_lab_{lab['id']}"):
                st.session_state.selected_lab_id = lab['id']
                st.session_state.current_page = "Lab Details"
                st.rerun()
        with col2:
            if st.button("💰 Book with KIC", key=f"book_kic_{lab['id']}"):
                st.session_state.book_lab_kic_id = lab['id']
                st.rerun()
        with col3:
            if st.button("💳 Book with AED", key=f"book_aed_{lab['id']}"):
                st.session_state.book_lab_aed_id = lab['id']
                st.rerun()
        with col4:
            if st.button("🔑 Access", key=f"access_lab_{lab['id']}"):
                st.session_state.current_page = "Lab Access"
                st.rerun()


def show_lab_access_page(db: Database):
    st.markdown('<h1 class="gradient-text">🔐 Lab Access Management</h1>', unsafe_allow_html=True)

    user = st.session_state.user
    tab1, tab2, tab3 = st.tabs(["🔑 My Access", "🚪 Verify Access", "📋 Request Access"])

    with tab1:
        lab_access = LabAccessManager.get_user_lab_access(user['id'], db)

        if lab_access:
            st.markdown("### Your Lab Access Credentials")

            for access in lab_access:
                st.markdown(f'''
                <div class="credentials-card">
                    <h4>🔬 {access['lab_name']}</h4>
                    <div style="color: rgba(255, 255, 255, 0.8); margin-bottom: 0.5rem;">
                        {access['university_name']}
                    </div>
                    <div style="color: rgba(255, 255, 255, 0.6); margin-bottom: 1rem;">
                        🎫 Access Level: {access['access_level'].title()} • 
                        📅 Valid until: {access['valid_until']}
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 8px;">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">Login Credentials:</div>
                        <div>
                            Username: <strong>{access['username']}</strong><br>
                            Password: <em>Use your saved password</em>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No lab access credentials yet. Request access below.")

    with tab2:
        st.markdown("### 🚪 Lab Access Verification")

        with st.form("verify_access"):
            cursor = db.conn.cursor()
            cursor.execute("SELECT id, name FROM labs ORDER BY name")
            labs = cursor.fetchall()

            if labs:
                selected_lab = st.selectbox("Select Lab", labs, format_func=lambda x: x[1])
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.form_submit_button("Verify Access", use_container_width=True):
                    if selected_lab and username and password:
                        access = LabAccessManager.verify_lab_access(selected_lab[0], username, password, db)
                        if access:
                            st.success(f"✅ Access granted to {access['lab_name']}!")
                            st.markdown(f'''
                            <div class="modern-card success-animation" style="border-left: 4px solid #16a34a;">
                                <h4>Access Verified</h4>
                                <div>User: {access['user_name']}</div>
                                <div>Lab: {access['lab_name']}</div>
                                <div>Access Level: {access['access_level'].title()}</div>
                                <div>Valid until: {access['valid_until']}</div>
                            </div>
                            ''', unsafe_allow_html=True)
                        else:
                            st.error("❌ Access denied. Invalid credentials or expired access.")
            else:
                st.info("No labs available for access verification.")

    with tab3:
        st.markdown("### 📋 Request Lab Access")

        with st.form("request_access"):
            cursor = db.conn.cursor()
            cursor.execute("""
                           SELECT l.id, l.name, u.name as university_name
                           FROM labs l
                                    JOIN universities u ON l.university_id = u.id
                           ORDER BY u.name, l.name
                           """)
            labs = cursor.fetchall()

            if labs:
                selected_lab = st.selectbox("Select Lab", labs,
                                            format_func=lambda x: f"{x[1]} ({x[2]})")
                access_level = st.selectbox("Access Level", ["basic", "advanced", "premium"])

                col1, col2 = st.columns(2)
                with col1:
                    valid_from = st.date_input("Access From", value=datetime.now().date())
                with col2:
                    valid_until = st.date_input("Access Until",
                                                value=datetime.now().date() + timedelta(days=90))

                purpose = st.text_area("Purpose of Access",
                                       placeholder="Describe your research project or why you need access...")

                if st.form_submit_button("Request Access", use_container_width=True):
                    if selected_lab and purpose:
                        username, password = LabAccessManager.grant_lab_access(
                            selected_lab[0], user['id'], access_level,
                            valid_from.strftime('%Y-%m-%d'), valid_until.strftime('%Y-%m-%d'), db
                        )

                        if username and password:
                            st.success("✅ Lab access granted!")
                            st.markdown(f'''
                            <div class="credentials-card success-animation">
                                <h4>🔑 Your New Lab Credentials</h4>
                                <div style="background: rgba(255, 255, 255, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                                    <div>
                                        <strong>Username:</strong> {username}<br>
                                        <strong>Password:</strong> {password}
                                    </div>
                                </div>
                                <div style="color: #fbbf24; font-size: 0.9rem;">
                                    ⚠️ Save these credentials securely. Password shown only once.
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)
                            st.rerun()
            else:
                st.info("No labs available for access requests.")


def show_universities_page(db: Database):
    st.markdown('<h1 class="gradient-text">🎓 Universities</h1>', unsafe_allow_html=True)
    st.markdown("Leading academic institutions in the UAE innovation ecosystem")

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM universities ORDER BY ranking_national")
    universities = cursor.fetchall()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(universities)}</div>
            <div style="color: #64748b; font-weight: 600;">Universities</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        total_students = sum(uni['total_students'] for uni in universities)
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_students:,}</div>
            <div style="color: #64748b; font-weight: 600;">Total Students</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        total_faculty = sum(uni['total_faculty'] for uni in universities)
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_faculty:,}</div>
            <div style="color: #64748b; font-weight: 600;">Faculty Members</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        cursor.execute("SELECT COUNT(*) FROM labs")
        total_labs = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_labs}</div>
            <div style="color: #64748b; font-weight: 600;">Research Labs</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    for uni in universities:
        cursor.execute("SELECT COUNT(*) FROM labs WHERE university_id = ?", (uni['id'],))
        lab_count = cursor.fetchone()[0]

        st.markdown(f'''
        <div class="modern-card">
            <div style="display: flex; gap: 1.5rem;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #0077b5, #00a0dc); 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center;
                            color: white; font-size: 1.5rem; font-weight: bold;">
                    🎓
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h3>{uni['name']}</h3>
                            <div style="color: #64748b; margin-bottom: 1rem;">
                                📍 {uni['location']} • Est. {uni['established_year']} • 
                                👥 {uni['total_students']:,} students • 
                                👨‍🏫 {uni['total_faculty']} faculty • 
                                🔬 {lab_count} labs •
                                🏆 Rank #{uni['ranking_national']}
                            </div>
                            <div style="color: #475569; margin-bottom: 1rem;">{uni['description']}</div>
                            <div style="margin-top: 1rem;">
                                📧 {uni['contact_email']} • 📞 {uni['contact_phone']}
                                {f' • <a href="{uni["website"]}" target="_blank" style="color: #0077b5;">🌐 Website</a>' if uni['website'] else ''}
                            </div>
                        </div>
                        <div>
                            {f'<span class="status-badge status-verified">✓ Verified</span>' if uni['is_verified'] else ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔬 View Labs", key=f"labs_{uni['id']}"):
                st.session_state.university_labs_id = uni['id']
                st.session_state.current_page = "Labs"
                st.rerun()
        with col2:
            if st.button("👥 View Researchers", key=f"researchers_{uni['id']}"):
                st.session_state.university_researchers_id = uni['id']
                st.session_state.current_page = "Talents"
                st.rerun()
        with col3:
            if st.button("📞 Contact", key=f"contact_uni_{uni['id']}"):
                st.info(f"Contact: {uni['contact_email']} or {uni['contact_phone']}")


def show_kic_hub_page(db: Database):
    user = st.session_state.user

    st.markdown('<h1 class="gradient-text">💰 KIC Hub</h1>', unsafe_allow_html=True)
    st.markdown("**Knowledge and Innovation Connected** - The future of innovation economy")

    # KIC Balance Overview
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'''
        <div class="profile-card">
            <h2 style="margin-bottom: 1rem;">Your KIC Wallet</h2>
            <div style="font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem;">
                {user['kic_balance']}
            </div>
            <div style="font-size: 1.2rem; opacity: 0.8;">KIC Available</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        cursor = db.conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM kic_transactions WHERE user_id = ? AND amount > 0", (user['id'],))
        total_earned = cursor.fetchone()[0] or 0

        st.markdown(f'''
        <div class="modern-card" style="text-align: center; padding: 2rem;">
            <h3>Total Earned</h3>
            <div style="font-size: 2rem; font-weight: bold; color: #16a34a;">
                +{total_earned} KIC
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        cursor.execute("SELECT SUM(amount) FROM kic_transactions WHERE user_id = ? AND amount < 0", (user['id'],))
        total_spent = abs(cursor.fetchone()[0] or 0)

        st.markdown(f'''
        <div class="modern-card" style="text-align: center; padding: 2rem;">
            <h3>Total Spent</h3>
            <div style="font-size: 2rem; font-weight: bold; color: #dc2626;">
                -{total_spent} KIC
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # KIC Features
    tab1, tab2, tab3, tab4 = st.tabs(["💳 Transactions", "📊 Analytics", "🔄 Transfer", "🎁 Earn More"])

    with tab1:
        st.markdown("### Recent Transactions")

        transactions = KICManager.get_kic_transactions(user['id'], db, 20)

        if transactions:
            for txn in transactions:
                color = "#16a34a" if txn['amount'] > 0 else "#dc2626"
                sign = "+" if txn['amount'] > 0 else ""
                icon = "📈" if txn['amount'] > 0 else "📉"

                st.markdown(f'''
                <div class="modern-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span style="font-size: 1.5rem;">{icon}</span>
                            <div>
                                <div style="font-weight: 600;">{txn['transaction_type'].title()}</div>
                                <div style="color: #64748b; font-size: 0.9rem;">{txn['description']}</div>
                                <div style="color: #94a3b8; font-size: 0.8rem;">{txn['created_at']}</div>
                            </div>
                        </div>
                        <div style="color: {color}; font-weight: bold; font-size: 1.2rem;">
                            {sign}{txn['amount']} KIC
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No transactions yet. Start earning KIC by completing projects!")

    with tab2:
        st.markdown("### KIC Analytics")

        # Transaction summary
        cursor.execute("""
                       SELECT strftime('%Y-%m', created_at) as month,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as earned,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as spent
                       FROM kic_transactions
                       WHERE user_id = ?
                       GROUP BY month
                       ORDER BY month DESC
                           LIMIT 6
                       """, (user['id'],))

        monthly_data = cursor.fetchall()

        if monthly_data:
            months = [data['month'] for data in monthly_data][::-1]
            earned = [data['earned'] for data in monthly_data][::-1]
            spent = [data['spent'] for data in monthly_data][::-1]

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Earned', x=months, y=earned, marker_color='#16a34a'))
            fig.add_trace(go.Bar(name='Spent', x=months, y=spent, marker_color='#dc2626'))

            fig.update_layout(
                title="Monthly KIC Activity",
                xaxis_title="Month",
                yaxis_title="KIC Amount",
                barmode='group',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            # Mock data for demo
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            earnings = [50 + i * 5 + (i % 7) * 20 for i in range(30)]

            fig = px.line(x=dates, y=earnings,
                          title="Daily KIC Earnings Projection",
                          labels={'x': 'Date', 'y': 'KIC Earned'})
            fig.update_traces(line_color='#f59e0b', line_width=3)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### Transfer KIC")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Send KIC")
            with st.form("send_kic"):
                cursor = db.conn.cursor()
                cursor.execute("SELECT id, name FROM users WHERE id != ?", (user['id'],))
                other_users = cursor.fetchall()

                recipient = st.selectbox("Send to",
                                         [(u['id'], u['name']) for u in other_users],
                                         format_func=lambda x: x[1])

                amount = st.number_input("Amount (KIC)", min_value=1, max_value=user['kic_balance'], value=100)
                description = st.text_input("Description", value="KIC Transfer")

                if st.form_submit_button("Send KIC 💸", use_container_width=True):
                    success = KICManager.transfer_kic(user['id'], recipient[0], amount, description, db)
                    if success:
                        st.success(f"Successfully sent {amount} KIC to {recipient[1]}!")
                        st.session_state.user['kic_balance'] -= amount
                        st.rerun()
                    else:
                        st.error("Insufficient KIC balance!")

        with col2:
            st.markdown("#### Request KIC")
            with st.form("request_kic"):
                requester = st.selectbox("Request from",
                                         [(u['id'], u['name']) for u in other_users],
                                         format_func=lambda x: x[1])

                req_amount = st.number_input("Amount (KIC)", min_value=1, value=100)
                req_reason = st.text_input("Reason", value="Payment for services")

                if st.form_submit_button("Send Request 📧", use_container_width=True):
                    st.success(f"KIC request sent to {requester[1]}!")

    with tab4:
        st.markdown("### Earn More KIC")

        earning_opportunities = [
            {
                "title": "Complete Your Profile",
                "description": "Add skills, portfolio, and certifications",
                "reward": 100,
                "icon": "👤",
                "progress": 80
            },
            {
                "title": "First Project Completion",
                "description": "Successfully complete your first project",
                "reward": 500,
                "icon": "🎯",
                "progress": 0
            },
            {
                "title": "5-Star Rating",
                "description": "Receive a 5-star rating from a client",
                "reward": 200,
                "icon": "⭐",
                "progress": 60
            },
            {
                "title": "Referral Bonus",
                "description": "Invite a friend to join the platform",
                "reward": 300,
                "icon": "🤝",
                "progress": 20
            },
            {
                "title": "Lab Certification",
                "description": "Complete lab safety certification",
                "reward": 150,
                "icon": "🔬",
                "progress": 100
            },
            {
                "title": "Innovation Challenge",
                "description": "Participate in monthly innovation challenge",
                "reward": 1000,
                "icon": "🏆",
                "progress": 30
            }
        ]

        for opportunity in earning_opportunities:
            st.markdown(f'''
            <div class="modern-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 2rem;">{opportunity['icon']}</span>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; font-size: 1.1rem;">{opportunity['title']}</div>
                            <div style="color: #64748b;">{opportunity['description']}</div>
                            <div style="margin-top: 0.5rem;">
                                <div style="background: #e2e8f0; border-radius: 10px; height: 8px; overflow: hidden;">
                                    <div style="background: linear-gradient(90deg, #16a34a, #22c55e); 
                                               width: {opportunity['progress']}%; height: 100%;"></div>
                                </div>
                                <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.25rem;">
                                    {opportunity['progress']}% Complete
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #16a34a; font-weight: bold; font-size: 1.2rem;">
                            +{opportunity['reward']} KIC
                        </div>
                        <button class="professional-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                            {'Claim' if opportunity['progress'] == 100 else 'Start Now'}
                        </button>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


def show_messages_page(db: Database):
    user = st.session_state.user

    st.markdown('<h1 class="gradient-text">💬 Messages</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Conversations")

        conversations = SocialManager.get_conversations(user['id'], db)

        if conversations:
            for conv in conversations:
                is_active = hasattr(st.session_state, 'active_conversation') and \
                            st.session_state.active_conversation == conv['other_user_id']

                with st.container():
                    if st.button(f"👤 {conv['name']}",
                                 key=f"conv_{conv['other_user_id']}",
                                 use_container_width=True,
                                 type="primary" if is_active else "secondary"):
                        st.session_state.active_conversation = conv['other_user_id']
                        st.rerun()

                    st.markdown(f"<small>{conv['user_type']} • {conv['last_message_time'][:16]}</small>",
                                unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No conversations yet. Connect with talents to start messaging!")

        # Start new conversation
        st.markdown("### Start New Conversation")
        cursor = db.conn.cursor()
        cursor.execute("""
                       SELECT u.id, u.name, u.user_type
                       FROM users u
                       WHERE u.id != ?
                       ORDER BY u.name
                       """, (user['id'],))
        all_users = cursor.fetchall()

        selected_user = st.selectbox("Select user",
                                     [(u['id'], f"{u['name']} ({u['user_type']})") for u in all_users],
                                     format_func=lambda x: x[1])

        if st.button("Start Conversation", use_container_width=True):
            st.session_state.active_conversation = selected_user[0]
            st.rerun()

    with col2:
        if hasattr(st.session_state, 'active_conversation'):
            other_user_id = st.session_state.active_conversation

            # Get other user info
            cursor = db.conn.cursor()
            cursor.execute("SELECT name, user_type FROM users WHERE id = ?", (other_user_id,))
            other_user = cursor.fetchone()

            st.markdown(f"### 💬 Chat with {other_user['name']}")

            # Message history container
            message_container = st.container()

            # Message input at bottom
            with st.form("send_message", clear_on_submit=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    message_text = st.text_input("Type your message...", label_visibility="collapsed")
                with col2:
                    send_button = st.form_submit_button("Send 📤", use_container_width=True)

                if send_button and message_text.strip():
                    SocialManager.send_message(user['id'], other_user_id, message_text, db)
                    st.rerun()

            # Display messages in the container
            with message_container:
                messages = SocialManager.get_messages(user['id'], other_user_id, db)

                st.markdown('<div class="chat-container">', unsafe_allow_html=True)

                for message in messages:
                    bubble_class = "sent" if message['sender_id'] == user['id'] else "received"

                    st.markdown(f'''
                    <div class="message-bubble {bubble_class}">
                        <div style="font-size: 0.9rem;">{message['message']}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.25rem;">
                            {message['created_at'][11:16]}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div style="text-align: center; padding: 4rem; color: #64748b;">
                <h3>👋 Select a conversation to start messaging</h3>
                <p>Connect with talented professionals and start collaborating!</p>
            </div>
            ''', unsafe_allow_html=True)


def show_my_projects_page(db: Database):
    user = st.session_state.user
    st.markdown('<h1 class="gradient-text">📊 My Projects</h1>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🚀 Active Projects", "✅ Completed Projects", "📈 Analytics"])

    user_projects = ProjectManager.get_user_projects(user['id'], db)

    with tab1:
        active_projects = [p for p in user_projects if p['participation_status'] == 'active']

        if active_projects:
            for project in active_projects:
                urgency_class = f"urgency-{project['urgency'].lower()}"

                st.markdown(f'''
                <div class="project-card">
                    <h4>{project['title']}</h4>
                    <div style="color: #0077b5; font-weight: 600; margin-bottom: 0.5rem;">
                        My Role: {project['role'].replace('_', ' ').title()}
                    </div>
                    <div style="color: #64748b; margin-bottom: 1rem;">
                        📍 {project['location']} • 📅 Joined: {project['joined_date']} • 
                        <span class="{urgency_class}">⚡ {project['urgency']} Priority</span> • 
                        📋 Status: {project['status']}
                    </div>
                    <div style="color: #475569; margin-bottom: 1rem;">{project['description']}</div>
                    {'<div style="color: #64748b;"><strong>My Contribution:</strong> ' + project['contribution_description'] + '</div>' if project['contribution_description'] else ''}
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                        <div style="color: #16a34a; font-weight: bold;">
                            💰 {project['kic_budget_min']:,} - {project['kic_budget_max']:,} KIC
                        </div>
                        <button class="professional-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                            View Details
                        </button>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No active projects. Browse available projects to get started!")

    with tab2:
        completed_projects = [p for p in user_projects if p['participation_status'] == 'completed']

        if completed_projects:
            total_earned = sum(p['payment_received'] or 0 for p in completed_projects)
            avg_rating = sum(p['rating_received'] or 0 for p in completed_projects if p['rating_received']) / len(
                [p for p in completed_projects if p['rating_received']]) if any(
                p['rating_received'] for p in completed_projects) else 0

            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{len(completed_projects)}</div>
                    <div style="color: #64748b;">Projects Completed</div>
                </div>
                ''', unsafe_allow_html=True)
            with col2:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{total_earned:,} KIC</div>
                    <div style="color: #64748b;">Total Earned</div>
                </div>
                ''', unsafe_allow_html=True)
            with col3:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{avg_rating:.1f}⭐</div>
                    <div style="color: #64748b;">Average Rating</div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")

            for project in completed_projects:
                st.markdown(f'''
                <div class="modern-card">
                    <h4>✅ {project['title']}</h4>
                    <div style="color: #0077b5; font-weight: 600;">
                        Role: {project['role'].replace('_', ' ').title()}
                    </div>
                    <div style="color: #64748b; margin: 0.5rem 0;">
                        📅 {project['joined_date']} - {project['completion_date']} • 
                        ⭐ Rating: {project['rating_received']:.1f}/5.0 • 
                        💰 Earned: {project['payment_received']} KIC
                    </div>
                    <div style="color: #475569; margin-top: 0.5rem;">
                        <strong>Contribution:</strong> {project['contribution_description']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No completed projects yet. Keep working on your active projects!")

    with tab3:
        st.markdown("### 📊 Project Analytics")

        if user_projects:
            # Project timeline
            project_data = []
            for project in user_projects:
                project_data.append({
                    'Project': project['title'][:30] + '...' if len(project['title']) > 30 else project['title'],
                    'Start': project['joined_date'],
                    'End': project['completion_date'] or datetime.now().strftime('%Y-%m-%d'),
                    'Status': project['participation_status'].title(),
                    'Payment': project['payment_received'] or 0
                })

            df = pd.DataFrame(project_data)

            # Projects over time
            fig = px.timeline(df, x_start="Start", x_end="End", y="Project", color="Status",
                              title="Project Timeline",
                              color_discrete_map={'Active': '#0077b5', 'Completed': '#16a34a'})
            fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

            # Earnings by project
            completed_df = df[df['Payment'] > 0]
            if not completed_df.empty:
                fig2 = px.bar(completed_df, x="Project", y="Payment",
                              title="Earnings by Project (KIC)",
                              color_discrete_sequence=['#16a34a'])
                fig2.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Complete some projects to see analytics!")


def show_profile_page(db: Database):
    user = st.session_state.user

    st.markdown(f'''
    <div style="margin-bottom: 2rem;">
        <h1 class="gradient-text">My Professional Profile</h1>
        <p style="color: #64748b;">Manage your professional presence on UAE Innovate Hub</p>
    </div>
    ''', unsafe_allow_html=True)

    # Profile tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 Profile", "🤝 Network", "💼 Activity", "💰 Wallet", "⚙️ Settings"])

    with tab1:
        col1, col2 = st.columns([1, 2])

        with col1:
            # Enhanced profile card
            st.markdown(f'''
            <div class="profile-card">
                <div class="profile-avatar">{user['name'][0].upper()}</div>
                <h3 style="margin-bottom: 0.5rem;">{user['name']}</h3>
                {f'<span class="status-badge status-verified">✓ Verified</span>' if user['is_verified'] else ''}
                <div style="opacity: 0.9; margin: 1rem 0;">{user['organization']}</div>
                <div style="opacity: 0.8; margin-bottom: 1rem;">📍 {user.get('location', 'UAE')}</div>

                <div style="display: flex; justify-content: space-around; margin: 1.5rem 0;">
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold;">{user['total_projects_completed']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">Projects</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold;">{user['reputation_score']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">Reputation</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold;">{user['kic_balance']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">KIC</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # Quick stats
            cursor = db.conn.cursor()
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM connections
                           WHERE (requester_id = ? OR addressee_id = ?)
                             AND status = 'accepted'
                           """, (user['id'], user['id']))
            network_size = cursor.fetchone()[0]

            st.markdown(f'''
            <div class="modern-card">
                <h4>Professional Stats</h4>
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Network Size:</span>
                        <strong>{network_size} connections</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Profile Views:</span>
                        <strong>127 this month</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>KIC Earned:</span>
                        <strong>2,450 total</strong>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown("### Edit Profile Information")

            with st.form("edit_profile"):
                col_a, col_b = st.columns(2)

                with col_a:
                    name = st.text_input("Full Name", value=user['name'])
                    organization = st.text_input("Organization", value=user['organization'])
                    location = st.selectbox("Location",
                                            ["Abu Dhabi", "Dubai", "Sharjah", "Ajman",
                                             "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"],
                                            index=0 if not user.get('location') else
                                            ["Abu Dhabi", "Dubai", "Sharjah", "Ajman",
                                             "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"].index(
                                                user.get('location', 'Abu Dhabi')))

                with col_b:
                    phone = st.text_input("Phone Number", value=user.get('phone', ''), placeholder="+971 50 123 4567")
                    linkedin_url = st.text_input("LinkedIn Profile", value=user.get('linkedin_url', ''))
                    website_url = st.text_input("Website/Portfolio", value=user.get('website_url', ''))

                bio = st.text_area("Professional Bio",
                                   value=user.get('bio', ''),
                                   placeholder="Tell the community about your expertise, interests, and goals...")

                # Professional details for talents
                if user['user_type'] == 'talent':
                    st.markdown("#### Talent-Specific Information")

                    # Get talent info if exists
                    cursor.execute("SELECT * FROM talents WHERE user_id = ?", (user['id'],))
                    talent_info = cursor.fetchone()

                    col_c, col_d = st.columns(2)
                    with col_c:
                        title = st.text_input("Professional Title",
                                              value=talent_info['title'] if talent_info else "",
                                              placeholder="e.g., Senior Data Scientist")
                        experience = st.selectbox("Years of Experience",
                                                  ["0-1 years", "2-3 years", "4-5 years", "6-10 years", "10+ years"],
                                                  index=0 if not talent_info else
                                                  ["0-1 years", "2-3 years", "4-5 years", "6-10 years",
                                                   "10+ years"].index(talent_info['experience']))

                    with col_d:
                        availability = st.selectbox("Availability",
                                                    ["Full-time", "Part-time", "Contract", "Remote"],
                                                    index=0 if not talent_info else
                                                    ["Full-time", "Part-time", "Contract", "Remote"].index(
                                                        talent_info['availability']))
                        hourly_rate = st.number_input("Hourly Rate (AED)",
                                                      min_value=0,
                                                      value=talent_info['hourly_rate'] if talent_info else 150)

                    skills = st.text_input("Skills",
                                           value=talent_info['skills'] if talent_info else "",
                                           placeholder="Python, Machine Learning, Data Analysis, etc.")
                    certifications = st.text_input("Certifications",
                                                   value=talent_info['certifications'] if talent_info else "",
                                                   placeholder="AWS Certified, PMP, etc.")

                if st.form_submit_button("Save Profile Changes", use_container_width=True):
                    cursor = db.conn.cursor()
                    cursor.execute("""
                                   UPDATE users
                                   SET name         = ?,
                                       organization = ?,
                                       bio          = ?,
                                       location     = ?,
                                       phone        = ?,
                                       linkedin_url = ?,
                                       website_url  = ?
                                   WHERE id = ?
                                   """,
                                   (name, organization, bio, location, phone, linkedin_url, website_url, user['id']))

                    if user['user_type'] == 'talent' and talent_info:
                        cursor.execute("""
                                       UPDATE talents
                                       SET title           = ?,
                                           experience      = ?,
                                           availability    = ?,
                                           hourly_rate     = ?,
                                           kic_hourly_rate = ?,
                                           skills          = ?,
                                           certifications  = ?
                                       WHERE user_id = ?
                                       """, (title, experience, availability, hourly_rate, hourly_rate // 20,
                                             skills, certifications, user['id']))

                    db.conn.commit()

                    st.success("✅ Profile updated successfully!")
                    st.session_state.user.update({
                        'name': name,
                        'organization': organization,
                        'bio': bio,
                        'location': location,
                        'phone': phone,
                        'linkedin_url': linkedin_url,
                        'website_url': website_url
                    })
                    st.rerun()

    with tab2:
        st.markdown("### 🤝 Professional Network")

        # Network statistics
        col1, col2, col3 = st.columns(3)

        cursor = db.conn.cursor()

        with col1:
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM connections
                           WHERE (requester_id = ? OR addressee_id = ?)
                             AND status = 'accepted'
                           """, (user['id'], user['id']))
            connections_count = cursor.fetchone()[0]

            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{connections_count}</div>
                <div style="color: #64748b; font-weight: 600;">Connections</div>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM connections
                           WHERE addressee_id = ?
                             AND status = 'pending'
                           """, (user['id'],))
            pending_requests = cursor.fetchone()[0]

            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{pending_requests}</div>
                <div style="color: #64748b; font-weight: 600;">Pending Requests</div>
            </div>
            ''', unsafe_allow_html=True)

        with col3:
            network_growth = "+12%"

            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{network_growth}</div>
                <div style="color: #64748b; font-weight: 600;">This Month</div>
            </div>
            ''', unsafe_allow_html=True)

        # Show connections
        cursor.execute("""
                       SELECT u.id, u.name, u.user_type, u.organization, u.is_verified
                       FROM connections c
                                JOIN users u
                                     ON (CASE WHEN c.requester_id = ? THEN c.addressee_id ELSE c.requester_id END =
                                         u.id)
                       WHERE (c.requester_id = ? OR c.addressee_id = ?)
                         AND c.status = 'accepted'
                       ORDER BY c.accepted_at DESC
                       """, (user['id'], user['id'], user['id']))

        connections = cursor.fetchall()

        if connections:
            st.markdown("#### Your Professional Network")

            for connection in connections:
                st.markdown(f'''
                <div class="modern-card">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #0077b5, #00a0dc); 
                                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                    color: white; font-weight: bold;">
                            {connection['name'][0].upper()}
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600;">{connection['name']}</div>
                            <div style="color: #64748b;">{connection['organization']}</div>
                            <div style="color: #0077b5; font-size: 0.9rem;">{connection['user_type'].title()}</div>
                        </div>
                        <div>
                            {f'<span class="status-badge status-verified">✓</span>' if connection['is_verified'] else ''}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        # Connection requests
        if pending_requests > 0:
            st.markdown("#### Pending Connection Requests")

            cursor.execute("""
                           SELECT c.id, u.name, u.user_type, u.organization, c.message
                           FROM connections c
                                    JOIN users u ON c.requester_id = u.id
                           WHERE c.addressee_id = ?
                             AND c.status = 'pending'
                           """, (user['id'],))

            requests = cursor.fetchall()

            for request in requests:
                st.markdown(f'''
                <div class="modern-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600;">{request['name']}</div>
                            <div style="color: #64748b;">{request['organization']}</div>
                            <div style="color: #475569; font-size: 0.9rem; margin-top: 0.5rem;">
                                "{request['message']}"
                            </div>
                        </div>
                        <div style="display: flex; gap: 0.5rem;">
                            <button class="professional-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                                Accept
                            </button>
                            <button class="professional-btn" style="background: #64748b; font-size: 0.9rem; padding: 0.5rem 1rem;">
                                Decline
                            </button>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Accept", key=f"accept_{request['id']}"):
                        SocialManager.accept_connection(request['id'], db)
                        st.success("Connection accepted!")
                        st.rerun()
                with col2:
                    if st.button("Decline", key=f"decline_{request['id']}"):
                        cursor.execute("UPDATE connections SET status = 'declined' WHERE id = ?", (request['id'],))
                        db.conn.commit()
                        st.info("Connection declined.")
                        st.rerun()

    with tab3:
        st.markdown("### 💼 Professional Activity")

        # Activity metrics
        col1, col2, col3 = st.columns(3)

        cursor.execute("SELECT COUNT(*) FROM activities WHERE user_id = ?", (user['id'],))
        total_activities = cursor.fetchone()[0]

        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{total_activities}</div>
                <div style="color: #64748b; font-weight: 600;">Total Activities</div>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-value">3</div>
                <div style="color: #64748b; font-weight: 600;">This Week</div>
            </div>
            ''', unsafe_allow_html=True)

        with col3:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-value">127</div>
                <div style="color: #64748b; font-weight: 600;">Profile Views</div>
            </div>
            ''', unsafe_allow_html=True)

        # Recent activity
        cursor.execute("""
                       SELECT *
                       FROM activities
                       WHERE user_id = ?
                       ORDER BY created_at DESC LIMIT 10
                       """, (user['id'],))

        activities = cursor.fetchall()

        if activities:
            st.markdown("#### Recent Activity")

            for activity in activities:
                icon_map = {
                    "project_completed": "✅",
                    "skill_certified": "🎓",
                    "connection_made": "🤝",
                    "project_started": "🚀",
                    "lab_booking": "🔬",
                    "university_project": "🎓"
                }

                icon = icon_map.get(activity['activity_type'], "📋")

                st.markdown(f'''
                <div class="activity-item">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 1.5rem;">{icon}</span>
                        <div style="flex: 1;">
                            <div style="font-weight: 600;">{activity['title']}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">{activity['description']}</div>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">
                            {activity['created_at'][:10]}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No recent activity. Start connecting and working on projects to build your activity history!")

    with tab4:
        st.markdown("### 💰 KIC Wallet Management")

        col1, col2 = st.columns([2, 1])

        with col1:
            # KIC balance overview
            st.markdown(f'''
            <div class="profile-card">
                <h3>Current KIC Balance</h3>
                <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0;">
                    {user['kic_balance']} KIC
                </div>
                <div style="opacity: 0.8;">Knowledge & Innovation Connected Currency</div>
            </div>
            ''', unsafe_allow_html=True)

            # Recent transactions
            st.markdown("#### Recent KIC Transactions")

            transactions = KICManager.get_kic_transactions(user['id'], db, 10)

            if transactions:
                for txn in transactions:
                    color = "#16a34a" if txn['amount'] > 0 else "#dc2626"
                    sign = "+" if txn['amount'] > 0 else ""
                    icon = "📈" if txn['amount'] > 0 else "📉"

                    st.markdown(f'''
                    <div class="modern-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <span style="font-size: 1.5rem;">{icon}</span>
                                <div>
                                    <div style="font-weight: 600;">{txn['transaction_type'].title()}</div>
                                    <div style="color: #64748b; font-size: 0.9rem;">{txn['description']}</div>
                                    <div style="color: #94a3b8; font-size: 0.8rem;">{txn['created_at'][:16]}</div>
                                </div>
                            </div>
                            <div style="color: {color}; font-weight: bold; font-size: 1.2rem;">
                                {sign}{txn['amount']} KIC
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.info("No KIC transactions yet.")

        with col2:
            # Quick actions
            st.markdown("#### Quick Actions")

            if st.button("💸 Send KIC", use_container_width=True):
                st.session_state.current_page = "KIC Hub"
                st.rerun()

            if st.button("📊 View Analytics", use_container_width=True):
                st.session_state.current_page = "KIC Hub"
                st.rerun()

            if st.button("🎁 Earn More KIC", use_container_width=True):
                st.session_state.current_page = "KIC Hub"
                st.rerun()

            # KIC earning tips
            st.markdown('''
            <div class="modern-card">
                <h4>💡 Earning Tips</h4>
                <div style="font-size: 0.9rem; line-height: 1.6;">
                    • Complete projects successfully<br>
                    • Maintain high ratings<br>
                    • Refer new talents<br>
                    • Use labs regularly<br>
                    • Stay active in community
                </div>
            </div>
            ''', unsafe_allow_html=True)

    with tab5:
        st.markdown("### ⚙️ Account Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Account Security")

            with st.form("change_password"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")

                if st.form_submit_button("Update Password"):
                    if new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(new_password) < 8:
                        st.error("Password must be at least 8 characters")
                    else:
                        # Verify current password
                        cursor = db.conn.cursor()
                        cursor.execute("""
                                       SELECT id
                                       FROM users
                                       WHERE id = ?
                                         AND password_hash = ?
                                       """, (user['id'], AuthManager.hash_password(current_password)))

                        if cursor.fetchone():
                            cursor.execute("""
                                           UPDATE users
                                           SET password_hash = ?
                                           WHERE id = ?
                                           """, (AuthManager.hash_password(new_password), user['id']))
                            db.conn.commit()
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error("Current password is incorrect")

        with col2:
            st.markdown("#### Notification Preferences")

            notification_settings = {
                "Email notifications for new projects": True,
                "Email notifications for messages": True,
                "Email notifications for bookings": True,
                "Weekly activity summary": False,
                "KIC transaction alerts": True,
                "Connection requests": True
            }

            for setting, default_value in notification_settings.items():
                st.checkbox(setting, value=default_value, key=f"notif_{setting}")

            if st.button("Save Notification Settings", use_container_width=True):
                st.success("✅ Notification preferences saved!")

        st.markdown("---")

        # Account actions
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📧 Export My Data", use_container_width=True):
                st.info("Data export will be sent to your email within 24 hours.")

        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        with col3:
            if st.button("🗑️ Delete Account", type="secondary", use_container_width=True):
                st.warning("⚠️ This action cannot be undone!")
                if st.checkbox("I understand this will permanently delete my account"):
                    if st.button("Confirm Deletion", type="secondary"):
                        st.error("Account deletion requires admin approval. Request submitted.")


# ==================== MAIN APPLICATION ====================
def main():
    # Load enhanced styles
    load_ultimate_css()

    # Initialize database with error handling
    try:
        db = Database()
        db.seed_comprehensive_data()
    except sqlite3.OperationalError as e:
        st.error(f"""
        **Database Schema Error**: {e}

        This usually happens when you have an old database file with a different schema.

        **Solutions:**
        1. Delete the file `innovate_hub_ultimate.db` from your project folder and restart the app
        2. Or use the "Reset Database" button on the login page
        """)
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error initializing database: {e}")
        st.stop()

    # Check authentication
    if 'user' not in st.session_state:
        show_ultimate_login_page(db)
        return

    # Navigation header
    st.markdown(f'''
    <div class="nav-container">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; padding: 0 1rem;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <h2 class="gradient-text" style="margin: 0; cursor: pointer;" onclick="window.location.reload()">
                    🔬 UAE Innovate Hub
                </h2>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span class="kic-balance">💰 {st.session_state.user['kic_balance']} KIC</span>
                <span style="color: #64748b;">
                    {st.session_state.user['name']} • {st.session_state.user['user_type'].title()}
                </span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Enhanced navigation menu
    pages = {
        "Home": ("🏠", "Dashboard"),
        "Talents": ("👥", "Talent Network"),
        "Companies": ("🏢", "Companies"),
        "Projects": ("📋", "Projects"),
        "My Projects": ("📊", "My Projects"),
        "Labs": ("🔬", "Research Labs"),
        "Lab Access": ("🔐", "Lab Access"),
        "Universities": ("🎓", "Universities"),
        "KIC Hub": ("💰", "KIC Hub"),
        "Messages": ("💬", "Messages"),
        "Profile": ("👤", "Profile")
    }

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Create navigation buttons
    cols = st.columns(len(pages))

    for idx, (page, (icon, label)) in enumerate(pages.items()):
        with cols[idx]:
            # Check for notifications
            has_notification = False
            if page == "Messages":
                cursor = db.conn.cursor()
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM messages
                               WHERE receiver_id = ?
                                 AND is_read = FALSE
                               """, (st.session_state.user['id'],))
                unread_messages = cursor.fetchone()[0]
                has_notification = unread_messages > 0

            button_type = "primary" if st.session_state.current_page == page else "secondary"

            if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True, type=button_type):
                st.session_state.current_page = page
                # Clear any temporary session state
                temp_keys = ['selected_talent_id', 'connect_talent_id', 'message_talent_id',
                             'hire_talent_id', 'apply_project_id', 'selected_project_id',
                             'book_lab_kic_id', 'book_lab_aed_id', 'selected_lab_id']
                for key in temp_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    st.markdown("---")

    # Display selected page
    try:
        if st.session_state.current_page == "Home":
            show_ultimate_dashboard(db)
        elif st.session_state.current_page == "Talents":
            show_talents_page(db)
        elif st.session_state.current_page == "Companies":
            show_companies_page(db)
        elif st.session_state.current_page == "Projects":
            show_projects_page(db)
        elif st.session_state.current_page == "My Projects":
            show_my_projects_page(db)
        elif st.session_state.current_page == "Labs":
            show_labs_page(db)
        elif st.session_state.current_page == "Lab Access":
            show_lab_access_page(db)
        elif st.session_state.current_page == "Universities":
            show_universities_page(db)
        elif st.session_state.current_page == "KIC Hub":
            show_kic_hub_page(db)
        elif st.session_state.current_page == "Messages":
            show_messages_page(db)
        elif st.session_state.current_page == "Profile":
            show_profile_page(db)
        else:
            show_ultimate_dashboard(db)
    except Exception as e:
        st.error(f"Error loading page: {e}")
        if st.button("Return to Dashboard"):
            st.session_state.current_page = "Home"
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown('''
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p>🔬 KIC Innovate Hub - Knowledge & Innovation Connected</p>
        <p style="font-size: 0.9rem;">Empowering innovation across the United Arab Emirates</p>
        <p style="font-size: 0.9rem;">Authors: Alisher Beisembekov & Ghanim Al-Falasi</p>
        <div style="margin-top: 1rem;">
            <a href="#" style="color: #0077b5; margin: 0 1rem;">About</a>
            <a href="#" style="color: #0077b5; margin: 0 1rem;">Privacy</a>
            <a href="#" style="color: #0077b5; margin: 0 1rem;">Terms</a>
            <a href="#" style="color: #0077b5; margin: 0 1rem;">Support</a>
        </div>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
