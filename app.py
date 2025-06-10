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
from streamlit_lottie import st_lottie
import requests

# ==================== КОНФИГУРАЦИЯ ====================
st.set_page_config(
    page_title="UAE Innovate Hub | by Alisher Beisembekov",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# UAE Innovate Hub\n\nDeveloped by **Alisher Beisembekov**\n\nA platform connecting UAE's innovation ecosystem.",
        'Report a bug': "https://github.com/alisherbeisembekov/uae-innovate-hub/issues",
    }
)

# ==================== ИНФОРМАЦИЯ ОБ АВТОРЕ ====================
__author__ = "Alisher Beisembekov"
__version__ = "1.0.0"
__email__ = "alisher.beisembekov@example.com"  # Замени на свой email
__copyright__ = "Copyright 2024, Alisher Beisembekov"
__linkedin__ = "https://linkedin.com/in/alisherbeisembekov"  # Замени на свой LinkedIn
__github__ = "https://github.com/alisherbeisembekov"  # Замени на свой GitHub

# ==================== БАЗА ДАННЫХ ====================
class Database:
    def __init__(self, db_path="innovate_hub.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        
    def create_tables(self):
        """Создание таблиц в БД"""
        cursor = self.conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            user_type TEXT NOT NULL,
            organization TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Таблица лабораторий
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS labs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            university TEXT NOT NULL,
            location TEXT NOT NULL,
            specialty TEXT NOT NULL,
            available_from DATE,
            equipment TEXT,
            description TEXT,
            contact TEXT,
            price_per_day INTEGER,
            rating REAL DEFAULT 0,
            image_url TEXT,
            capacity INTEGER,
            amenities TEXT
        )''')
        
        # Таблица талантов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS talents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            experience TEXT,
            education TEXT,
            skills TEXT,
            availability TEXT,
            bio TEXT,
            hourly_rate INTEGER,
            portfolio_url TEXT,
            linkedin_url TEXT,
            rating REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        
        # Таблица проектов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            location TEXT NOT NULL,
            deadline DATE,
            posted DATE DEFAULT CURRENT_DATE,
            description TEXT,
            requirements TEXT,
            tags TEXT,
            budget_min INTEGER,
            budget_max INTEGER,
            status TEXT DEFAULT 'Active',
            contact TEXT,
            views INTEGER DEFAULT 0,
            applications INTEGER DEFAULT 0
        )''')
        
        # Таблица бронирований
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lab_id INTEGER,
            start_date DATE,
            end_date DATE,
            purpose TEXT,
            status TEXT DEFAULT 'Pending',
            total_cost INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (lab_id) REFERENCES labs (id)
        )''')
        
        # Таблица отзывов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_type TEXT,
            item_id INTEGER,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        
        # Таблица уведомлений
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            message TEXT,
            type TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        
        self.conn.commit()
        
    def seed_data(self):
        """Заполнение БД начальными данными"""
        cursor = self.conn.cursor()
        
        # Проверяем, есть ли уже данные
        cursor.execute("SELECT COUNT(*) FROM labs")
        if cursor.fetchone()[0] > 0:
            return
            
        # Добавляем лаборатории
        labs_data = [
            ("Khalifa University Robotics Lab", "Khalifa University", "Abu Dhabi", 
             "Robotics & AI", "2024-01-15", "Industrial Robots,Motion Capture System,Collaborative Robots,3D Vision Systems",
             "State-of-the-art robotics laboratory specializing in humanoid robots, industrial automation, and AI-driven robotics research. Features 10 robotic workstations.",
             "robotics.lab@ku.ac.ae", 1500, 4.8, None, 20, "3D Printers,VR Equipment,Conference Room,High-Speed Internet"),
            
            ("UAEU Advanced Materials Lab", "UAE University", "Al Ain",
             "Materials Science", "2024-02-01", "SEM,X-ray Diffractometer,AFM,Tensile Testing Machine,Spectroscopy",
             "Leading materials research facility with comprehensive characterization capabilities for nanomaterials, composites, and advanced alloys.",
             "materials@uaeu.ac.ae", 1200, 4.6, None, 15, "Clean Room,Chemical Storage,Safety Equipment,Fume Hoods"),
             
            ("DSO Drone Testing Zone", "Dubai Silicon Oasis", "Dubai",
             "UAV Testing", "2024-01-10", "Open Testing Field,Flight Monitoring Systems,Weather Station,Obstacle Course",
             "Dedicated 30,000 sq.m outdoor facility for testing drone capabilities, autonomous flight systems, and aerial applications.",
             "drones@dso.ae", 800, 4.9, None, 50, "Charging Stations,Control Tower,Safety Nets,Workshop"),
            
            ("AUS Biotechnology Research Center", "American University of Sharjah", "Sharjah",
             "Biotechnology", "2024-01-20", "PCR Machines,Cell Culture Facility,Flow Cytometer,Centrifuges,Incubators",
             "Modern biotech lab focusing on genetic research, molecular biology, and biomedical applications. BSL-2 certified facility.",
             "biotech@aus.edu", 1100, 4.7, None, 12, "Sterile Room,Cold Storage,Autoclave,Biosafety Cabinets"),
            
            ("NYUAD Computer Vision Lab", "NYU Abu Dhabi", "Abu Dhabi",
             "Computer Vision & AI", "2024-01-25", "GPU Clusters,Motion Tracking Systems,High-Speed Cameras,VR/AR Equipment",
             "Cutting-edge facility for computer vision research with 50+ GPU cluster and specialized imaging hardware.",
             "vision@nyuad.ae", 1400, 4.8, None, 18, "Server Room,Dark Room,Green Screen Studio,Meeting Rooms"),
            
            ("Masdar Institute Solar Testing Facility", "Masdar Institute", "Abu Dhabi",
             "Renewable Energy", "2024-02-05", "Solar Simulators,PV Testing Equipment,Weather Monitoring,Thermal Cameras",
             "Outdoor and indoor testing facilities for solar panels, concentrated solar power, and energy storage systems.",
             "solar@masdar.ac.ae", 1300, 4.9, None, 25, "Outdoor Test Field,Control Room,Data Center,Workshop"),
            
            ("Zayed University 3D Printing Lab", "Zayed University", "Dubai",
             "Advanced Manufacturing", "2024-01-18", "Industrial 3D Printers,Metal Printers,Scanners,CAD Workstations",
             "Advanced additive manufacturing lab with 15+ 3D printers including metal, polymer, and ceramic printing capabilities.",
             "3dlab@zu.ac.ae", 900, 4.5, None, 16, "Material Storage,Post-Processing Area,Design Studio,Training Room"),
            
            ("UAEU Nanotechnology Center", "UAE University", "Al Ain",
             "Nanotechnology", "2024-02-08", "Electron Microscopes,AFM,Chemical Vapor Deposition,Spin Coater",
             "State-of-the-art nanofabrication and characterization facility for nanomaterials research and development.",
             "nanotech@uaeu.ac.ae", 1600, 4.7, None, 10, "Clean Room Class 100,Chemical Lab,Characterization Suite"),
            
            ("Ajman University IoT Lab", "Ajman University", "Ajman",
             "IoT & Embedded Systems", "2024-01-30", "IoT Development Kits,Sensor Arrays,Network Equipment,Oscilloscopes",
             "Comprehensive IoT testing facility with various sensors, communication protocols, and edge computing devices.",
             "iot@ajman.ac.ae", 700, 4.4, None, 20, "Electronics Workshop,Server Rack,Meeting Space,Component Storage"),
            
            ("RAK Medical Simulation Center", "RAK Medical University", "Ras Al Khaimah",
             "Medical Technology", "2024-02-12", "Medical Simulators,VR Training Systems,Surgical Robots,Imaging Equipment",
             "Advanced medical training facility with high-fidelity patient simulators and surgical training systems.",
             "medsim@rakmhsu.ac.ae", 1800, 4.8, None, 30, "Operating Theater,ICU Simulation,Debriefing Rooms,Control Center"),
            
            ("Khalifa University Quantum Lab", "Khalifa University", "Abu Dhabi",
             "Quantum Computing", "2024-02-15", "Quantum Computer Access,Cryogenic Systems,Laser Systems,Control Electronics",
             "One of the region's first quantum computing research facilities with access to quantum processors and simulators.",
             "quantum@ku.ac.ae", 2500, 4.9, None, 8, "Shielded Room,Laser Safety Area,Theory Room,Visitor Center"),
            
            ("University of Sharjah Chemistry Lab", "University of Sharjah", "Sharjah",
             "Chemistry & Pharma", "2024-01-22", "NMR Spectrometer,Mass Spectrometer,HPLC,Gas Chromatograph",
             "Comprehensive analytical chemistry lab supporting pharmaceutical research and chemical analysis.",
             "chemistry@sharjah.ac.ae", 1000, 4.6, None, 14, "Fume Hoods,Chemical Storage,Sample Prep Area,Instrument Room"),
            
            ("HBMSU VR Learning Lab", "Hamdan Bin Mohammed Smart University", "Dubai",
             "Virtual Reality & Education", "2024-02-03", "VR Headsets,Motion Capture,Haptic Devices,360° Cameras",
             "Immersive learning environment with latest VR/AR technology for educational content development.",
             "vrlab@hbmsu.ac.ae", 850, 4.5, None, 24, "Motion Capture Studio,Development Stations,Demo Area,Content Library"),
            
            ("ADU Autonomous Systems Lab", "Abu Dhabi University", "Abu Dhabi",
             "Autonomous Systems", "2024-01-28", "Autonomous Vehicles,LIDAR Systems,GPS/INS,Simulation Software",
             "Testing facility for autonomous ground and aerial vehicles with indoor and outdoor testing areas.",
             "autonomous@adu.ac.ae", 1350, 4.7, None, 22, "Test Track,Simulation Room,Vehicle Bay,Control Center"),
            
            ("Sorbonne Abu Dhabi AI Lab", "Sorbonne University Abu Dhabi", "Abu Dhabi",
             "Artificial Intelligence", "2024-02-10", "AI Workstations,Deep Learning Servers,Robot Platforms,Smart Sensors",
             "Multidisciplinary AI research lab focusing on machine learning, NLP, and intelligent systems.",
             "ailab@sorbonne.ae", 1150, 4.6, None, 20, "Server Farm,Collaboration Space,Demo Room,Library"),
        ]
        
        cursor.executemany('''
        INSERT INTO labs (name, university, location, specialty, available_from, 
                         equipment, description, contact, price_per_day, rating, 
                         image_url, capacity, amenities)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', labs_data)
        
        # Добавляем пользователей и таланты
        users_data = [
            ("ahmed.mansouri@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Ahmed Al Mansouri", "talent", "Tech Innovations LLC"),
            ("fatima.zaabi@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Fatima Al Zaabi", "talent", "Analytics Solutions"),
            ("rashid.marzouqi@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Dr. Rashid Al Marzouqi", "talent", "Advanced Materials Research Center"),
            ("sara.hashemi@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Dr. Sara Al Hashemi", "talent", "BioTech Solutions"),
            ("mohammed.qasimi@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Mohammed Al Qasimi", "talent", "Neural Networks Lab"),
            ("layla.shamsi@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Layla Al Shamsi", "talent", "Sky Innovations"),
            ("khalid.rahman@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Khalid Rahman", "talent", "IoT Systems Corp"),
            ("mariam.ali@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Dr. Mariam Ali", "talent", "Renewable Energy Institute"),
            ("omar.hassan@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Omar Hassan", "talent", "Autonomous Vehicles Lab"),
            ("noura.abdullah@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Noura Abdullah", "talent", "3D Manufacturing Hub"),
            ("youssef.ibrahim@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Dr. Youssef Ibrahim", "talent", "Quantum Computing Center"),
            ("huda.salem@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Huda Salem", "talent", "Cybersecurity Solutions"),
            ("tariq.ahmed@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Tariq Ahmed", "talent", "Blockchain Lab"),
            ("aisha.muhammad@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Dr. Aisha Muhammad", "talent", "Nanotech Research Center"),
            ("hassan.ali@example.com", hashlib.sha256("password123".encode()).hexdigest(),
             "Hassan Ali", "talent", "Computer Vision Institute"),
        ]
        
        for user_data in users_data:
            cursor.execute('''
            INSERT INTO users (email, password_hash, name, user_type, organization)
            VALUES (?, ?, ?, ?, ?)
            ''', user_data)
            
        # Добавляем таланты
        talents_data = [
            (1, "Robotics Engineer", "Abu Dhabi", "3 years", "MSc Robotics",
             "Robotics,Computer Vision,Python,ROS,Arduino,MATLAB", "Part-time",
             "Specialized in designing robotic control systems for industrial automation and research applications. Experience with humanoid robots and collaborative robotics.", 
             150, "github.com/ahmed-robotics", "linkedin.com/in/ahmed-mansouri", 4.7),
            
            (2, "Data Scientist", "Abu Dhabi", "2 years", "MSc Computer Science",
             "Machine Learning,Python,TensorFlow,PyTorch,SQL,Tableau", "Full-time",
             "Expert in ML models and predictive analytics. Specialized in deep learning for financial forecasting and healthcare applications.", 
             120, "github.com/fatima-ml", "linkedin.com/in/fatima-zaabi", 4.5),
            
            (3, "Materials Scientist", "Al Ain", "5 years", "PhD Materials Science",
             "Materials Testing,Electron Microscopy,Thermal Analysis,X-ray Diffraction,Polymer Science", "Full-time",
             "Published researcher specializing in nanomaterials and advanced composites for aerospace applications. 15+ peer-reviewed publications.", 
             180, None, "linkedin.com/in/rashid-marzouqi", 4.9),
            
            (4, "Biotechnology Researcher", "Sharjah", "4 years", "PhD Biotechnology",
             "PCR,Cell Culture,Molecular Biology,Biochemistry,CRISPR,Bioinformatics", "Contract",
             "Expert in genetic engineering and molecular diagnostics. Developed rapid COVID-19 testing methods and working on cancer therapeutics.", 
             160, "researchgate.net/sara-hashemi", "linkedin.com/in/sara-hashemi", 4.8),
            
            (5, "AI Developer", "Abu Dhabi", "3 years", "MSc Artificial Intelligence",
             "Deep Learning,Computer Vision,TensorFlow,PyTorch,OpenCV,CUDA", "Remote",
             "Specialized in neural network architecture and computer vision for retail analytics and smart city applications.", 
             140, "github.com/mohammed-ai", "linkedin.com/in/mohammed-qasimi", 4.6),
            
            (6, "Drone Specialist", "Dubai", "2 years", "BSc Aerospace Engineering",
             "UAV Systems,Flight Control,Aerial Photography,Mapping,LiDAR,Photogrammetry", "Full-time",
             "Licensed drone pilot with expertise in autonomous flight systems and aerial surveying for construction and agriculture.", 
             110, "dronepilot.ae/layla", "linkedin.com/in/layla-shamsi", 4.4),
            
            (7, "IoT Solutions Architect", "Dubai", "6 years", "MSc Electrical Engineering",
             "IoT,Embedded Systems,C++,Python,MQTT,LoRaWAN,Edge Computing", "Full-time",
             "Designed and deployed large-scale IoT networks for smart buildings and industrial monitoring with 50+ successful projects.", 
             170, None, "linkedin.com/in/khalid-rahman", 4.8),
            
            (8, "Solar Energy Expert", "Abu Dhabi", "7 years", "PhD Renewable Energy",
             "Solar PV,Energy Storage,MATLAB,Homer Pro,Grid Integration,Energy Modeling", "Contract",
             "Leading expert in solar energy systems design and optimization for desert climates. Consulted on 10+ MW-scale projects.", 
             200, "solarexpert.ae/mariam", "linkedin.com/in/mariam-ali", 4.9),
            
            (9, "Autonomous Systems Engineer", "Dubai", "4 years", "MSc Mechatronics",
             "Self-Driving Cars,SLAM,ROS,C++,Sensor Fusion,Path Planning", "Full-time",
             "Specialized in autonomous navigation algorithms and sensor integration for self-driving vehicles in urban environments.", 
             155, "github.com/omar-autonomous", "linkedin.com/in/omar-hassan", 4.7),
            
            (10, "3D Printing Specialist", "Sharjah", "3 years", "BSc Mechanical Engineering",
             "3D Printing,CAD,SolidWorks,Fusion 360,Material Science,Rapid Prototyping", "Part-time",
             "Expert in additive manufacturing for aerospace and medical applications. Certified in metal and polymer 3D printing.", 
             130, "3dportfolio.ae/noura", "linkedin.com/in/noura-abdullah", 4.5),
            
            (11, "Quantum Computing Researcher", "Abu Dhabi", "5 years", "PhD Physics",
             "Quantum Algorithms,Qiskit,Python,Quantum Mechanics,Cryptography,Linear Algebra", "Remote",
             "Research scientist working on quantum computing applications for optimization and cryptography problems.", 
             220, "quantumresearch.ae/youssef", "linkedin.com/in/youssef-ibrahim", 4.9),
            
            (12, "Cybersecurity Analyst", "Dubai", "4 years", "MSc Information Security",
             "Penetration Testing,Network Security,Python,Ethical Hacking,SIEM,Forensics", "Full-time",
             "Certified ethical hacker with expertise in vulnerability assessment and security architecture for critical infrastructure.", 
             145, None, "linkedin.com/in/huda-salem", 4.6),
            
            (13, "Blockchain Developer", "Dubai", "3 years", "BSc Computer Science",
             "Solidity,Ethereum,Smart Contracts,Web3,JavaScript,Hyperledger", "Contract",
             "Developed DeFi applications and supply chain solutions on blockchain. Expert in smart contract security and optimization.", 
             135, "github.com/tariq-blockchain", "linkedin.com/in/tariq-ahmed", 4.5),
            
            (14, "Nanotechnology Researcher", "Al Ain", "6 years", "PhD Nanotechnology",
             "Nanomaterials,AFM,SEM,Chemical Synthesis,Drug Delivery,Characterization", "Full-time",
             "Leading researcher in nanomedicine and targeted drug delivery systems. 20+ publications in high-impact journals.", 
             190, "nanotech.ae/aisha", "linkedin.com/in/aisha-muhammad", 4.8),
            
            (15, "Computer Vision Engineer", "Abu Dhabi", "4 years", "MSc Computer Engineering",
             "Computer Vision,Deep Learning,OpenCV,Python,YOLO,Image Processing", "Remote",
             "Specialized in real-time object detection and tracking systems for surveillance and autonomous systems.", 
             150, "github.com/hassan-cv", "linkedin.com/in/hassan-ali", 4.7),
        ]
        
        cursor.executemany('''
        INSERT INTO talents (user_id, title, location, experience, education,
                           skills, availability, bio, hourly_rate, portfolio_url,
                           linkedin_url, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', talents_data)
        
        # Добавляем проекты
        projects_data = [
            ("Smart City Sensor Network Development", "Dubai Future Foundation", "Dubai",
             "2024-08-20", "2024-01-15", 
             "Looking for IoT experts to develop and test an urban sensor network for monitoring air quality, traffic, and noise pollution. The project aims to create a scalable infrastructure for UAE smart cities.",
             "Expertise in IoT sensor networks, data engineering, and embedded systems. Experience with LoRaWAN and edge computing preferred.",
             "IoT,Data Engineering,Embedded Systems,Smart City", 50000, 80000, "Active", "projects@dubaifuture.gov.ae", 145, 12),
            
            ("Advanced Materials Testing for Construction", "Al Futtaim Construction", "Abu Dhabi",
             "2024-07-25", "2024-01-18",
             "Need materials scientists to analyze new sustainable construction materials. Focus on thermal performance, durability, and structural integrity of novel cement composites.",
             "PhD in Materials Science or equivalent experience. Access to SEM, XRD, and thermal analysis equipment required.",
             "Materials Science,Construction,Testing,Sustainability", 30000, 45000, "Active", "materials@alfuttaim.ae", 89, 5),
            
            ("Drone Delivery System Testing", "Noon", "Dubai",
             "2024-09-15", "2024-01-20",
             "Seeking drone specialists to validate last-mile delivery systems in urban environments. Testing navigation algorithms, payload handling, and collision avoidance.",
             "Licensed drone pilot with experience in autonomous flight systems. Knowledge of UAE drone regulations essential.",
             "Drones,UAV,Logistics,Navigation", 60000, 90000, "Active", "innovation@noon.com", 234, 18),
            
            ("AI-Powered Patient Diagnosis System", "Mubadala Healthcare", "Abu Dhabi",
             "2024-04-10", "2023-11-05",
             "Developed AI system for early disease detection using patient data. Successfully improved diagnostic accuracy by 35% for common conditions.",
             "Machine learning expertise, healthcare domain knowledge, Python proficiency required.",
             "AI,Healthcare,Machine Learning,Medical", 80000, 120000, "Completed", "ai.health@mubadala.ae", 567, 32),
            
            ("Blockchain Supply Chain Platform", "DP World", "Dubai",
             "2024-10-01", "2024-01-25",
             "Building a blockchain-based supply chain tracking system for port operations. Need blockchain developers and logistics experts.",
             "Solidity, smart contract development, supply chain knowledge. Experience with Hyperledger preferred.",
             "Blockchain,Supply Chain,Smart Contracts,Logistics", 70000, 100000, "Active", "blockchain@dpworld.com", 156, 9),
            
            ("Solar Panel Efficiency Optimization", "Masdar", "Abu Dhabi",
             "2024-06-30", "2024-01-10",
             "Research project to improve solar panel efficiency in desert conditions. Testing new coating materials and cooling systems.",
             "PhD in Renewable Energy or Materials Science. Experience with solar PV systems and thermal management.",
             "Solar Energy,Materials Science,Research,Renewable", 40000, 65000, "Active", "research@masdar.ae", 98, 7),
            
            ("Autonomous Vehicle Testing Program", "RTA Dubai", "Dubai",
             "2024-12-01", "2024-02-01",
             "Large-scale testing of autonomous vehicles in Dubai. Need engineers for sensor calibration, route mapping, and safety validation.",
             "Experience with SLAM, sensor fusion, and autonomous navigation. ROS expertise required.",
             "Autonomous Vehicles,Robotics,AI,Transportation", 100000, 150000, "Active", "autonomous@rta.ae", 412, 24),
            
            ("Biotechnology Lab Equipment Validation", "Khalifa University", "Abu Dhabi",
             "2024-05-15", "2024-01-28",
             "Validating new biotechnology lab equipment for research facility. Need biotech experts for protocol development and testing.",
             "PhD in Biotechnology or related field. Experience with PCR, cell culture, and molecular biology techniques.",
             "Biotechnology,Research,Lab Equipment,Validation", 35000, 50000, "Active", "biotech@ku.ac.ae", 67, 4),
            
            ("Quantum Computing Research Initiative", "UAEU", "Al Ain",
             "2024-11-30", "2024-02-05",
             "Exploring quantum computing applications for cryptography and optimization. Seeking quantum computing researchers.",
             "PhD in Physics or Computer Science. Experience with quantum algorithms and Qiskit framework.",
             "Quantum Computing,Research,Cryptography,Physics", 90000, 130000, "Pending", "quantum@uaeu.ac.ae", 43, 2),
            
            ("3D Printing Medical Devices", "Cleveland Clinic Abu Dhabi", "Abu Dhabi",
             "2024-07-01", "2024-01-22",
             "Developing custom medical implants using 3D printing. Need specialists in biocompatible materials and CAD design.",
             "Experience with medical-grade 3D printing, CAD software, and biocompatible materials.",
             "3D Printing,Medical Devices,CAD,Healthcare", 55000, 75000, "Active", "3dmedical@clevelandclinic.ae", 123, 8),
            
            ("Cybersecurity Audit for Banking System", "Emirates NBD", "Dubai",
             "2024-04-30", "2024-01-30",
             "Comprehensive security audit of banking infrastructure. Need certified ethical hackers and security analysts.",
             "CISSP or CEH certification required. Experience with financial systems security.",
             "Cybersecurity,Banking,Security Audit,Penetration Testing", 65000, 95000, "Active", "security@emiratesnbd.com", 189, 11),
            
            ("Nanotechnology Water Purification", "DEWA", "Dubai",
             "2024-08-15", "2024-02-03",
             "Developing nanomaterial-based water purification systems. Research focus on removing microplastics and heavy metals.",
             "PhD in Nanotechnology or Chemistry. Experience with water treatment and nanomaterial synthesis.",
             "Nanotechnology,Water Treatment,Research,Environmental", 50000, 70000, "Active", "nanotech@dewa.gov.ae", 76, 5),
            
            ("Computer Vision for Retail Analytics", "Majid Al Futtaim", "Dubai",
             "2024-06-15", "2024-01-25",
             "Implementing computer vision systems for customer behavior analysis and inventory management in retail stores.",
             "Deep learning expertise, experience with object detection and tracking. Python and TensorFlow required.",
             "Computer Vision,AI,Retail,Analytics", 45000, 65000, "Active", "tech@majidalfuttaim.com", 201, 15),
            
            ("IoT Smart Agriculture Platform", "Abu Dhabi Agriculture Authority", "Al Ain",
             "2024-09-30", "2024-02-07",
             "Building IoT platform for precision agriculture. Monitoring soil conditions, irrigation, and crop health.",
             "IoT development experience, knowledge of agriculture technology. LoRaWAN and sensor networks expertise.",
             "IoT,Agriculture,Sensors,Data Analytics", 40000, 60000, "Pending", "smartfarm@adaa.gov.ae", 54, 3),
            
            ("Renewable Energy Grid Integration", "TAQA", "Abu Dhabi",
             "2024-10-15", "2024-02-10",
             "Studying integration of renewable energy sources into existing power grid. Focus on stability and energy storage.",
             "Electrical Engineering background, experience with grid systems and energy storage solutions.",
             "Renewable Energy,Grid Systems,Energy Storage,Electrical Engineering", 60000, 85000, "Active", "renewable@taqa.com", 92, 6),
        ]
        
        cursor.executemany('''
        INSERT INTO projects (title, organization, location, deadline, posted,
                            description, requirements, tags, budget_min, budget_max,
                            status, contact, views, applications)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', projects_data)
        
        # Добавляем примеры бронирований
        bookings_data = [
            (1, 1, "2024-02-15", "2024-02-17", "Testing new robotic arm design", "Confirmed", 4500),
            (2, 3, "2024-02-20", "2024-02-20", "Drone delivery system testing", "Confirmed", 800),
            (3, 2, "2024-02-25", "2024-02-28", "Material analysis for aerospace project", "Pending", 3600),
            (4, 4, "2024-03-01", "2024-03-03", "Biotech equipment training", "Confirmed", 3300),
            (5, 5, "2024-03-05", "2024-03-06", "Computer vision algorithm testing", "Confirmed", 2800),
        ]
        
        cursor.executemany('''
        INSERT INTO bookings (user_id, lab_id, start_date, end_date, purpose, status, total_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', bookings_data)
        
        # Добавляем примеры отзывов
        reviews_data = [
            (1, "lab", 1, 5, "Excellent facilities and very helpful staff. The robotics equipment is top-notch!"),
            (2, "lab", 3, 5, "Perfect for drone testing. Large open space and great safety measures."),
            (3, "talent", 1, 5, "Ahmed is incredibly knowledgeable and helped us solve complex robotics challenges."),
            (4, "talent", 2, 4, "Fatima delivered great insights for our data analysis project."),
            (5, "lab", 5, 5, "State-of-the-art computer vision lab. GPU clusters performed excellently."),
            (1, "talent", 5, 5, "Mohammed's AI expertise was invaluable for our project."),
            (2, "lab", 2, 4, "Good materials testing facility, though booking process could be smoother."),
            (3, "talent", 3, 5, "Dr. Rashid's materials science knowledge is exceptional. Highly recommended!"),
        ]
        
        cursor.executemany('''
        INSERT INTO reviews (user_id, item_type, item_id, rating, comment)
        VALUES (?, ?, ?, ?, ?)
        ''', reviews_data)
        
        # Добавляем примеры уведомлений
        notifications_data = [
            (1, "Booking Confirmed", "Your booking for Khalifa University Robotics Lab has been confirmed for Feb 15-17.", "booking"),
            (2, "New Project Match", "A new project 'Drone Delivery System Testing' matches your skills.", "project"),
            (3, "Review Received", "You received a 5-star review for your recent work.", "review"),
            (4, "Booking Reminder", "Reminder: Your lab booking starts tomorrow at 9:00 AM.", "reminder"),
            (5, "New Talent Available", "A new Computer Vision Engineer joined the platform.", "talent"),
        ]
        
        cursor.executemany('''
        INSERT INTO notifications (user_id, title, message, type)
        VALUES (?, ?, ?, ?)
        ''', notifications_data)
        
        self.conn.commit()

# ==================== СТИЛИ ====================
def load_css():
    st.markdown("""
    <style>
        /* Основные стили */
        .main {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #ffffff;
        }
        
        /* Анимированный градиент для заголовков */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .gradient-text {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        
        /* Карточки с эффектом стекла */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Кнопки с градиентом */
        .gradient-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 50px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
        }
        
        .gradient-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
        }
        
        /* Навигация */
        .nav-container {
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .nav-item {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            margin: 0 0.5rem;
        }
        
        .nav-item:hover {
            color: white;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .nav-item.active {
            color: white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Статус бейджи */
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .status-active {
            background: rgba(52, 211, 153, 0.2);
            color: #34d399;
            border: 1px solid #34d399;
        }
        
        .status-pending {
            background: rgba(251, 191, 36, 0.2);
            color: #fbbf24;
            border: 1px solid #fbbf24;
        }
        
        .status-completed {
            background: rgba(96, 165, 250, 0.2);
            color: #60a5fa;
            border: 1px solid #60a5fa;
        }
        
        /* Теги */
        .skill-tag {
            background: rgba(139, 92, 246, 0.2);
            color: #a78bfa;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.85rem;
            margin: 0.2rem;
            display: inline-block;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }
        
        /* Анимация загрузки */
        .loading-dots {
            display: inline-block;
            position: relative;
            width: 80px;
            height: 20px;
        }
        
        .loading-dots div {
            position: absolute;
            top: 8px;
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: #667eea;
            animation-timing-function: cubic-bezier(0, 1, 1, 0);
        }
        
        .loading-dots div:nth-child(1) {
            left: 8px;
            animation: loading-dots1 0.6s infinite;
        }
        
        .loading-dots div:nth-child(2) {
            left: 32px;
            animation: loading-dots2 0.6s infinite;
        }
        
        .loading-dots div:nth-child(3) {
            left: 56px;
            animation: loading-dots2 0.6s infinite;
        }
        
        @keyframes loading-dots1 {
            0% { transform: scale(0); }
            100% { transform: scale(1); }
        }
        
        @keyframes loading-dots2 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(24px, 0); }
        }
        
        /* Метрики дашборда */
        .metric-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        /* Уведомления */
        .notification {
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }
        
        .notification.unread {
            background: rgba(59, 130, 246, 0.2);
        }
        
        /* Календарь */
        .calendar-day {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 0.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .calendar-day:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .calendar-day.booked {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid #ef4444;
        }
        
        .calendar-day.available {
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
        }
        
        /* Форма поиска */
        .search-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 50px;
            padding: 0.5rem 1.5rem;
            display: flex;
            align-items: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .search-input {
            background: transparent;
            border: none;
            color: white;
            width: 100%;
            outline: none;
            padding: 0.5rem;
        }
        
        /* Прогресс бар */
        .progress-bar {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            height: 10px;
            overflow: hidden;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        /* Рейтинг звезды */
        .rating-stars {
            color: #fbbf24;
            font-size: 1.2rem;
        }
        
        /* Тултипы */
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            background-color: rgba(0, 0, 0, 0.9);
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        /* Скроллбар */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== УТИЛИТЫ ====================
def st_rerun():
    """Совместимость с разными версиями Streamlit"""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

def create_rating_stars(rating: float) -> str:
    """Создание HTML для звезд рейтинга"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars_html = "★" * full_stars
    if half_star:
        stars_html += "☆"
    stars_html += "☆" * empty_stars
    
    return f'<span class="rating-stars">{stars_html}</span> {rating:.1f}'

# ==================== КОМПОНЕНТЫ ====================
class AuthManager:
    """Менеджер аутентификации"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def login(email: str, password: str, db: Database) -> Optional[Dict]:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT id, email, name, user_type, organization 
            FROM users 
            WHERE email = ? AND password_hash = ?
        """, (email, AuthManager.hash_password(password)))
        
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    
    @staticmethod
    def register(email: str, password: str, name: str, user_type: str, 
                organization: str, db: Database) -> bool:
        try:
            cursor = db.conn.cursor()
            cursor.execute("""
                INSERT INTO users (email, password_hash, name, user_type, organization)
                VALUES (?, ?, ?, ?, ?)
            """, (email, AuthManager.hash_password(password), name, user_type, organization))
            db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

class NotificationManager:
    """Менеджер уведомлений"""
    
    @staticmethod
    def create_notification(user_id: int, title: str, message: str, 
                          notification_type: str, db: Database):
        cursor = db.conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, message, notification_type))
        db.conn.commit()
    
    @staticmethod
    def get_unread_count(user_id: int, db: Database) -> int:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM notifications 
            WHERE user_id = ? AND is_read = FALSE
        """, (user_id,))
        return cursor.fetchone()[0]
    
    @staticmethod
    def get_notifications(user_id: int, db: Database, limit: int = 10):
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT * FROM notifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (user_id, limit))
        return cursor.fetchall()

# ==================== СТРАНИЦЫ ====================
def show_login_page(db: Database):
    """Страница входа и регистрации"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 3rem;">UAE Innovate Hub</h1>', 
                   unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.7);">Connect. Innovate. Test. Collaborate.</p>', 
                   unsafe_allow_html=True)
        
        # Добавим простую анимацию вместо Lottie
        st.markdown('''
        <div style="text-align: center; margin: 2rem 0;">
            <div class="loading-dots">
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
        '''.format(__version__, __author__, __email__, __linkedin__, __github__), unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password")
                
                col1, col2 = st.columns(2)
                with col1:
                    remember_me = st.checkbox("Remember me")
                with col2:
                    st.markdown('<a href="#" style="float: right; color: #667eea;">Forgot password?</a>', 
                               unsafe_allow_html=True)
                
                if st.form_submit_button("Login", use_container_width=True):
                    user = AuthManager.login(email, password, db)
                    if user:
                        st.session_state.user = user
                        st.success("Welcome back!")
                        st_rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            with st.form("register_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name")
                    email = st.text_input("Email")
                with col2:
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                
                user_type = st.selectbox("I am a", ["Company", "Talent", "University"])
                organization = st.text_input("Organization/University")
                
                terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                
                if st.form_submit_button("Create Account", use_container_width=True):
                    if password != confirm_password:
                        st.error("Passwords don't match")
                    elif not terms:
                        st.error("Please accept the terms")
                    else:
                        success = AuthManager.register(email, password, name, 
                                                     user_type.lower(), organization, db)
                        if success:
                            st.success("Account created! Please login.")
                        else:
                            st.error("Email already exists")
        
        # Авторство в футере страницы логина
        st.markdown("---")
        st.markdown('''
        <div style="text-align: center; color: rgba(255,255,255,0.4); margin-top: 3rem;">
            <p>Developed with ❤️ by <strong>Alisher Beisembekov</strong></p>
            <p style="font-size: 0.8rem;">UAE Innovate Hub © 2024</p>
        </div>
        ''', unsafe_allow_html=True)

def show_dashboard(db: Database):
    """Главная страница - дашборд"""
    
    st.markdown('<h1 class="gradient-text">Welcome to UAE Innovate Hub</h1>', unsafe_allow_html=True)
    
    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    
    cursor = db.conn.cursor()
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM labs")
        lab_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{lab_count}+</div>
            <div class="metric-label">Testing Labs</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        cursor.execute("SELECT COUNT(*) FROM talents")
        talent_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{talent_count}+</div>
            <div class="metric-label">Talents</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'Active'")
        project_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{project_count}</div>
            <div class="metric-label">Active Projects</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Confirmed'")
        booking_count = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{booking_count}</div>
            <div class="metric-label">Bookings</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Графики
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Booking Trends")
        # Создаем данные для графика
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        bookings = [5 + i//3 + (i%7)*2 for i in range(30)]
        
        fig = px.line(x=dates, y=bookings, 
                     labels={'x': 'Date', 'y': 'Bookings'},
                     line_shape='spline')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False,
            height=300
        )
        fig.update_traces(line_color='#667eea', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏢 Labs by Category")
        cursor.execute("SELECT specialty, COUNT(*) as count FROM labs GROUP BY specialty")
        lab_stats = cursor.fetchall()
        
        if lab_stats:
            categories = [row['specialty'] for row in lab_stats]
            counts = [row['count'] for row in lab_stats]
            
            fig = px.pie(values=counts, names=categories, hole=0.6)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=True,
                height=300
            )
            fig.update_traces(marker=dict(colors=['#667eea', '#764ba2', '#e73c7e', '#23a6d5']))
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Последние активности
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔔 Recent Activities")
        activities = [
            ("New lab added", "Khalifa University AI Lab", "2 hours ago", "🏢"),
            ("Project posted", "Smart City Sensor Development", "5 hours ago", "📋"),
            ("Talent joined", "Dr. Sarah Ahmed - IoT Expert", "1 day ago", "👤"),
            ("Booking confirmed", "Drone Testing Zone - 3 days", "2 days ago", "✅"),
        ]
        
        for activity in activities:
            st.markdown(f'''
            <div class="glass-card" style="padding: 1rem;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 1rem;">{activity[3]}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">{activity[0]}</div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{activity[1]}</div>
                    </div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">{activity[2]}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Футер с авторством
    st.markdown("---")
    st.markdown('''
    <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 2rem 0;">
        <p>UAE Innovate Hub © 2024 | Developed by <strong>Alisher Beisembekov</strong></p>
        <p style="font-size: 0.9rem;">Connecting UAE's innovation ecosystem</p>
    </div>
    ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🌟 Featured Labs")
        cursor.execute("SELECT * FROM labs ORDER BY rating DESC LIMIT 3")
        featured_labs = cursor.fetchall()
        
        for lab in featured_labs:
            st.markdown(f'''
            <div class="glass-card" style="padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: bold;">{lab['name']}</div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{lab['location']}</div>
                    </div>
                    <div>{create_rating_stars(lab['rating'])}</div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <span class="skill-tag">{lab['specialty']}</span>
                    <span style="color: #22c55e; margin-left: 1rem;">AED {lab['price_per_day']}/day</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

def show_labs_page(db: Database):
    """Страница лабораторий"""
    
    st.markdown('<h1 class="gradient-text">Testing Laboratories</h1>', unsafe_allow_html=True)
    
    # Поиск и фильтры
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search labs...", placeholder="Search by name, location, or specialty")
    
    with col2:
        sort_by = st.selectbox("Sort by", ["Rating", "Price", "Name", "Availability"])
    
    with col3:
        view_mode = st.radio("View", ["Grid", "List"], horizontal=True)
    
    # Фильтры в сайдбаре
    with st.sidebar:
        st.markdown("### 🔧 Filters")
        
        # Специальности
        cursor = db.conn.cursor()
        cursor.execute("SELECT DISTINCT specialty FROM labs")
        specialties = [row[0] for row in cursor.fetchall()]
        selected_specialties = st.multiselect("Specialty", specialties)
        
        # Локации
        cursor.execute("SELECT DISTINCT location FROM labs")
        locations = [row[0] for row in cursor.fetchall()]
        selected_locations = st.multiselect("Location", locations)
        
        # Ценовой диапазон
        price_range = st.slider("Price per day (AED)", 0, 5000, (0, 5000))
        
        # Рейтинг
        min_rating = st.slider("Minimum rating", 0.0, 5.0, 0.0, 0.5)
        
        # Доступность
        availability = st.date_input("Available from", datetime.now())
        
        # Информация об авторе в сайдбаре
        st.markdown("---")
        st.markdown('''
        <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 0.8rem;">
            <p>Developed by<br><strong>Alisher Beisembekov</strong></p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Построение SQL запроса
    query = "SELECT * FROM labs WHERE 1=1"
    params = []
    
    if search_query:
        query += " AND (name LIKE ? OR description LIKE ? OR equipment LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param, search_param, search_param])
    
    if selected_specialties:
        query += f" AND specialty IN ({','.join(['?']*len(selected_specialties))})"
        params.extend(selected_specialties)
    
    if selected_locations:
        query += f" AND location IN ({','.join(['?']*len(selected_locations))})"
        params.extend(selected_locations)
    
    query += " AND price_per_day BETWEEN ? AND ?"
    params.extend([price_range[0], price_range[1]])
    
    query += " AND rating >= ?"
    params.append(min_rating)
    
    # Сортировка
    if sort_by == "Rating":
        query += " ORDER BY rating DESC"
    elif sort_by == "Price":
        query += " ORDER BY price_per_day ASC"
    elif sort_by == "Name":
        query += " ORDER BY name ASC"
    else:
        query += " ORDER BY available_from ASC"
    
    cursor.execute(query, params)
    labs = cursor.fetchall()
    
    # Отображение результатов
    st.markdown(f"### Found {len(labs)} labs")
    
    if view_mode == "Grid":
        cols = st.columns(3)
        for idx, lab in enumerate(labs):
            with cols[idx % 3]:
                st.markdown(f'''
                <div class="glass-card">
                    <h4>{lab['name']}</h4>
                    <p style="color: rgba(255,255,255,0.7);">{lab['university']}</p>
                    <p>📍 {lab['location']}</p>
                    <div style="margin: 1rem 0;">
                        <span class="skill-tag">{lab['specialty']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span>{create_rating_stars(lab['rating'])}</span>
                        <span style="color: #22c55e;">AED {lab['price_per_day']}/day</span>
                    </div>
                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 1rem 0;">
                        {lab['description'][:100]}...
                    </p>
                </div>
                ''', unsafe_allow_html=True)
                
                if st.button("View Details", key=f"lab_{lab['id']}"):
                    st.session_state.selected_lab_id = lab['id']
                    st_rerun()
    else:
        # List view
        for lab in labs:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f'''
                <div class="glass-card">
                    <h4>{lab['name']}</h4>
                    <p style="color: rgba(255,255,255,0.7);">{lab['university']} • {lab['location']}</p>
                    <p style="color: rgba(255,255,255,0.6);">{lab['description']}</p>
                    <div style="margin-top: 0.5rem;">
                        {' '.join([f'<span class="skill-tag">{eq}</span>' for eq in lab['equipment'].split(',')[:3]])}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div style="text-align: center; padding: 1rem;">
                    <div>{create_rating_stars(lab['rating'])}</div>
                    <div style="color: #22c55e; font-size: 1.2rem; margin-top: 0.5rem;">
                        AED {lab['price_per_day']}/day
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                if st.button("Book Now", key=f"book_lab_{lab['id']}", use_container_width=True):
                    st.session_state.booking_lab_id = lab['id']
                    st_rerun()

def show_talents_page(db: Database):
    """Страница талантов"""
    
    st.markdown('<h1 class="gradient-text">Talent Pool</h1>', unsafe_allow_html=True)
    
    # Статистика талантов
    col1, col2, col3, col4 = st.columns(4)
    cursor = db.conn.cursor()
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM talents")
        total_talents = cursor.fetchone()[0]
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_talents}</div>
            <div class="metric-label">Total Talents</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        cursor.execute("SELECT AVG(rating) FROM talents")
        avg_rating = cursor.fetchone()[0] or 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f}⭐</div>
            <div class="metric-label">Average Rating</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        cursor.execute("SELECT COUNT(DISTINCT skills) FROM talents")
        skill_count = 50  # Примерное количество уникальных навыков
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{skill_count}+</div>
            <div class="metric-label">Skills Covered</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        cursor.execute("SELECT AVG(hourly_rate) FROM talents")
        avg_rate = cursor.fetchone()[0] or 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{int(avg_rate)} AED</div>
            <div class="metric-label">Avg. Hourly Rate</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Поиск и фильтры
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search talents...", 
                                    placeholder="Search by name, skills, title, or expertise")
    
    with col2:
        sort_option = st.selectbox("Sort by", 
                                  ["Best Match", "Rating", "Hourly Rate (Low to High)", 
                                   "Hourly Rate (High to Low)", "Experience"])
    
    # Расширенные фильтры
    with st.expander("🔧 Advanced Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Навыки
            cursor.execute("SELECT DISTINCT skills FROM talents")
            all_skills = []
            for row in cursor.fetchall():
                all_skills.extend([s.strip() for s in row[0].split(',')])
            unique_skills = sorted(list(set(all_skills)))[:20]  # Топ-20 навыков
            
            selected_skills = st.multiselect("Skills", unique_skills)
        
        with col2:
            # Локации
            cursor.execute("SELECT DISTINCT location FROM talents")
            locations = [row[0] for row in cursor.fetchall()]
            selected_locations = st.multiselect("Locations", locations)
        
        with col3:
            # Доступность
            availability_options = ["Full-time", "Part-time", "Contract", "Remote"]
            selected_availability = st.multiselect("Availability", availability_options)
        
        with col4:
            # Ценовой диапазон
            rate_range = st.slider("Hourly rate (AED)", 0, 500, (0, 500))
            
            # Минимальный рейтинг
            min_rating = st.slider("Min. rating", 0.0, 5.0, 0.0, 0.5)
    
    # Построение запроса
    query = """
    SELECT t.*, u.name, u.email 
    FROM talents t 
    JOIN users u ON t.user_id = u.id 
    WHERE 1=1
    """
    params = []
    
    if search_query:
        query += " AND (u.name LIKE ? OR t.title LIKE ? OR t.skills LIKE ? OR t.bio LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param] * 4)
    
    if selected_skills:
        skill_conditions = " OR ".join(["t.skills LIKE ?" for _ in selected_skills])
        query += f" AND ({skill_conditions})"
        params.extend([f"%{skill}%" for skill in selected_skills])
    
    if selected_locations:
        query += f" AND t.location IN ({','.join(['?']*len(selected_locations))})"
        params.extend(selected_locations)
    
    if selected_availability:
        query += f" AND t.availability IN ({','.join(['?']*len(selected_availability))})"
        params.extend(selected_availability)
    
    query += " AND t.hourly_rate BETWEEN ? AND ?"
    params.extend([rate_range[0], rate_range[1]])
    
    query += " AND t.rating >= ?"
    params.append(min_rating)
    
    # Сортировка
    if sort_option == "Rating":
        query += " ORDER BY t.rating DESC"
    elif sort_option == "Hourly Rate (Low to High)":
        query += " ORDER BY t.hourly_rate ASC"
    elif sort_option == "Hourly Rate (High to Low)":
        query += " ORDER BY t.hourly_rate DESC"
    elif sort_option == "Experience":
        query += " ORDER BY t.experience DESC"
    else:  # Best Match
        query += " ORDER BY t.rating DESC, t.hourly_rate ASC"
    
    cursor.execute(query, params)
    talents = cursor.fetchall()
    
    # Отображение результатов
    st.markdown(f"### Found {len(talents)} talents")
    
    # Переключатель вида
    view_mode = st.radio("View as:", ["Cards", "List", "Compact"], horizontal=True)
    
    if view_mode == "Cards":
        # Карточки талантов (по 2 в ряд)
        for i in range(0, len(talents), 2):
            col1, col2 = st.columns(2)
            
            for idx, col in enumerate([col1, col2]):
                if i + idx < len(talents):
                    talent = talents[i + idx]
                    with col:
                        st.markdown(f'''
                        <div class="glass-card">
                            <div style="display: flex; align-items: start;">
                                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea, #764ba2); 
                                            border-radius: 50%; margin-right: 1rem; flex-shrink: 0;">
                                    <div style="text-align: center; line-height: 80px; font-size: 2rem; font-weight: bold;">
                                        {talent['name'][0].upper()}
                                    </div>
                                </div>
                                <div style="flex: 1;">
                                    <h4>{talent['name']}</h4>
                                    <p style="color: #667eea; font-weight: 600;">{talent['title']}</p>
                                    <p>📍 {talent['location']} • {talent['experience']} • {talent['education']}</p>
                                    <p style="color: rgba(255,255,255,0.7); margin: 0.5rem 0; font-size: 0.9rem;">
                                        {talent['bio'][:150]}{'...' if len(talent['bio']) > 150 else ''}
                                    </p>
                                    <div style="margin: 0.5rem 0;">
                                        {' '.join([f'<span class="skill-tag">{skill.strip()}</span>' 
                                                 for skill in talent['skills'].split(',')[:5]])}
                                        {f'<span class="skill-tag">+{len(talent["skills"].split(",")) - 5} more</span>' 
                                         if len(talent["skills"].split(",")) > 5 else ''}
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                                        <div>
                                            {create_rating_stars(talent['rating'])}
                                            <span style="color: #22c55e; margin-left: 1rem;">AED {talent['hourly_rate']}/hr</span>
                                        </div>
                                        <span class="status-badge status-active">{talent['availability']}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("View Profile", key=f"view_talent_{talent['id']}"):
                                st.session_state.selected_talent_id = talent['id']
                                st.experimental_rerun()
                        with col_b:
                            if st.button("Quick Contact", key=f"contact_talent_{talent['id']}"):
                                st.session_state.contact_talent_id = talent['id']
                                st.experimental_rerun()
    
    elif view_mode == "List":
        # Детальный список
        for talent in talents:
            st.markdown(f'''
            <div class="glass-card">
                <div style="display: flex; gap: 2rem;">
                    <div style="flex: 1;">
                        <h3>{talent['name']} - {talent['title']}</h3>
                        <p>📍 {talent['location']} • 📚 {talent['education']} • 💼 {talent['experience']} experience</p>
                        <p style="color: rgba(255,255,255,0.8);">{talent['bio']}</p>
                        <div style="margin: 1rem 0;">
                            <strong>Skills:</strong> {talent['skills']}
                        </div>
                        {f'<div><strong>Portfolio:</strong> <a href="{talent["portfolio_url"]}" style="color: #667eea;">{talent["portfolio_url"]}</a></div>' 
                         if talent.get('portfolio_url') else ''}
                        {f'<div><strong>LinkedIn:</strong> <a href="{talent["linkedin_url"]}" style="color: #667eea;">{talent["linkedin_url"]}</a></div>' 
                         if talent.get('linkedin_url') else ''}
                    </div>
                    <div style="text-align: center; min-width: 200px;">
                        <div>{create_rating_stars(talent['rating'])}</div>
                        <div style="color: #22c55e; font-size: 1.5rem; margin: 1rem 0;">
                            AED {talent['hourly_rate']}/hour
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <span class="status-badge status-active">{talent['availability']}</span>
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("Full Profile", key=f"full_profile_{talent['id']}"):
                    st.session_state.selected_talent_id = talent['id']
                    st.experimental_rerun()
            with col2:
                if st.button("Contact Now", key=f"contact_now_{talent['id']}"):
                    st.session_state.contact_talent_id = talent['id']
                    st.experimental_rerun()
    
    else:  # Compact view
        # Компактная таблица
        for talent in talents:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{talent['name']}**  \n{talent['title']}")
            with col2:
                st.markdown(f"{talent['location']} • {talent['availability']}")
            with col3:
                st.markdown(create_rating_stars(talent['rating']))
            with col4:
                st.markdown(f"**AED {talent['hourly_rate']}/hr**")
            with col5:
                if st.button("→", key=f"compact_view_{talent['id']}"):
                    st.session_state.selected_talent_id = talent['id']
                    st.experimental_rerun()

def show_projects_page(db: Database):
    """Страница проектов"""
    
    st.markdown('<h1 class="gradient-text">Projects & Collaborations</h1>', unsafe_allow_html=True)
    
    # Кнопка создания проекта
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Post New Project", use_container_width=True):
            st.session_state.show_new_project_form = True
            st.experimental_rerun()
    
    # Табы
    tab1, tab2, tab3 = st.tabs(["🔥 Active Projects", "⏳ Pending", "✅ Completed"])
    
    with tab1:
        show_projects_by_status(db, "Active")
    
    with tab2:
        show_projects_by_status(db, "Pending")
    
    with tab3:
        show_projects_by_status(db, "Completed")

def show_projects_by_status(db: Database, status: str):
    """Отображение проектов по статусу"""
    
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT *, julianday(deadline) - julianday('now') as days_left 
        FROM projects 
        WHERE status = ? 
        ORDER BY posted DESC
    """, (status,))
    projects = cursor.fetchall()
    
    if not projects:
        st.info(f"No {status.lower()} projects at the moment.")
        return
    
    for project in projects:
        days_left = int(project['days_left']) if project['days_left'] else 0
        deadline_color = "#ef4444" if days_left < 7 else "#fbbf24" if days_left < 30 else "#22c55e"
        
        st.markdown(f'''
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3>{project['title']} 
                        <span class="status-badge status-{status.lower()}">{status}</span>
                    </h3>
                    <p style="color: #667eea; font-weight: 600;">{project['organization']}</p>
                    <p>📍 {project['location']} • 
                       <span style="color: {deadline_color};">⏰ {days_left} days left</span> • 
                       👁️ {project['views']} views • 
                       📝 {project['applications']} applications
                    </p>
                    <p style="color: rgba(255,255,255,0.7); margin: 1rem 0;">{project['description']}</p>
                    <div style="margin: 1rem 0;">
                        {' '.join([f'<span class="skill-tag">{tag}</span>' 
                                 for tag in project['tags'].split(',')])}
                    </div>
                </div>
                <div style="text-align: right; min-width: 200px;">
                    <div style="color: #22c55e; font-size: 1.2rem; font-weight: bold;">
                        AED {project['budget_min']:,} - {project['budget_max']:,}
                    </div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">
                        Posted {project['posted']}
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("View Details", key=f"view_project_{project['id']}"):
                # Увеличиваем счетчик просмотров
                cursor.execute("UPDATE projects SET views = views + 1 WHERE id = ?", 
                             (project['id'],))
                db.conn.commit()
                st.session_state.selected_project_id = project['id']
                st.experimental_rerun()
        
        with col2:
            if status == "Active" and st.button("Apply", key=f"apply_project_{project['id']}"):
                st.session_state.apply_project_id = project['id']
                st.experimental_rerun()

def show_profile_page(db: Database):
    """Страница профиля пользователя"""
    
    user = st.session_state.user
    
    st.markdown(f'<h1 class="gradient-text">My Profile</h1>', unsafe_allow_html=True)
    
    # Табы профиля
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "📅 Bookings", "🔔 Notifications", "⚙️ Settings"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Аватар
            st.markdown('''
            <div style="text-align: center;">
                <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #667eea, #764ba2); 
                            border-radius: 50%; margin: 0 auto;"></div>
                <h3 style="margin-top: 1rem;">{}</h3>
                <p style="color: rgba(255,255,255,0.7);">{}</p>
                <p>{}</p>
            </div>
            '''.format(user['name'], user['user_type'].title(), user['organization']), 
            unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Edit Profile")
            
            with st.form("edit_profile"):
                name = st.text_input("Name", value=user['name'])
                organization = st.text_input("Organization", value=user['organization'])
                bio = st.text_area("Bio", placeholder="Tell us about yourself...")
                
                if st.form_submit_button("Save Changes"):
                    cursor = db.conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET name = ?, organization = ? 
                        WHERE id = ?
                    """, (name, organization, user['id']))
                    db.conn.commit()
                    st.success("Profile updated!")
                    st.session_state.user['name'] = name
                    st.session_state.user['organization'] = organization
                    st.experimental_rerun()
    
    with tab2:
        st.markdown("### My Bookings")
        
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT b.*, l.name as lab_name, l.location, l.price_per_day
            FROM bookings b
            JOIN labs l ON b.lab_id = l.id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC
        """, (user['id'],))
        bookings = cursor.fetchall()
        
        if bookings:
            for booking in bookings:
                status_class = {
                    'Pending': 'status-pending',
                    'Confirmed': 'status-active',
                    'Cancelled': 'status-completed'
                }.get(booking['status'], '')
                
                st.markdown(f'''
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h4>{booking['lab_name']}</h4>
                            <p>📍 {booking['location']}</p>
                            <p>📅 {booking['start_date']} to {booking['end_date']}</p>
                            <p style="color: rgba(255,255,255,0.7);">{booking['purpose']}</p>
                        </div>
                        <div style="text-align: right;">
                            <span class="status-badge {status_class}">{booking['status']}</span>
                            <p style="color: #22c55e; font-size: 1.2rem; margin-top: 1rem;">
                                AED {booking['total_cost']:,}
                            </p>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No bookings yet.")
    
    with tab3:
        st.markdown("### Notifications")
        
        # Получаем уведомления
        notifications = NotificationManager.get_notifications(user['id'], db)
        
        if notifications:
            for notif in notifications:
                read_class = "" if notif['is_read'] else "unread"
                st.markdown(f'''
                <div class="notification {read_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h4>{notif['title']}</h4>
                            <p style="color: rgba(255,255,255,0.7);">{notif['message']}</p>
                        </div>
                        <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">
                            {notif['created_at']}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Отмечаем как прочитанное
                if not notif['is_read']:
                    cursor = db.conn.cursor()
                    cursor.execute("UPDATE notifications SET is_read = TRUE WHERE id = ?", 
                                 (notif['id'],))
                    db.conn.commit()
        else:
            st.info("No notifications.")
    
    with tab4:
        st.markdown("### Account Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Change Password")
            with st.form("change_password"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password"):
                    if new_password != confirm_password:
                        st.error("Passwords don't match")
                    else:
                        # Проверяем текущий пароль
                        cursor = db.conn.cursor()
                        cursor.execute("""
                            SELECT id FROM users 
                            WHERE id = ? AND password_hash = ?
                        """, (user['id'], AuthManager.hash_password(current_password)))
                        
                        if cursor.fetchone():
                            cursor.execute("""
                                UPDATE users 
                                SET password_hash = ? 
                                WHERE id = ?
                            """, (AuthManager.hash_password(new_password), user['id']))
                            db.conn.commit()
                            st.success("Password updated!")
                        else:
                            st.error("Current password is incorrect")
        
        with col2:
            st.markdown("#### Email Preferences")
            
            email_bookings = st.checkbox("Email me about booking confirmations", value=True)
            email_projects = st.checkbox("Email me about new projects", value=True)
            email_newsletter = st.checkbox("Subscribe to newsletter", value=False)
            
            if st.button("Save Email Preferences"):
                st.success("Preferences saved!")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("🚪 Logout"):
                del st.session_state.user
                st.experimental_rerun()
        
        with col2:
            if st.button("🗑️ Delete Account", type="secondary"):
                st.warning("This action cannot be undone!")
        
        # О платформе
        st.markdown("---")
        st.markdown('''
        <div class="glass-card">
            <h4>📱 About UAE Innovate Hub</h4>
            <p style="color: rgba(255,255,255,0.7);">
                UAE Innovate Hub is a comprehensive platform connecting companies, universities, and talented individuals 
                to accelerate innovation and research in the UAE.
            </p>
            <div style="margin-top: 1rem;">
                <p><strong>Version:</strong> {0}</p>
                <p><strong>Developer:</strong> {1}</p>
                <p><strong>Contact:</strong> <a href="mailto:{2}" style="color: #667eea;">{2}</a></p>
                <p><strong>LinkedIn:</strong> <a href="{3}" style="color: #667eea;">Alisher Beisembekov</a></p>
                <p><strong>GitHub:</strong> <a href="{4}" style="color: #667eea;">@alisherbeisembekov</a></p>
            </div>'''.format(__version__, __author__, __email__, __linkedin__, __github__), unsafe_allow_html=True)
        </div>
        ''', unsafe_allow_html=True)

# ==================== ГЛАВНОЕ ПРИЛОЖЕНИЕ ====================
def main():
    # Загружаем стили
    load_css()
    
    # Инициализация БД
    db = Database()
    db.seed_data()
    
    # Проверка аутентификации
    if 'user' not in st.session_state:
        show_login_page(db)
        return
    
    # Навигация
    st.markdown('''
    <div class="nav-container">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <h2 class="gradient-text" style="margin: 0;"> UAE Innovate Hub</h2>
                <div style="display: flex; gap: 1rem;">
    ''', unsafe_allow_html=True)
    
    # Меню навигации
    pages = {
        "Dashboard": "📊",
        "Labs": "🏢",
        "Talents": "👥",
        "Projects": "📋",
        "DSO Hub": "🌆",
        "Profile": "👤"
    }
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    cols = st.columns(len(pages) + 1)
    
    for idx, (page, icon) in enumerate(pages.items()):
        with cols[idx]:
            if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.experimental_rerun()
    
    # Уведомления
    with cols[-1]:
        unread_count = NotificationManager.get_unread_count(st.session_state.user['id'], db)
        notif_label = f"🔔 ({unread_count})" if unread_count > 0 else "🔔"
        if st.button(notif_label, key="notifications"):
            st.session_state.current_page = "Profile"
            st.experimental_rerun()
    
    st.markdown('''
                </div>
            </div>
            <div style="color: rgba(255,255,255,0.7);">
                Welcome, {} 👋
            </div>
        </div>
    </div>
    '''.format(st.session_state.user['name']), unsafe_allow_html=True)
    
    # Отображение выбранной страницы
    if st.session_state.current_page == "Dashboard":
        show_dashboard(db)
    elif st.session_state.current_page == "Labs":
        show_labs_page(db)
    elif st.session_state.current_page == "Talents":
        show_talents_page(db)
    elif st.session_state.current_page == "Projects":
        show_projects_page(db)
    elif st.session_state.current_page == "Profile":
        show_profile_page(db)
    elif st.session_state.current_page == "DSO Hub":
        show_dso_hub_page(db)

def show_dso_hub_page(db: Database):
    """Страница DSO Hub"""
    
    st.markdown('<h1 class="gradient-text">Dubai Silicon Oasis Testing Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.7); font-size: 1.2rem;">An open innovation ecosystem where companies can test and validate their technology in real-world environments</p>', unsafe_allow_html=True)
    
    # Главные кнопки
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Book Testing Slot", use_container_width=True):
            st.session_state.show_booking_form = True
            st.experimental_rerun()
    
    # Ключевые преимущества
    st.markdown("### 🌟 Key Benefits")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌆</div>
            <h4>Real Environment</h4>
            <p style="color: rgba(255,255,255,0.7);">Test in actual urban settings with real infrastructure</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👨‍💻</div>
            <h4>Technical Support</h4>
            <p style="color: rgba(255,255,255,0.7);">Access to technical expertise and support</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📱</div>
            <h4>Digital Infrastructure</h4>
            <p style="color: rgba(255,255,255,0.7);">High-speed connectivity and data analytics</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="glass-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h4>Fast Permitting</h4>
            <p style="color: rgba(255,255,255,0.7);">Simplified regulatory approvals for testing</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Тестовые зоны
    st.markdown("### 🏗️ Testing Zones")
    
    testing_zones = [
        {
            "name": "Drone Testing Field",
            "description": "30,000 sq.m outdoor facility for UAV testing",
            "features": ["Wind simulation", "GPS tracking", "Obstacle courses", "Safety nets"],
            "price": "AED 2,000/day",
            "icon": "🚁"
        },
        {
            "name": "Autonomous Vehicle Track",
            "description": "2.5 km test track with urban environment simulation",
            "features": ["Traffic scenarios", "Weather simulation", "5G connectivity", "Control center"],
            "price": "AED 5,000/day",
            "icon": "🚗"
        },
        {
            "name": "Smart City Testbed",
            "description": "Real urban environment for IoT and smart city solutions",
            "features": ["Sensor networks", "Data platform", "API access", "Edge computing"],
            "price": "AED 3,000/day",
            "icon": "🏙️"
        }
    ]
    
    for zone in testing_zones:
        st.markdown(f'''
        <div class="glass-card">
            <div style="display: flex; gap: 2rem;">
                <div style="font-size: 4rem;">{zone["icon"]}</div>
                <div style="flex: 1;">
                    <h3>{zone["name"]}</h3>
                    <p style="color: rgba(255,255,255,0.7);">{zone["description"]}</p>
                    <div style="margin: 1rem 0;">
                        {' '.join([f'<span class="skill-tag">{feature}</span>' for feature in zone["features"]])}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #22c55e; font-size: 1.2rem; font-weight: bold;">{zone["price"]}</span>
                        <button class="gradient-button">Book Now</button>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Success Stories
    st.markdown("### 🏆 Success Stories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="glass-card">
            <h4>🚁 M2M Factory - Drone Delivery</h4>
            <p style="color: rgba(255,255,255,0.7);">Tested autonomous drone delivery system, achieving 40% improved efficiency and regulatory approval for commercial operations.</p>
            <div style="margin-top: 1rem;">
                <span class="status-badge status-active">Commercial Deployment</span>
                <span class="status-badge status-completed">40% Efficiency Gain</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="glass-card">
            <h4>☀️ Enerwhere - Solar Innovation</h4>
            <p style="color: rgba(255,255,255,0.7);">Developed and tested new solar panel configurations, resulting in patent-pending design with 23% efficiency improvement.</p>
            <div style="margin-top: 1rem;">
                <span class="status-badge status-active">Patent Filed</span>
                <span class="status-badge status-completed">23% Better Performance</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Статистика
    st.markdown("---")
    st.markdown("### 📊 DSO Testing Hub Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">150+</div>
            <div class="metric-label">Companies Tested</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">50+</div>
            <div class="metric-label">Patents Filed</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">85%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">24/7</div>
            <div class="metric-label">Support Available</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # CTA Section
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); 
                border-radius: 16px; padding: 3rem; text-align: center; margin: 2rem 0;">
        <h2 class="gradient-text">Ready to Test Your Innovation?</h2>
        <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem; margin: 1rem 0;">
            Join the growing list of companies who have accelerated their product development at Dubai Silicon Oasis
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📞 Contact Us", use_container_width=True):
            st.info("Contact: innovation@dso.ae | +971 4 501 5000")

if __name__ == "__main__":
    main()
