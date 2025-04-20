import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import client
from src.prediction import PredictPipeline
from src.summariser import Summariser
from src.utils import plot_pie_chart, plot_wordcloud
import base64
import os

# Utility: Convert image to base64
def img_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

# Load images in base64
favicon_path = "templates/img/hotelytics_favicon.png"
logo_path = "templates/img/hotelytics_logo.png"

favicon_base64 = img_to_base64(favicon_path)
logo_base64 = img_to_base64(logo_path)

# Page config with embedded base64 favicon
if favicon_base64:
    st.set_page_config(
        page_title="Hotelytics.ai",
        page_icon=f"data:image/png;base64,{favicon_base64}",
        layout="wide",
        initial_sidebar_state="expanded",
    )
else:
    st.set_page_config(
        page_title="Hotelytics.ai",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# Hide Streamlit default UI elements
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Poppins:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', 'Montserrat', sans-serif !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Show logo in sidebar if available
if logo_base64:
    st.sidebar.markdown(
        f'<img class="sidebar-img" src="data:image/png;base64,{logo_base64}" style="margin-bottom: 20px; width: 100%;">',
        unsafe_allow_html=True
    )



# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=["Home", "Analyze", "Predict"],
        icons=["house", "bar-chart", "activity"],
        default_index=["Home", "Analyze", "Predict"].index(default_tab),
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#eba718", "font-size": "22px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "padding": "8px 14px",
                "color": "#eba718",
                "font-weight": "normal",
            },
            "nav-link-selected": {
                "background-color": "#eba718",
                "color": "white",
                "font-weight": "600",
            },
        }
    )

st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.markdown("""
Welcome to Hotelytics.ai, an innovative platform designed to revolutionize how hotels understand and enhance guest experiences using AI.
""", unsafe_allow_html=True)

st.sidebar.header("What We Do:")
st.sidebar.markdown("""
Hotelytics.ai automates sentiment analysis of guest reviews, providing insights into satisfaction and areas for improvement.
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Main Page
if selected == "Home":
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: #ffffff;
                font-family: 'Poppins', sans-serif;
            }
                
            div.stMainBlockContainer.block-container.st-emotion-cache-t1wise.eht7o1d4 {
                background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent background */
                background-image: radial-gradient(circle, rgba(0, 0, 0, 0.2) 1px, transparent 1px);
                background-size: 10px 10px;  /* Adjusts the size of the dots */
            }

            .hero-title {
                font-size: 4rem;
                font-weight: 800;
                text-align: center;
                color: transparent;
                background: linear-gradient(45deg, #830402, #c81d04, #da4a04, #f48a06, #ea6504);
                background-size: 400% 400%;
                -webkit-background-clip: text;
                background-clip: text;
                margin-bottom: -25px;
                margin-top: -50px;
                animation: wavingGradient 5s ease infinite;
            }

            @keyframes wavingGradient {
                0% {
                    background-position: 0% 50%; /* Start from the left */
                }
                50% {
                    background-position: 100% 50%; /* Move to the right */
                }
                100% {
                    background-position: 0% 50%; /* Return to the start position */
                }
            }

            .hero-sub {
                text-align: center;
                color: #9ca3af;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }


            .cta-button {
                display: flex;
                justify-content: center;
                margin-bottom: 4rem;
            }

            .stButton {
                margin-top: 0px;
                margin-bottom: 20px;
                display: flex;
                justify-content: center;
                
            }

            .stButton > button {
                margin: 0 auto;
                width: 250px;
                background: linear-gradient(45deg, #830402, #c81d04, #da4a04, #f48a06, #ea6504);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 0.2rem 0.2rem;
                font-size: 1.5rem; 
                font-weight: 600; 
                transition: transform 1s ease, box-shadow 1s ease, background-position 1.2s ease;
                text-align: center;
                text-decoration: none; 
                display: inline-block;
                font-family: 'Poppins', sans-serif;
                background-size: 400% 400%;
                background-position: 0% 50%;
            }

            .stButton > button:hover {
                background-position: 100% 50%;
                transform: scale(1.05); /* Slight size increase on hover */
                box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2); /* Shadow on hover */
                background: linear-gradient(45deg, #830402, #c81d04, #da4a04, #f48a06, #ea6504);
            }

            .stButton p {
                font-size: 1.5rem;
                font-family: "Poppins", "Sans-serif";
                font-weight: 600;
                color: #ffffff;
            }


            .section-title {
                text-align: center;
                font-size: 1.8rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.7rem;
                margin-top: 3.5rem;
            }

            .card-container {
                display: flex;
                justify-content: center;
                gap: 2rem;
                flex-wrap: wrap;
                padding: 0 1rem;
            }

            .card {
                background: #0a0a0a;
                border: 1px solid #facc15;
                border-radius: 12px;
                padding: 1.5rem;
                max-width: 300px;
                min-height: 180px;
                transition: all 0.3s ease;
                font-weight: 600;
            }

            .card:hover {
                background-color: #eba718;
                border-color: #eba718;
            }

            .card:hover .sentiment {
                color: #1f2937;
            }

            .card:hover .review-text {
                color: #111827;
                font-weight: 600;
            }

            .sentiment {
                display: flex;
                align-items: center;
                font-weight: 700;
                color: #fbbf24;
                margin-bottom: 0.75rem;
                font-size: 1.05rem;
                transition: color 0.3s ease;
            }

            .sentiment i {
                margin-right: 0.5rem;
            }

            .review-text {
                color: #d1d5db;
                font-size: 0.95rem;
                line-height: 1.5;
                transition: color 0.3s ease;
            }
                
            
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero-title">Insights Now - Action Tomorrow</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI-Powered Sentiment Analysis for Smarter Hotel Decisions</div>', unsafe_allow_html=True)


    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    
    def render_home():
        if st.button("Try It Now »", key="cta"):
            st.session_state.page = "Predict"  # Update page state to 'Predict'

    # Function to render the Predict page
    def render_predict():
        client.single_sentiment_analyzer_snippet_view()
        st.markdown("""
            <style>
                .section-title{display: none;}  
                    
                .card-container{display: none;}
                    
                .card{display: none;}
                    
                .why-choose-container{display: none;}
            </style>
        """, unsafe_allow_html=True)

    
    # Main code to switch between pages
    if st.session_state.page == "Home":
        render_home()  

    elif st.session_state.page == "Predict":
        render_predict() 


    st.markdown('<div class="section-title">See It In Action</div>', unsafe_allow_html=True)
    st.markdown("""
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        </head>
        
        <div class="card-container">
            <div class="card">
                <div class="sentiment"><i class="fa fa-smile"></i> Positive</div>
                <div class="review-text">"Exceptional service and beautiful rooms. The staff went above and beyond to make our stay memorable!"</div>
            </div>
            <div class="card">
                <div class="sentiment"><i class="fa fa-meh"></i> Neutral</div>
                <div class="review-text">"Average experience. Room was clean but nothing special. Location was convenient."</div>
            </div>
            <div class="card">
                <div class="sentiment"><i class="fa fa-frown"></i> Negative</div>
                <div class="review-text">"Disappointed with the cleanliness. The bathroom needed renovation and the AC was noisy."</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif selected == "Analyze":
    client.bulk_sentiment_analyzer()

elif selected == "Predict":
    client.single_sentiment_analyzer()