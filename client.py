import time
import pandas as pd
import streamlit as st

from src.prediction import PredictPipeline
from src.summariser import Summariser
from src.utils import plot_frequency_chart, plot_pie_chart1, plot_wordcloud1


@st.fragment
def visualize_data_1(data,pred):
    with st.container(height=500):
        st.markdown("## Uploaded Reviews")
        st.write(data.head(15))
    with st.container(height=500):
        plot_pie_chart1(pred["Sentiment"])
    with st.container(height=500):
        
        plot_frequency_chart(data)


def visualize_data_2(data,pred):
    
    with st.container(height=500):
        st.markdown("## Reviews with Sentiment")
        st.write(pred.head(15))
            
    with st.container(height=500):
        
        with st.container(height=500):
            
            positive_reviews = pred[pred['Sentiment'] == 'POSITIVE']
            plot_wordcloud1(positive_reviews,"Positive")
            
    with st.container(height=500):
        with st.container(height=500):
            negative_reviews = pred[pred['Sentiment'] == 'NEGATIVE']
            plot_wordcloud1(negative_reviews,"Negative")
            
    return pred


def stream_data(txt:str):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.02)




def summarizer_display(df):
    #css
    st.markdown("""
            <style>
                .centered-title {
                    font-size: 25px;
                    text-align: center;
                    margin-top: 20px;
                    margin-bottom: -50px;
                }
            
                </style>
            """, unsafe_allow_html=True)
    


    st.markdown("<h4 class='centered-title'>Choose summary parameters or click 'Generate Summary' for an overview.</h4>", unsafe_allow_html=True)
    selected_aspects = st.multiselect(
        "",
        ["Staff Quality", "Ambience", "Parking", "Transportation", "Internet", "Restaurant"], key="unique_multiselect_key"
    )

    if st.button("Generate Summary", key="unique_summary_button_key"):
        with st.spinner("Generating summary..."):
            summ = Summariser()
            summary_result = summ.summarize_reviews(df, selected_aspects)
            # st.session_state['summary_result'] = summary_result  # Save summary result to session state
            st.write("### Summary")
            st.write_stream(stream_data(summary_result))


        txt_file = summary_result
        
        # Generate a .txt file for download
        st.download_button(
            label="Download as TXT",
            data=txt_file,
            file_name="summary.txt",
            mime="text/plain"
        )

def bulk_sentiment_analyzer():
    st.markdown("""
    <style>
    button.st-emotion-cache-b0y9n5.em9zgd02 {
        color: #eba718;  /* Set text color to #eba718 by default */
        border: 2px solid black;  /* Set border to black for inactive state */
    }

    button.st-emotion-cache-b0y9n5.em9zgd02:hover,
    button.st-emotion-cache-b0y9n5.em9zgd02:focus,
    button.st-emotion-cache-b0y9n5.em9zgd02:active {
        border: 1.5px solid #eba718;  /* Set border to #eba718 on hover, focus, or active state */
        color: #eba718;  /* Set text color to #eba718 on hover, focus, or active state */
    }

                
    .bulk-sentiment-full-width {
        width: 100%;
        text-align: center;
        font-size: 70px;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        margin-top: 30px;
        line-height: 1.1;
        color: transparent;
        background: linear-gradient(45deg, #830402, #c81d04, #da4a04, #f48a06, #ea6504);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        background-clip: text;
        animation: wavingGradient 5s ease infinite;
    }

    @keyframes wavingGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .bulk-sentiment-line2 {
        margin-top: -10px;
    }

    .stFileUploader > section {
        font-size: 22px;
        font-family: "Poppins", sans-serif;    
        margin-top: 20px !important;
        height: 140px;
        padding: 10px 40px;
        position: relative;
        border-radius: 20px;
        border: 2px solid transparent;
        background:
            linear-gradient(#262730, #262730) padding-box,
            repeating-linear-gradient(
                45deg,
                #eba718,
                #eba718 10px,
                transparent 10px,
                transparent 15px
            ) border-box;   
    }

    span.st-emotion-cache-9ycgxx.e17y52ym3 {
        visibility: hidden;
        position: relative;
    }

    span.st-emotion-cache-9ycgxx.e17y52ym3::after {
        content: "Drop reviews here, get insights!";
        visibility: visible;
        position: absolute;
        left: 0;
        top: 0;
        width: 200%; /* Increased width */
        white-space: nowrap; /* Prevents wrapping */
        color: #eba718;
        font-family: "Poppins", sans-serif;
        font-size: 20px;
        font-weight: 500;
    }


    </style>

    <div class="bulk-sentiment-full-width">
        Accelerate your services<br><span class="bulk-sentiment-line2">one step forward</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; font-size: 2px; margin-top: 40px; margin-bottom: -50px;">
        <h3>Sentiment Analyzer</h3>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["csv"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Read the CSV file
        dataframe = pd.read_csv(uploaded_file)
        
        # Initialize the progress bar
        progress_text = "Operation in progress. Please wait."
        progress_bar = st.progress(0)
        progress_text_display = st.empty()
        progress_text_display.text(progress_text)
        
        # Simulate a multi-step process with progress updates
        steps = ["Loading model", "Predicting data", "Generating results"]
        num_steps = len(steps)

        # Step 1: Initialize pipeline (simulate loading model)
        time.sleep(1)  
        progress_bar.progress(1 / num_steps)
        progress_text_display.text(f"{steps[0]}...")

        pipeline = PredictPipeline()

        # Step 2: Predict data (simulate prediction)
        time.sleep(1)
        progress_bar.progress(2 / num_steps)
        progress_text_display.text(f"{steps[1]}...")

        pred = pipeline.predict_csv(dataframe)

        # Step 3: Display results
        time.sleep(1)
        progress_bar.progress(3 / num_steps)
        progress_text_display.text(f"{steps[2]}...")

        # Update progress bar to 100% completion
        progress_bar.progress(1.0)
        progress_text_display.text("Completed!")
        progress_bar.empty()

        # Display results
        daily, monthly = st.columns(2)
        with daily:
            visualize_data_1(dataframe, pred)
        with monthly:
            visualize_data_2(dataframe, pred)

        with st.container():
            summarizer_display(dataframe)


def single_sentiment_analyzer():
    col1 = st.container()
    with col1:
        st.markdown("""
        <style>
        
        .single-sentiment-full-width {
            width: 100%;
            text-align: center;
            font-size: 70px;
            font-family: 'Poppins', sans-serif;
            font-weight: 1000;
            margin-top: 0px;
            line-height: 1.1;
            color: transparent;
            background: linear-gradient(45deg, #830402, #c81d04, #da4a04, #f48a06, #ea6504);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            background-clip: text;
            animation: wavingGradient 5s ease infinite;
        }
                    
        @keyframes wavingGradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        .single-sentiment-sub-heading {
            width: 100%;
            text-align: center;
            font-size: 20px;
            font-family: 'Poppins', sans-serif;
            font-weight: 300;
            color: #9ca3af;
            margin-top: 20px;
        }

        .single-sentiment-line2 {
            margin-top: -10px;
        }

        .single-sentiment-container {
            line-height: 1.4;
            text-align: center;
            padding: 44px;
            color: #333;
        }

        h1 {
            font-size: 50px;
        }

        p {
            font-size: 18px;
        }

        p small {
            font-size: 80%;
            color: #666;
        }

        .single-sentiment-highlight-container, .single-sentiment-highlight {
            position: relative;
            font-weight: bold;
        }
        .single-sentiment-highlight{
            color: #000;
        }

        .single-sentiment-highlight-container {
            display: inline-block;
        }

        .single-sentiment-highlight-container:before {
            content: " ";
            display: block;
            height: 90%;
            width: 105%;
            margin-left: -1px;
            margin-right: -3px;
            position: absolute;
            background: #ffd500;
            transform: rotate(2deg);
            top: -1px;
            left: -1px;
            border-radius: 20% 25% 20% 24%;
            padding: 10px 3px 3px 10px;
        }

        /* New Predict Button Styling */
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
            transform: scale(1.05);
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
        }

        .stButton p {
            font-size: 1.5rem;
            font-family: "Poppins", "Sans-serif";
            font-weight: 600;
            color: #0e1117;
        }

        .single-sentiment-green-success {
            color: #007200;
            font-size: 30px;
            font-weight: bold;
            background-color: #96e072;
            border-left: 10px solid #007200;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
                
        .single-sentiment-red-success {
            color: #6a040f;
            font-size: 30px;
            font-weight: bold;
            background-color: #f8d7da;
            border-left: 10px solid #6a040f;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }

        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="single-sentiment-full-width">A smarter way to<br><span class="single-sentiment-line2">interpret your hotel reviews</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '''
            <div class="single-sentiment-sub-heading">Unlock Guest Insights for Better Service with 
                <span class="single-sentiment-highlight-container">
                    <span class="single-sentiment-highlight"> Hotelytics.ai</span>
                </span>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # Multiselector      
    col1, col2, col3 = st.columns([1, 3, 1], vertical_alignment="top")
    with col1:
        pass

    with col2:
        st.markdown("""
            <style>  
                label.st-emotion-cache-1weic72.e1gk92lc0 {
                    display: none !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
             
                .single-sentiment-centered-title {
                    font-size: 20px;
                    font-weight: 600;
                    font-family: 'Montserrat', sans-serif;
                    text-align: center;
                    margin-top: 50px;
                    margin-bottom: -10px !important; 
                }

                .single-sentiment-custom-textarea {
                    text-align: center;
                    margin-top: 0px;
                    margin-bottom: -50px;
                    width: 1080px;
                    height: 80px;
                    max-height: 100px;
                    border-radius: 25px;
                    border: 1px solid #d7ae19;
                    padding: 10px;
                    font-family: 'Montserrat', sans-serif;
                }

            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h4 class='single-sentiment-centered-title'>Enter a review to predict its sentiment</h4>", unsafe_allow_html=True)
        
        user_reviews = st.text_area(
            "", 
            placeholder="e.g: Amazing experience! From check-in to check-out, everything was seamless. The hotel is stylish, clean, and the customer service is exceptional. Highly recommend!", 
            height=80, 
            key="custom_textarea"
        )
    
        if st.button("Predict ➔"):
            if not user_reviews.strip():
                st.warning("Please enter a review before analyzing!")
            else:
                pred = PredictPipeline()
                sentiment = pred.predict_str(user_reviews)

                if sentiment == "POSITIVE":
                    st.markdown("""
                    <div class="single-sentiment-green-success">
                        POSITIVE ✅
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="single-sentiment-red-success">
                        NEGATIVE ❌
                    </div>
                    """, unsafe_allow_html=True)

    with col3:
        pass


def single_sentiment_analyzer_snippet_view():
    col1 = st.container()
    with col1:
        pass

    # Multiselector      
    col1, col2, col3 = st.columns([1, 3, 1], vertical_alignment="top")
    with col1:
        pass

    with col2:
        st.markdown("""
            <style>
                h4.single-sentiment-centered-title {
                    font-size: 22px;
                    text-align: center;
                    margin-top: 0px;
                    margin-bottom: 0px; 
                    font-family: 'Montserrat', sans-serif;
                }

                div[data-testid="stTextArea"] textarea {
                    width: 90vw !important;
                    max-width: 100% !important;
                    height: 80px !important;
                    border-radius: 10px !important;
                    border: 1px solid #0e1117 !important;
                    padding: 10px !important;
                    font-size: 16px;
                    font-family: 'Montserrat', sans-serif;
                    box-sizing: border-box;
                }

                button.st-emotion-cache-b0y9n5.em9zgd02 {
                    display: block;
                    margin: 15px auto 12px auto;
                    background: linear-gradient(45deg, #830402, #c81d04, #da4a04, #f48a06, #ea6504); /* Dynamic gradient */
                    color: white;
                    border: none;
                    border-radius: 10px; /* Updated border-radius */
                    padding: 10px 20px; /* Adjusted padding */
                    font-size: 22px; /* Updated font-size */
                    font-weight: 400;
                    font-family: 'Montserrat', sans-serif;
                    transition: transform 0.3s ease, background-position 0.3s ease; /* Add background-position transition */
                    text-align: center;
                    text-decoration: none;
                    background-size: 400% 400%; /* Make the gradient large enough to move */
                    background-position: 0% 50%; /* Start position of the gradient */
                }

                button.st-emotion-cache-b0y9n5.em9zgd02:hover {
                    background-position: 100% 50%; /* Change the gradient position on hover */
                    transform: scale(1.03); /* Slight size increase */
                    border: none; /* No border needed for hover */
                }

                button.st-emotion-cache-b0y9n5.em9zgd02 p {
                    font-size: 1.2rem;
                    font-family: 'Montserrat', sans-serif;
                    font-weight: 600;
                    color: #ffffff;
                    
                }
                    
                .single-sentiment-green-success {
                    color: #007200;
                    font-size: 30px;
                    font-weight: bold;
                    background-color: #96e072;
                    border-left: 10px solid #007200;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    font-family: 'Montserrat', sans-serif;
                }

                .single-sentiment-red-success {
                    color: #6a040f;
                    font-size: 30px;
                    font-weight: bold;
                    background-color: #f8d7da;
                    border-left: 10px solid #6a040f;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    font-family: 'Montserrat', sans-serif;
                }
                    

                .streamlit-expanderHeader {
                    max-width: 100%;
                }
                .custom-textarea textarea {
                    width: 150%;
                    min-width: 500px; 
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h4 class='single-sentiment-centered-title'>Enter a review to predict its sentiment</h4>", unsafe_allow_html=True)

        user_reviews = st.text_area(
            "",
            placeholder="e.g: Great hotel with top-notch service. Clean, stylish, and made our stay so enjoyable!",
            height=80,
            key="custom_textarea",
            label_visibility="collapsed" 

        )

        if st.button("Predict ➔"):
            if not user_reviews.strip():
                st.warning("Please enter a review before analyzing!")
            else:
                pred = PredictPipeline()
                sentiment = pred.predict_str(user_reviews)

                if sentiment == "POSITIVE":
                    st.markdown("""
                    <div class="single-sentiment-green-success">
                        POSITIVE ✅
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="single-sentiment-red-success">
                        NEGATIVE ❌
                    </div>
                    """, unsafe_allow_html=True)

    with col3:
        pass
