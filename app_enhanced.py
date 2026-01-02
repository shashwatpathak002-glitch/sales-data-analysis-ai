"""Enhanced Sales Data Analysis - With Authentication & Data Storage"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from src.database import Database
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.forecasting_model import ForecastingModel

# Initialize database
db = Database()

# Configure Streamlit
st.set_page_config(
    page_title="Sales Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    :root {
        --primary-color: #00B4D8;
        --secondary-color: #0096C7;
        --bg-color: #F0F7FF;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0rem;
    }
    
    .stTabs [data-baseweb="tabs"] button {
        background-color: #E8F4F8;
        border-radius: 8px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .auth-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 30px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.page = "Login"

# Authentication Page
def auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1>📊 Sales Analytics Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:white; font-size:1.1em'>Smart Sales Forecasting & Analysis</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown("### Login to Your Account")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", use_container_width=True):
                success, user_id, message = db.login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        with tab2:
            st.markdown("### Create New Account")
            new_username = st.text_input("New Username", key="reg_user")
            new_email = st.text_input("Email Address", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = db.register_user(new_username, new_email, new_password)
                    if success:
                        st.success(message)
                        st.info("Please login with your new credentials")
                    else:
                        st.error(message)

# Main Dashboard
def main_dashboard():
    # Sidebar
    with st.sidebar:
        st.markdown(f"<h3>👤 {st.session_state.username}</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "Upload Data", "Analysis", "Forecast", "My Data", "Logout"]
        )
        
        if page == "Logout":
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
        
        return page
    
    # Header
    st.markdown("<h1>📊 Sales Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = main_dashboard_navigation()
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Upload Data":
        show_upload()
    elif page == "Analysis":
        show_analysis()
    elif page == "Forecast":
        show_forecast()
    elif page == "My Data":
        show_user_data()

def main_dashboard_navigation():
    with st.sidebar:
        return st.radio(
            "Navigation",
            ["Dashboard", "Upload Data", "Analysis", "Forecast", "My Data", "Logout"],
            key="nav"
        )

def show_dashboard():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Total Uploads", "5", "+2")
    with col2:
        st.metric("📈 Analysis Done", "12", "+3")
    with col3:
        st.metric("🔮 Forecasts", "8", "+1")
    
    st.markdown("---")
    st.markdown("### Welcome to Your Sales Analytics Dashboard")
    st.write("""
    This platform helps you:
    - 📥 Upload and manage sales data
    - 📈 Perform exploratory data analysis
    - 🔮 Generate accurate sales forecasts
    - 📊 Track trends and patterns
    """)

def show_upload():
    st.markdown("### 📥 Upload Your Sales Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"File loaded! Shape: {df.shape}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df.head(10))
            with col2:
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")
                st.write(f"Data Types: {df.dtypes.to_dict()}")
            
            if st.button("Save Data", use_container_width=True):
                success, message, data_id = db.save_user_data(
                    st.session_state.user_id,
                    uploaded_file.name,
                    df
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"Error: {str(e)}")

def show_analysis():
    st.markdown("### 📈 Data Analysis")
    st.info("Upload data first to see analysis")

def show_forecast():
    st.markdown("### 🔮 Sales Forecasting")
    st.info("Upload data first to generate forecasts")

def show_user_data():
    st.markdown("### 📤 My Uploads")
    user_data = db.get_user_data(st.session_state.user_id)
    
    if user_data:
        for item in user_data:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📄 {item['filename']} - {item['upload_date']}")
            with col2:
                if st.button("Delete", key=item['id']):
                    db.delete_user_data(st.session_state.user_id, item['id'])
                    st.rerun()
    else:
        st.info("No data uploaded yet")

# Main execution
if not st.session_state.logged_in:
    auth_page()
else:
    main_dashboard()
