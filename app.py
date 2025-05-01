import streamlit as st
import pandas as pd
import datetime
import json
import os
import random
from PIL import Image
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="LabConnect",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_type' not in st.session_state:
    st.session_state.user_type = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"


# Mock data functions (these would connect to a database in a real application)
def load_labs_data():
    return pd.DataFrame({
        'lab_id': range(1, 11),
        'name': [
            'BioGenetics Lab', 'Chemical Analysis Center', 'Molecular Research Hub',
            'Advanced Materials Testing', 'Medical Diagnostics Lab', 'Environmental Sciences Lab',
            'Pharmaceutical Testing Lab', 'Food Safety Research Center', 'Nanotechnology Lab',
            'Quantum Physics Research Center'
        ],
        'location': [
            'New York, NY', 'Boston, MA', 'San Francisco, CA', 'Chicago, IL', 'Houston, TX',
            'Seattle, WA', 'Austin, TX', 'Denver, CO', 'Atlanta, GA', 'Miami, FL'
        ],
        'specialization': [
            'Genetic Research', 'Chemical Analysis', 'Molecular Biology',
            'Materials Science', 'Medical Testing', 'Environmental Testing',
            'Pharmaceutical Research', 'Food Safety Testing', 'Nanotechnology',
            'Quantum Physics'
        ],
        'price_per_hour': [
            150, 120, 180, 200, 130,
            110, 160, 140, 220, 250
        ],
        'rating': [
            4.8, 4.5, 4.9, 4.7, 4.6,
            4.3, 4.7, 4.5, 4.8, 4.9
        ],
        'available': [
            True, True, True, False, True,
            True, False, True, True, True
        ],
        'image': [
            'lab1.jpg', 'lab2.jpg', 'lab3.jpg', 'lab4.jpg', 'lab5.jpg',
            'lab6.jpg', 'lab7.jpg', 'lab8.jpg', 'lab9.jpg', 'lab10.jpg'
        ],
        'description': [
            'State-of-the-art genetics research laboratory with advanced DNA sequencing capabilities.',
            'Full-service chemical analysis lab specializing in organic and inorganic compounds testing.',
            'Leading molecular biology research center with PCR, Western blot, and ELISA capabilities.',
            'Materials testing facility with SEM, TEM, and XRD equipment for detailed analysis.',
            'CLIA-certified medical diagnostics lab offering a wide range of clinical tests.',
            'Environmental testing lab specializing in water, soil, and air quality analysis.',
            'GMP-compliant pharmaceutical testing lab with dissolution and stability testing services.',
            'ISO-certified food safety testing lab with microbiological and chemical testing capabilities.',
            'Advanced nanotechnology research facility with clean room and atomic manipulation tools.',
            'Quantum physics research center with superconducting quantum computers and cryogenics.'
        ],
        'services': [
            ['DNA Sequencing', 'PCR Analysis', 'Genetic Mapping'],
            ['Elemental Analysis', 'Chromatography', 'Spectroscopy'],
            ['ELISA', 'Protein Purification', 'Cell Culture'],
            ['Mechanical Testing', 'Thermal Analysis', 'Microscopy'],
            ['Blood Tests', 'Urinalysis', 'Microbiology'],
            ['Water Quality Testing', 'Soil Analysis', 'Air Quality Testing'],
            ['Dissolution Testing', 'Stability Studies', 'Method Development'],
            ['Microbiological Testing', 'Allergen Testing', 'Nutritional Analysis'],
            ['SEM Imaging', 'Nanofabrication', 'Particle Size Analysis'],
            ['Quantum Computing', 'Low Temperature Physics', 'Quantum Entanglement Studies']
        ],
        'equipment': [
            ['Illumina NextSeq', 'Thermal Cyclers', 'DNA Extractors'],
            ['HPLC', 'GC-MS', 'ICP-MS'],
            ['Flow Cytometer', 'Confocal Microscope', 'Real-time PCR'],
            ['Tensile Tester', 'SEM', 'DSC'],
            ['Blood Analyzers', 'Microbiology Incubators', 'Centrifuges'],
            ['ICP-OES', 'Gas Analyzers', 'Particle Counters'],
            ['Dissolution Testers', 'HPLC Systems', 'Stability Chambers'],
            ['PCR Systems', 'ELISA Readers', 'Microbiological Analyzers'],
            ['AFM', 'SEM', 'TEM'],
            ['Quantum Computers', 'Cryostats', 'Particle Detectors']
        ]
    })


def load_talents_data():
    return pd.DataFrame({
        'talent_id': range(1, 11),
        'name': [
            'Dr. Sarah Johnson', 'Dr. Michael Chen', 'Dr. Emily Rodriguez',
            'Dr. David Kim', 'Dr. Olivia Taylor', 'Dr. James Wilson',
            'Dr. Sophia Patel', 'Dr. Robert Garcia', 'Dr. Ava Thompson',
            'Dr. William Brown'
        ],
        'specialization': [
            'Molecular Biology', 'Analytical Chemistry', 'Microbiology',
            'Materials Science', 'Biochemistry', 'Environmental Science',
            'Pharmaceutical Sciences', 'Food Science', 'Nanotechnology',
            'Quantum Physics'
        ],
        'experience_years': [
            12, 8, 15, 10, 7,
            20, 9, 14, 6, 25
        ],
        'education': [
            'Ph.D. Harvard University', 'Ph.D. MIT', 'Ph.D. Stanford University',
            'Ph.D. Caltech', 'Ph.D. UC Berkeley', 'Ph.D. Princeton University',
            'Ph.D. Columbia University', 'Ph.D. University of Chicago', 'Ph.D. Yale University',
            'Ph.D. Cornell University'
        ],
        'rating': [
            4.9, 4.7, 4.8, 4.6, 4.5,
            4.9, 4.6, 4.7, 4.5, 4.8
        ],
        'hourly_rate': [
            95, 85, 100, 90, 80,
            110, 85, 95, 75, 120
        ],
        'available': [
            True, True, False, True, True,
            False, True, True, True, True
        ],
        'image': [
            'talent1.jpg', 'talent2.jpg', 'talent3.jpg', 'talent4.jpg', 'talent5.jpg',
            'talent6.jpg', 'talent7.jpg', 'talent8.jpg', 'talent9.jpg', 'talent10.jpg'
        ],
        'skills': [
            ['PCR', 'DNA Sequencing', 'Cell Culture', 'CRISPR'],
            ['HPLC', 'GC-MS', 'Spectroscopy', 'Method Development'],
            ['Bacterial Culture', 'Aseptic Technique', 'Antibiotic Resistance Testing', 'PCR'],
            ['SEM', 'XRD', 'Mechanical Testing', 'Materials Characterization'],
            ['Protein Purification', 'Enzyme Kinetics', 'Western Blotting', 'ELISA'],
            ['Environmental Sampling', 'Water Analysis', 'Soil Testing', 'GIS'],
            ['Drug Formulation', 'Stability Testing', 'Dissolution Studies', 'HPLC'],
            ['Food Analysis', 'Sensory Evaluation', 'Microbial Testing', 'Nutritional Analysis'],
            ['AFM', 'SEM', 'Nanofabrication', 'Particle Size Analysis'],
            ['Quantum Computing', 'Cryogenics', 'Laser Spectroscopy', 'Mathematical Modeling']
        ],
        'publications': [
            8, 5, 12, 7, 4,
            15, 6, 10, 3, 20
        ],
        'bio': [
            'Experienced molecular biologist specializing in genetic engineering and CRISPR technology.',
            'Analytical chemist with expertise in developing novel methods for complex sample analysis.',
            'Microbiologist focusing on antibiotic resistance mechanisms in pathogenic bacteria.',
            'Materials scientist specializing in the development and characterization of advanced composites.',
            'Biochemist with expertise in protein structure-function relationships and drug discovery.',
            'Environmental scientist specializing in the impact of industrial pollutants on aquatic ecosystems.',
            'Pharmaceutical scientist with expertise in controlled drug delivery systems.',
            'Food scientist specializing in food safety, quality control, and product development.',
            'Nanotechnology specialist focusing on the development of nanomaterials for biomedical applications.',
            'Quantum physicist with expertise in quantum computing algorithms and applications.'
        ]
    })


def load_bookings_data():
    # In a real application, this would be stored in a database
    if not os.path.exists('bookings.json'):
        return []

    try:
        with open('bookings.json', 'r') as f:
            return json.load(f)
    except:
        return []


def save_booking(booking):
    bookings = load_bookings_data()
    booking['booking_id'] = len(bookings) + 1
    bookings.append(booking)

    with open('bookings.json', 'w') as f:
        json.dump(bookings, f)


def load_job_listings():
    # In a real application, this would be stored in a database
    if not os.path.exists('job_listings.json'):
        return []

    try:
        with open('job_listings.json', 'r') as f:
            return json.load(f)
    except:
        return []


def save_job_listing(job):
    jobs = load_job_listings()
    job['job_id'] = len(jobs) + 1
    job['date_posted'] = datetime.datetime.now().strftime("%Y-%m-%d")
    job['status'] = 'Open'
    jobs.append(job)

    with open('job_listings.json', 'w') as f:
        json.dump(jobs, f)


def load_service_offerings():
    # In a real application, this would be stored in a database
    if not os.path.exists('services.json'):
        return []

    try:
        with open('services.json', 'r') as f:
            return json.load(f)
    except:
        return []


def save_service_offering(service):
    services = load_service_offerings()
    service['service_id'] = len(services) + 1
    service['date_posted'] = datetime.datetime.now().strftime("%Y-%m-%d")
    services.append(service)

    with open('services.json', 'w') as f:
        json.dump(services, f)


def load_applications():
    # In a real application, this would be stored in a database
    if not os.path.exists('applications.json'):
        return []

    try:
        with open('applications.json', 'r') as f:
            return json.load(f)
    except:
        return []


def save_application(application):
    applications = load_applications()
    application['application_id'] = len(applications) + 1
    application['date_applied'] = datetime.datetime.now().strftime("%Y-%m-%d")
    application['status'] = 'Pending'
    applications.append(application)

    with open('applications.json', 'w') as f:
        json.dump(applications, f)


def get_placeholder_image(image_name, is_lab=True):
    """
    This function would normally return the actual image, but for this demonstration
    we'll return a placeholder. In a real application, these would be actual images
    stored in a database or file system.
    """
    if is_lab:
        return f"https://via.placeholder.com/300x200?text=Lab+Image"
    else:
        return f"https://via.placeholder.com/200x200?text=Profile+Image"


# Custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #34495e;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        background-color: white;
    }
    .highlight {
        background-color: #f1c40f;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
    }
    .btn-book {
        background-color: #2ecc71;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .btn-apply {
        background-color: #3498db;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .rating {
        color: #f39c12;
        font-weight: bold;
    }
    .detail-label {
        font-weight: bold;
        color: #7f8c8d;
    }
    .nav-link {
        text-decoration: none;
        color: #3498db;
        font-weight: bold;
    }
    .nav-link:hover {
        color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)


# Login functionality
def login_page():
    st.markdown("<h1 class='main-header'>LabConnect Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("Login as", ["Lab Owner", "Researcher", "Lab Talent"])

        if st.button("Login"):
            # In a real application, you would validate credentials against a database
            if username and password:  # Simple validation for demonstration
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_type = user_type
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

        if st.button("Register"):
            # In a real application, this would take you to a registration page
            st.info("In a real application, this would open a registration form.")
        st.markdown("</div>", unsafe_allow_html=True)


# Navigation sidebar
def show_sidebar():
    with st.sidebar:
        st.image("https://via.placeholder.com/150?text=LabConnect", width=150)
        st.title("LabConnect")
        st.markdown(f"Welcome, {st.session_state.username}")
        st.markdown(f"Logged in as: {st.session_state.user_type}")

        st.markdown("### Navigation")
        if st.button("Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        if st.button("Book Labs"):
            st.session_state.current_page = "Book Labs"
            st.rerun()
        if st.button("Find Testing Labs"):
            st.session_state.current_page = "Find Testing Labs"
            st.rerun()
        if st.button("Find Talents"):
            st.session_state.current_page = "Find Talents"
            st.rerun()
        if st.button("Hire Talents"):
            st.session_state.current_page = "Hire Talents"
            st.rerun()
        if st.button("Offer Lab Services"):
            st.session_state.current_page = "Offer Lab Services"
            st.rerun()
        if st.button("My Dashboard"):
            st.session_state.current_page = "Dashboard"
            st.rerun()

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.rerun()


# Home page
def home_page():
    st.markdown("<h1 class='main-header'>Welcome to LabConnect</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <p>LabConnect is your one-stop platform for all laboratory-related needs:</p>
    <ul>
        <li>Book laboratory spaces for your research and testing needs</li>
        <li>Find specialized testing laboratories for your samples</li>
        <li>Connect with talented researchers and lab specialists</li>
        <li>Post job opportunities and hire the right talent</li>
        <li>Offer your laboratory services to potential clients</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2 class='sub-header'>Featured Labs</h2>", unsafe_allow_html=True)
        labs_data = load_labs_data()
        featured_labs = labs_data.sample(3)

        for _, lab in featured_labs.iterrows():
            st.markdown(f"""
            <div class='card'>
                <h3>{lab['name']}</h3>
                <p><span class='detail-label'>Location:</span> {lab['location']}</p>
                <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
                <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(lab['rating'])} ({lab['rating']})</span></p>
                <a href='#' class='btn-book'>View Details</a>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h2 class='sub-header'>Featured Talents</h2>", unsafe_allow_html=True)
        talents_data = load_talents_data()
        featured_talents = talents_data.sample(3)

        for _, talent in featured_talents.iterrows():
            st.markdown(f"""
            <div class='card'>
                <h3>{talent['name']}</h3>
                <p><span class='detail-label'>Specialization:</span> {talent['specialization']}</p>
                <p><span class='detail-label'>Experience:</span> {talent['experience_years']} years</p>
                <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(talent['rating'])} ({talent['rating']})</span></p>
                <a href='#' class='btn-apply'>View Profile</a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-header'>How It Works</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h3>For Researchers</h3>
            <p>Find and book labs that match your research needs</p>
            <p>Connect with skilled lab professionals</p>
            <p>Get your samples tested at specialized facilities</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h3>For Lab Owners</h3>
            <p>List your laboratory spaces for booking</p>
            <p>Offer specialized testing services</p>
            <p>Maximize your lab's utilization and revenue</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h3>For Lab Professionals</h3>
            <p>Showcase your skills and experience</p>
            <p>Find research and lab positions</p>
            <p>Connect with labs and researchers worldwide</p>
        </div>
        """, unsafe_allow_html=True)


# Book Labs page
def book_labs_page():
    st.markdown("<h1 class='main-header'>Book Laboratory Spaces</h1>", unsafe_allow_html=True)

    # Filters
    st.markdown("<h2 class='sub-header'>Find the Perfect Lab for Your Needs</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        location_filter = st.selectbox("Location", ["All Locations", "New York, NY", "Boston, MA", "San Francisco, CA",
                                                    "Chicago, IL", "Houston, TX", "Seattle, WA", "Austin, TX",
                                                    "Denver, CO", "Atlanta, GA", "Miami, FL"])

    with col2:
        specialization_filter = st.selectbox("Specialization",
                                             ["All Specializations", "Genetic Research", "Chemical Analysis",
                                              "Molecular Biology", "Materials Science", "Medical Testing",
                                              "Environmental Testing", "Pharmaceutical Research",
                                              "Food Safety Testing", "Nanotechnology", "Quantum Physics"])

    with col3:
        price_range = st.slider("Price Range ($/hour)", 0, 300, (100, 200))

    with col4:
        availability_filter = st.checkbox("Show only available labs", value=True)

    # Load and filter labs data
    labs_data = load_labs_data()

    if location_filter != "All Locations":
        labs_data = labs_data[labs_data['location'] == location_filter]

    if specialization_filter != "All Specializations":
        labs_data = labs_data[labs_data['specialization'] == specialization_filter]

    labs_data = labs_data[(labs_data['price_per_hour'] >= price_range[0]) &
                          (labs_data['price_per_hour'] <= price_range[1])]

    if availability_filter:
        labs_data = labs_data[labs_data['available'] == True]

    # Display labs
    if len(labs_data) == 0:
        st.warning("No labs match your criteria. Please adjust your filters.")
    else:
        st.markdown(f"<p>Found {len(labs_data)} labs matching your criteria</p>", unsafe_allow_html=True)

        for i in range(0, len(labs_data), 2):
            col1, col2 = st.columns(2)

            if i < len(labs_data):
                lab = labs_data.iloc[i]
                with col1:
                    lab_card(lab)

            if i + 1 < len(labs_data):
                lab = labs_data.iloc[i + 1]
                with col2:
                    lab_card(lab)


def lab_card(lab):
    st.markdown(f"""
    <div class='card'>
        <h3>{lab['name']}</h3>
        <p><span class='detail-label'>Location:</span> {lab['location']}</p>
        <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
        <p><span class='detail-label'>Price:</span> ${lab['price_per_hour']}/hour</p>
        <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(lab['rating'])} ({lab['rating']})</span></p>
        <p><span class='detail-label'>Status:</span> {"Available" if lab['available'] else "Currently Booked"}</p>
    </div>
    """, unsafe_allow_html=True)

    if lab['available']:
        if st.button(f"Book {lab['name']}", key=f"book_{lab['lab_id']}"):
            st.session_state.selected_lab = lab
            st.session_state.current_page = "Lab Booking"
            st.rerun()

    if st.button(f"View Details for {lab['name']}", key=f"details_{lab['lab_id']}"):
        st.session_state.selected_lab = lab
        st.session_state.current_page = "Lab Details"
        st.rerun()


# Lab Details page
def lab_details_page():
    lab = st.session_state.selected_lab

    st.markdown(f"<h1 class='main-header'>{lab['name']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(get_placeholder_image(lab['image']), caption=lab['name'])

    with col2:
        st.markdown(f"""
        <div class='card'>
            <p>{lab['description']}</p>
            <p><span class='detail-label'>Location:</span> {lab['location']}</p>
            <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
            <p><span class='detail-label'>Price:</span> ${lab['price_per_hour']}/hour</p>
            <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(lab['rating'])} ({lab['rating']})</span></p>
            <p><span class='detail-label'>Status:</span> {"Available" if lab['available'] else "Currently Booked"}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-header'>Services Offered</h2>", unsafe_allow_html=True)

    services_list = ", ".join(lab['services'])
    st.markdown(f"""
    <div class='card'>
        <p>{services_list}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-header'>Equipment Available</h2>", unsafe_allow_html=True)

    equipment_list = ", ".join(lab['equipment'])
    st.markdown(f"""
    <div class='card'>
        <p>{equipment_list}</p>
    </div>
    """, unsafe_allow_html=True)

    if lab['available']:
        if st.button("Book This Lab"):
            st.session_state.current_page = "Lab Booking"
            st.rerun()

    if st.button("Back to Labs"):
        st.session_state.current_page = "Book Labs"
        st.rerun()


# Lab Booking page
def lab_booking_page():
    lab = st.session_state.selected_lab

    st.markdown(f"<h1 class='main-header'>Book {lab['name']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>Lab Details</h3>
            <p><span class='detail-label'>Name:</span> {lab['name']}</p>
            <p><span class='detail-label'>Location:</span> {lab['location']}</p>
            <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
            <p><span class='detail-label'>Price:</span> ${lab['price_per_hour']}/hour</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Booking Details</h3>", unsafe_allow_html=False)

        booking_date = st.date_input("Booking Date", datetime.datetime.now() + datetime.timedelta(days=1))

        start_time = st.time_input("Start Time", datetime.time(9, 0))
        end_time = st.time_input("End Time", datetime.time(17, 0))

        # Calculate total hours and cost
        start_datetime = datetime.datetime.combine(booking_date, start_time)
        end_datetime = datetime.datetime.combine(booking_date, end_time)
        duration_hours = (end_datetime - start_datetime).total_seconds() / 3600

        if duration_hours <= 0:
            st.error("End time must be after start time")
        else:
            total_cost = duration_hours * lab['price_per_hour']
            st.markdown(f"<p><span class='detail-label'>Duration:</span> {duration_hours:.2f} hours</p>",
                        unsafe_allow_html=True)
            st.markdown(f"<p><span class='detail-label'>Total Cost:</span> ${total_cost:.2f}</p>",
                        unsafe_allow_html=True)

        purpose = st.text_area("Purpose of Booking", height=100)
        special_requests = st.text_area("Special Requests (equipment, setup, etc.)", height=100)

        if st.button("Confirm Booking"):
            if duration_hours <= 0:
                st.error("End time must be after start time")
            elif not purpose:
                st.error("Please provide the purpose of your booking")
            else:
                booking = {
                    "lab_id": lab['lab_id'],
                    "lab_name": lab['name'],
                    "user": st.session_state.username,
                    "booking_date": booking_date.strftime("%Y-%m-%d"),
                    "start_time": start_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M"),
                    "duration_hours": duration_hours,
                    "total_cost": total_cost,
                    "purpose": purpose,
                    "special_requests": special_requests,
                    "status": "Confirmed"
                }

                save_booking(booking)
                st.success("Booking confirmed! You can view the details in your dashboard.")
                if st.button("Go to Dashboard"):
                    st.session_state.current_page = "Dashboard"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Cancel"):
        st.session_state.current_page = "Book Labs"
        st.rerun()


# Find Testing Labs page
def find_testing_labs_page():
    st.markdown("<h1 class='main-header'>Find Testing Labs</h1>", unsafe_allow_html=True)

    # Filters
    st.markdown("<h2 class='sub-header'>Find Specialized Testing Services</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        test_type = st.selectbox("Test Type", ["All Types", "DNA Analysis", "Chemical Analysis", "Materials Testing",
                                               "Food Safety Testing", "Environmental Testing", "Medical Testing",
                                               "Pharmaceutical Testing", "Structural Analysis", "Electronic Testing"])

    with col2:
        location_filter = st.selectbox("Location", ["All Locations", "New York, NY", "Boston, MA", "San Francisco, CA",
                                                    "Chicago, IL", "Houston, TX", "Seattle, WA", "Austin, TX",
                                                    "Denver, CO", "Atlanta, GA", "Miami, FL"])

    with col3:
        turnaround_time = st.selectbox("Turnaround Time",
                                       ["Any", "Same Day", "1-2 Days", "3-5 Days", "1 Week", "2+ Weeks"])

    # In a real application, this would query a database of testing services
    # For this demo, we'll use the labs data and filter based on their services
    labs_data = load_labs_data()
    testing_labs = []

    for _, lab in labs_data.iterrows():
        services_lower = [s.lower() for s in lab['services']]

        if test_type != "All Types":
            if test_type.lower() not in " ".join(services_lower):
                continue

        if location_filter != "All Locations":
            if lab['location'] != location_filter:
                continue

        # Add some random turnaround times for demonstration
        turnaround_options = ["Same Day", "1-2 Days", "3-5 Days", "1 Week", "2+ Weeks"]
        lab_turnaround = random.choice(turnaround_options)

        if turnaround_time != "Any":
            if lab_turnaround != turnaround_time:
                continue

        lab_copy = lab.copy()
        lab_copy['turnaround_time'] = lab_turnaround
        testing_labs.append(lab_copy)

    # Display testing labs
    if len(testing_labs) == 0:
        st.warning("No testing labs match your criteria. Please adjust your filters.")
    else:
        st.markdown(f"<p>Found {len(testing_labs)} testing labs matching your criteria</p>", unsafe_allow_html=True)

        for i in range(0, len(testing_labs), 2):
            col1, col2 = st.columns(2)

            if i < len(testing_labs):
                lab = testing_labs[i]
                with col1:
                    testing_lab_card(lab)

            if i + 1 < len(testing_labs):
                lab = testing_labs[i + 1]
                with col2:
                    testing_lab_card(lab)


def testing_lab_card(lab):
    services_list = ", ".join(lab['services'][:3])
    if len(lab['services']) > 3:
        services_list += ", and more..."

    st.markdown(f"""
    <div class='card'>
        <h3>{lab['name']}</h3>
        <p><span class='detail-label'>Location:</span> {lab['location']}</p>
        <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
        <p><span class='detail-label'>Testing Services:</span> {services_list}</p>
        <p><span class='detail-label'>Turnaround Time:</span> {lab['turnaround_time']}</p>
        <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(lab['rating'])} ({lab['rating']})</span></p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Request Quote from {lab['name']}", key=f"quote_{lab['lab_id']}"):
            st.session_state.selected_lab = lab
            st.session_state.current_page = "Testing Quote"
            st.rerun()

    with col2:
        if st.button(f"View Details for {lab['name']}", key=f"test_details_{lab['lab_id']}"):
            st.session_state.selected_lab = lab
            st.session_state.current_page = "Testing Lab Details"
            st.rerun()


# Testing Quote Request page
def testing_quote_page():
    lab = st.session_state.selected_lab

    st.markdown(f"<h1 class='main-header'>Request Testing Quote from {lab['name']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>Lab Details</h3>
            <p><span class='detail-label'>Name:</span> {lab['name']}</p>
            <p><span class='detail-label'>Location:</span> {lab['location']}</p>
            <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
            <p><span class='detail-label'>Turnaround Time:</span> {lab['turnaround_time']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Available Testing Services</h3>", unsafe_allow_html=False)
        for service in lab['services']:
            st.markdown(f"- {service}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Testing Request Details</h3>", unsafe_allow_html=False)

        test_type = st.selectbox("Test Type", lab['services'])
        sample_description = st.text_area("Sample Description", height=100)
        number_of_samples = st.number_input("Number of Samples", min_value=1, value=1)
        special_requests = st.text_area("Special Requirements or Instructions", height=100)

        required_by_date = st.date_input("Results Required By", datetime.datetime.now() + datetime.timedelta(days=7))

        contact_name = st.text_input("Contact Name", value=st.session_state.username)
        contact_email = st.text_input("Contact Email")
        contact_phone = st.text_input("Contact Phone")

        if st.button("Submit Testing Quote Request"):
            if not sample_description:
                st.error("Please provide a sample description")
            elif not contact_email:
                st.error("Please provide a contact email")
            else:
                # In a real application, this would be saved to a database and sent to the lab
                st.success(
                    "Your testing quote request has been submitted. The lab will contact you shortly with pricing information.")
                if st.button("Return to Testing Labs"):
                    st.session_state.current_page = "Find Testing Labs"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Cancel"):
        st.session_state.current_page = "Find Testing Labs"
        st.rerun()


# Testing Lab Details page
def testing_lab_details_page():
    lab = st.session_state.selected_lab

    st.markdown(f"<h1 class='main-header'>{lab['name']} - Testing Services</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(get_placeholder_image(lab['image']), caption=lab['name'])

    with col2:
        st.markdown(f"""
        <div class='card'>
            <p>{lab['description']}</p>
            <p><span class='detail-label'>Location:</span> {lab['location']}</p>
            <p><span class='detail-label'>Specialization:</span> {lab['specialization']}</p>
            <p><span class='detail-label'>Turnaround Time:</span> {lab['turnaround_time']}</p>
            <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(lab['rating'])} ({lab['rating']})</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-header'>Testing Services</h2>", unsafe_allow_html=True)

    for service in lab['services']:
        st.markdown(f"""
        <div class='card'>
            <h3>{service}</h3>
            <p>This is a detailed description of the {service.lower()} service offered by {lab['name']}. 
            In a real application, this would include detailed information about the testing methodology, 
            equipment used, detection limits, and pricing information.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-header'>Testing Equipment</h2>", unsafe_allow_html=True)

    equipment_list = ", ".join(lab['equipment'])
    st.markdown(f"""
    <div class='card'>
        <p>{equipment_list}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Request Testing Quote"):
        st.session_state.current_page = "Testing Quote"
        st.rerun()

    if st.button("Back to Testing Labs"):
        st.session_state.current_page = "Find Testing Labs"
        st.rerun()


# Find Talents page
def find_talents_page():
    st.markdown("<h1 class='main-header'>Find Lab Talents</h1>", unsafe_allow_html=True)

    # Filters
    st.markdown("<h2 class='sub-header'>Find Specialized Lab Professionals</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        specialization_filter = st.selectbox("Specialization",
                                             ["All Specializations", "Molecular Biology", "Analytical Chemistry",
                                              "Microbiology", "Materials Science", "Biochemistry",
                                              "Environmental Science", "Pharmaceutical Sciences",
                                              "Food Science", "Nanotechnology", "Quantum Physics"])

    with col2:
        min_experience = st.slider("Minimum Experience (years)", 0, 25, 3)

    with col3:
        rate_range = st.slider("Hourly Rate Range ($)", 0, 150, (50, 100))

    with col4:
        availability_filter = st.checkbox("Show only available talents", value=True)

    # Load and filter talents data
    talents_data = load_talents_data()

    if specialization_filter != "All Specializations":
        talents_data = talents_data[talents_data['specialization'] == specialization_filter]

    talents_data = talents_data[talents_data['experience_years'] >= min_experience]

    talents_data = talents_data[(talents_data['hourly_rate'] >= rate_range[0]) &
                                (talents_data['hourly_rate'] <= rate_range[1])]

    if availability_filter:
        talents_data = talents_data[talents_data['available'] == True]

    # Display talents
    if len(talents_data) == 0:
        st.warning("No talents match your criteria. Please adjust your filters.")
    else:
        st.markdown(f"<p>Found {len(talents_data)} talents matching your criteria</p>", unsafe_allow_html=True)

        for i in range(0, len(talents_data), 3):
            cols = st.columns(3)

            for j in range(3):
                if i + j < len(talents_data):
                    talent = talents_data.iloc[i + j]
                    with cols[j]:
                        talent_card(talent)


def talent_card(talent):
    skills_list = ", ".join(talent['skills'][:3])
    if len(talent['skills']) > 3:
        skills_list += ", and more..."

    st.markdown(f"""
    <div class='card'>
        <h3>{talent['name']}</h3>
        <p><span class='detail-label'>Specialization:</span> {talent['specialization']}</p>
        <p><span class='detail-label'>Experience:</span> {talent['experience_years']} years</p>
        <p><span class='detail-label'>Education:</span> {talent['education']}</p>
        <p><span class='detail-label'>Skills:</span> {skills_list}</p>
        <p><span class='detail-label'>Hourly Rate:</span> ${talent['hourly_rate']}</p>
        <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(talent['rating'])} ({talent['rating']})</span></p>
        <p><span class='detail-label'>Status:</span> {"Available" if talent['available'] else "Currently Booked"}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if talent['available']:
            if st.button(f"Hire {talent['name']}", key=f"hire_{talent['talent_id']}"):
                st.session_state.selected_talent = talent
                st.session_state.current_page = "Hire Talent"
                st.rerun()

    with col2:
        if st.button(f"View Profile of {talent['name']}", key=f"profile_{talent['talent_id']}"):
            st.session_state.selected_talent = talent
            st.session_state.current_page = "Talent Profile"
            st.rerun()

# Talent Profile page
def talent_profile_page():
    talent = st.session_state.selected_talent

    st.markdown(f"<h1 class='main-header'>{talent['name']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(get_placeholder_image(talent['image'], is_lab=False), caption=talent['name'])

        st.markdown(f"""
        <div class='card'>
            <h3>Contact Information</h3>
            <p>In a real application, contact information would be available after connecting or hiring.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
            <p>{talent['bio']}</p>
            <p><span class='detail-label'>Specialization:</span> {talent['specialization']}</p>
            <p><span class='detail-label'>Experience:</span> {talent['experience_years']} years</p>
            <p><span class='detail-label'>Education:</span> {talent['education']}</p>
            <p><span class='detail-label'>Publications:</span> {talent['publications']}</p>
            <p><span class='detail-label'>Hourly Rate:</span> ${talent['hourly_rate']}</p>
            <p><span class='detail-label'>Rating:</span> <span class='rating'>{'★' * int(talent['rating'])} ({talent['rating']})</span></p>
            <p><span class='detail-label'>Status:</span> {"Available for hire" if talent['available'] else "Currently unavailable"}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-header'>Skills & Expertise</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Technical Skills</h3>", unsafe_allow_html=False)
        for skill in talent['skills']:
            st.markdown(f"- {skill}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>Research Experience</h3>
            <p>In a real application, this section would contain detailed information about the talent's
            research experience, previous employment, and notable projects.</p>
        </div>
        """, unsafe_allow_html=True)

    if talent['available']:
        if st.button("Hire This Talent"):
            st.session_state.current_page = "Hire Talent"
            st.rerun()

    if st.button("Back to Talents"):
        st.session_state.current_page = "Find Talents"
        st.rerun()


# Hire Talent page
def hire_talent_page():
    talent = st.session_state.selected_talent

    st.markdown(f"<h1 class='main-header'>Hire {talent['name']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>Talent Details</h3>
            <p><span class='detail-label'>Name:</span> {talent['name']}</p>
            <p><span class='detail-label'>Specialization:</span> {talent['specialization']}</p>
            <p><span class='detail-label'>Experience:</span> {talent['experience_years']} years</p>
            <p><span class='detail-label'>Hourly Rate:</span> ${talent['hourly_rate']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Skills</h3>", unsafe_allow_html=False)
        for skill in talent['skills']:
            st.markdown(f"- {skill}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Project Details</h3>", unsafe_allow_html=False)

        project_title = st.text_input("Project Title")
        project_description = st.text_area("Project Description", height=100)

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.datetime.now() + datetime.timedelta(days=7))
        with col2:
            end_date = st.date_input("End Date", datetime.datetime.now() + datetime.timedelta(days=37))

        estimated_hours = st.number_input("Estimated Hours", min_value=1, value=40)
        total_cost = estimated_hours * talent['hourly_rate']
        st.markdown(f"<p><span class='detail-label'>Total Estimated Cost:</span> ${total_cost:.2f}</p>",
                    unsafe_allow_html=True)

        special_requirements = st.text_area("Special Requirements or Skills Needed", height=100)

        if st.button("Submit Hiring Request"):
            if not project_title:
                st.error("Please provide a project title")
            elif not project_description:
                st.error("Please provide a project description")
            elif end_date <= start_date:
                st.error("End date must be after start date")
            else:
                # In a real application, this would be saved to a database and sent to the talent
                st.success(
                    "Your hiring request has been submitted. The talent will be notified and can accept or decline the offer.")
                if st.button("Return to Talents"):
                    st.session_state.current_page = "Find Talents"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Cancel"):
        st.session_state.current_page = "Find Talents"
        st.rerun()


# Hire Talents page (job listings)
def hire_talents_page():
    st.markdown("<h1 class='main-header'>Post Job Opportunities</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Post a New Job", "Your Job Listings"])

    # Post a New Job tab
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2>Post a New Job Opportunity</h2>", unsafe_allow_html=False)

        job_title = st.text_input("Job Title")
        organization = st.text_input("Organization / Lab Name")
        location = st.text_input("Location")

        job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Temporary", "Internship"])

        experience_level = st.selectbox("Experience Level",
                                        ["Entry Level", "Mid Level", "Senior", "Principal", "Executive"])

        col1, col2 = st.columns(2)
        with col1:
            salary_min = st.number_input("Minimum Salary ($)", min_value=0, value=40000)
        with col2:
            salary_max = st.number_input("Maximum Salary ($)", min_value=0, value=80000)

        required_skills = st.text_area("Required Skills (comma separated)")
        job_description = st.text_area("Job Description", height=200)

        application_deadline = st.date_input("Application Deadline",
                                             datetime.datetime.now() + datetime.timedelta(days=30))

        if st.button("Post Job"):
            if not job_title:
                st.error("Please provide a job title")
            elif not organization:
                st.error("Please provide an organization name")
            elif not location:
                st.error("Please provide a location")
            elif not job_description:
                st.error("Please provide a job description")
            elif salary_max <= salary_min:
                st.error("Maximum salary must be greater than minimum salary")
            else:
                # Process skills into a list
                skills = [skill.strip() for skill in required_skills.split(",") if skill.strip()]

                job = {
                    "job_title": job_title,
                    "organization": organization,
                    "location": location,
                    "job_type": job_type,
                    "experience_level": experience_level,
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "required_skills": skills,
                    "job_description": job_description,
                    "application_deadline": application_deadline.strftime("%Y-%m-%d"),
                    "poster": st.session_state.username
                }

                save_job_listing(job)
                st.success("Job posted successfully!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Your Job Listings tab
    with tab2:
        job_listings = load_job_listings()

        # Filter to show only this user's job listings
        user_jobs = [job for job in job_listings if job.get('poster') == st.session_state.username]

        if not user_jobs:
            st.info("You haven't posted any job listings yet.")
        else:
            for job in user_jobs:
                st.markdown(f"""
                <div class='card'>
                    <h3>{job['job_title']}</h3>
                    <p><span class='detail-label'>Organization:</span> {job['organization']}</p>
                    <p><span class='detail-label'>Location:</span> {job['location']}</p>
                    <p><span class='detail-label'>Job Type:</span> {job['job_type']}</p>
                    <p><span class='detail-label'>Experience Level:</span> {job['experience_level']}</p>
                    <p><span class='detail-label'>Salary Range:</span> ${job['salary_min']} - ${job['salary_max']}</p>
                    <p><span class='detail-label'>Posted:</span> {job['date_posted']}</p>
                    <p><span class='detail-label'>Application Deadline:</span> {job['application_deadline']}</p>
                    <p><span class='detail-label'>Status:</span> {job['status']}</p>
                </div>
                """, unsafe_allow_html=True)

                # In a real application, there would be options to view applicants, edit, or delete the job listing


# Offer Lab Services page
def offer_lab_services_page():
    st.markdown("<h1 class='main-header'>Offer Lab Services</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Post a New Service", "Your Service Offerings"])

    # Post a New Service tab
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2>Post a New Lab Service</h2>", unsafe_allow_html=False)

        service_title = st.text_input("Service Title")
        lab_name = st.text_input("Lab / Organization Name")
        location = st.text_input("Location")

        service_category = st.selectbox("Service Category", [
            "Analytical Testing", "Material Characterization", "Microbiology Testing",
            "Genetic Analysis", "Environmental Testing", "Medical Testing",
            "Food Safety Testing", "Pharmaceutical Testing", "Prototype Development",
            "R&D Consulting", "Equipment Rental", "Training & Workshops"
        ])

        service_description = st.text_area("Service Description", height=200)

        col1, col2 = st.columns(2)
        with col1:
            pricing_model = st.selectbox("Pricing Model",
                                         ["Per Sample", "Per Hour", "Per Day", "Per Project", "Custom"])
        with col2:
            price_range = st.text_input("Price Range", "e.g., $100-200 per sample")

        equipment_used = st.text_area("Equipment / Technology Used")
        turnaround_time = st.text_input("Typical Turnaround Time", "e.g., 3-5 business days")

        accreditations = st.text_area("Accreditations / Certifications (if any)")

        if st.button("Post Service"):
            if not service_title:
                st.error("Please provide a service title")
            elif not lab_name:
                st.error("Please provide a lab name")
            elif not location:
                st.error("Please provide a location")
            elif not service_description:
                st.error("Please provide a service description")
            else:
                service = {
                    "service_title": service_title,
                    "lab_name": lab_name,
                    "location": location,
                    "service_category": service_category,
                    "service_description": service_description,
                    "pricing_model": pricing_model,
                    "price_range": price_range,
                    "equipment_used": equipment_used,
                    "turnaround_time": turnaround_time,
                    "accreditations": accreditations,
                    "provider": st.session_state.username
                }

                save_service_offering(service)
                st.success("Service offering posted successfully!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Your Service Offerings tab
    with tab2:
        service_offerings = load_service_offerings()

        # Filter to show only this user's service offerings
        user_services = [service for service in service_offerings if
                         service.get('provider') == st.session_state.username]

        if not user_services:
            st.info("You haven't posted any service offerings yet.")
        else:
            for service in user_services:
                st.markdown(f"""
                <div class='card'>
                    <h3>{service['service_title']}</h3>
                    <p><span class='detail-label'>Lab / Organization:</span> {service['lab_name']}</p>
                    <p><span class='detail-label'>Location:</span> {service['location']}</p>
                    <p><span class='detail-label'>Category:</span> {service['service_category']}</p>
                    <p><span class='detail-label'>Pricing:</span> {service['pricing_model']} - {service['price_range']}</p>
                    <p><span class='detail-label'>Turnaround Time:</span> {service['turnaround_time']}</p>
                    <p><span class='detail-label'>Posted:</span> {service['date_posted']}</p>
                </div>
                """, unsafe_allow_html=True)

                # In a real application, there would be options to view inquiries, edit, or delete the service offering


# Dashboard page
def dashboard_page():
    st.markdown("<h1 class='main-header'>My Dashboard</h1>", unsafe_allow_html=True)

    # Display different tabs based on user type
    if st.session_state.user_type == "Researcher":
        tab1, tab2, tab3 = st.tabs(["My Lab Bookings", "My Testing Requests", "My Hiring Requests"])

        # My Lab Bookings tab
        with tab1:
            bookings = load_bookings_data()
            user_bookings = [booking for booking in bookings if booking.get('user') == st.session_state.username]

            if not user_bookings:
                st.info("You don't have any lab bookings yet.")
            else:
                for booking in user_bookings:
                    st.markdown(f"""
                    <div class='card'>
                        <h3>{booking['lab_name']}</h3>
                        <p><span class='detail-label'>Booking Date:</span> {booking['booking_date']}</p>
                        <p><span class='detail-label'>Time:</span> {booking['start_time']} - {booking['end_time']}</p>
                        <p><span class='detail-label'>Duration:</span> {booking['duration_hours']:.2f} hours</p>
                        <p><span class='detail-label'>Total Cost:</span> ${booking['total_cost']:.2f}</p>
                        <p><span class='detail-label'>Status:</span> {booking['status']}</p>
                        <p><span class='detail-label'>Purpose:</span> {booking['purpose']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # My Testing Requests tab
        with tab2:
            st.info("In a real application, this tab would display your testing requests and their statuses.")

        # My Hiring Requests tab
        with tab3:
            st.info("In a real application, this tab would display your talent hiring requests and their statuses.")

    elif st.session_state.user_type == "Lab Owner":
        tab1, tab2 = st.tabs(["Lab Booking Requests", "Testing Service Requests"])

        # Lab Booking Requests tab
        with tab1:
            st.info("In a real application, this tab would display booking requests for your labs.")

        # Testing Service Requests tab
        with tab2:
            st.info("In a real application, this tab would display testing service requests for your lab.")

    elif st.session_state.user_type == "Lab Talent":
        tab1, tab2 = st.tabs(["Job Applications", "Hiring Requests"])

        # Job Applications tab
        with tab1:
            applications = load_applications()
            user_applications = [app for app in applications if app.get('applicant') == st.session_state.username]

            if not user_applications:
                st.info("You haven't applied to any jobs yet.")
            else:
                for app in user_applications:
                    st.markdown(f"""
                    <div class='card'>
                        <h3>{app['job_title']}</h3>
                        <p><span class='detail-label'>Organization:</span> {app['organization']}</p>
                        <p><span class='detail-label'>Applied On:</span> {app['date_applied']}</p>
                        <p><span class='detail-label'>Status:</span> {app['status']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Hiring Requests tab
        with tab2:
            st.info("In a real application, this tab would display direct hiring requests for your services.")


# Main application
def main():
    apply_custom_css()

    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        show_sidebar()

        # Display the appropriate page based on the current_page state
        if st.session_state.current_page == "Home":
            home_page()
        elif st.session_state.current_page == "Book Labs":
            book_labs_page()
        elif st.session_state.current_page == "Lab Details":
            lab_details_page()
        elif st.session_state.current_page == "Lab Booking":
            lab_booking_page()
        elif st.session_state.current_page == "Find Testing Labs":
            find_testing_labs_page()
        elif st.session_state.current_page == "Testing Lab Details":
            testing_lab_details_page()
        elif st.session_state.current_page == "Testing Quote":
            testing_quote_page()
        elif st.session_state.current_page == "Find Talents":
            find_talents_page()
        elif st.session_state.current_page == "Talent Profile":
            talent_profile_page()
        elif st.session_state.current_page == "Hire Talent":
            hire_talent_page()
        elif st.session_state.current_page == "Hire Talents":
            hire_talents_page()
        elif st.session_state.current_page == "Offer Lab Services":
            offer_lab_services_page()
        elif st.session_state.current_page == "Dashboard":
            dashboard_page()


if __name__ == "__main__":
    main()
