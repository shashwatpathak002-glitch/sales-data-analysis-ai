"""Sales Data Analysis & Forecasting - Streamlit Web Application"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# Configure Streamlit
st.set_page_config(
    page_title="Sales Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 0rem 0rem;}
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Sales Data Analysis & Forecasting")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")
    page = st.radio(
        "Select Page",
        ["Home", "Data Upload", "EDA", "Forecasting", "About"]
    )

if page == "Home":
    st.header("Welcome to Sales Data Analysis Platform")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Features", "5+")
    with col2:
        st.metric("Analysis Methods", "10+")
    with col3:
        st.metric("Models", "Regression")
    
    st.markdown("""
    ### Key Features:
    - 📥 **Data Upload**: Upload your sales CSV data
    - 🧹 **Data Cleaning**: Handle missing values and outliers
    - 📈 **EDA**: Explore trends and patterns
    - 🔮 **Forecasting**: Predict future sales
    - 📊 **Visualization**: Interactive charts and graphs
    """)

elif page == "Data Upload":
    st.header("📥 Upload Sales Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"File loaded successfully! Shape: {df.shape}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Dataset Preview")
                st.dataframe(df.head(10))
            with col2:
                st.subheader("Dataset Info")
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")
                st.write(f"Columns: {', '.join(df.columns)}")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

elif page == "EDA":
    st.header("📈 Exploratory Data Analysis")
    st.info("Upload data first to see EDA visualizations")
    
elif page == "Forecasting":
    st.header("🔮 Sales Forecasting")
    st.info("Upload data first to generate forecasts")
    
elif page == "About":
    st.header("ℹ️ About This Project")
    st.markdown("""
    ### Sales Data Analysis & Forecasting
    
    **Project**: Data Science Portfolio Project
    **Author**: Shashwat Pathak
    **GitHub**: [Repository Link](https://github.com/shashwatpathak002-glitch/sales-data-analysis-ai)
    
    ### Technologies Used:
    - Python 3.8+
    - Streamlit
    - Pandas & NumPy
    - Scikit-learn
    - Plotly
    
    ### Contact:
    - LinkedIn: [shashwat-pathak-6b8ab3337](https://linkedin.com/in/shashwat-pathak-6b8ab3337/)
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>", unsafe_allow_html=True)
st.markdown("Built with ❤️ using Streamlit")
st.markdown("</p>", unsafe_allow_html=True)
