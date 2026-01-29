import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="MindGuard AI", layout="wide", page_icon="🧠")

# 2. Advanced CSS for a Modern Tech Look
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f4f7f9;
        color: #2c3e50;
    }

    /* Styled Containers (The Squares) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border-top: 8px solid #3498db !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        padding: 30px !important;
        height: 700px !important; /* Increased fixed height */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }

    /* Main Title Animation Look */
    .hero-title {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .hero-subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
    }

    /* Flashy Button Animation */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(231, 76, 60, 0); }
        100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
    }

    /* Modern & Striking Button */
    .stButton button {
        width: 100%;
        border-radius: 50px;
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        height: 4rem;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
    }
    
    /* Center the button in the middle column */
    div[data-testid="column"]:nth-of-type(2) .stButton {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px rgba(255, 75, 43, 0.4);
        animation: pulse-glow 1.5s infinite;
    }
    
    /* Bottom Info Section Styles */
    .bottom-info-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2ecc71;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
        height: 100%;
    }
    .bottom-info-title {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Model Loading
@st.cache_resource
def load_model():
    try:
        return joblib.load('modelo_burnout_pipeline.pkl')
    except:
        return None

model = load_model()
CRITICAL_WORDS = ['suicide', 'kill', 'burnout', 'exhausted', 'hopeless', 'quit', 'resign', 'death']
EXTRA_POINTS = 15

# --- HEADER ---
st.markdown('<h1 class="hero-title">MindGuard AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Decoding Workplace Stress through Linguistic Intelligence</p>', unsafe_allow_html=True)

# --- MAIN DASHBOARD (3-Column Layout) ---
# Use vertical_alignment="center" to align the button in the middle vertically
col_left, col_mid, col_right = st.columns([1, 0.2, 1], gap="medium", vertical_alignment="center")

with col_left:
    with st.container(border=True):
        st.markdown("### ✍️ Share Your Story")
        st.write("Describe your recent workplace feelings, workload, or general mood:")
        
        user_input = st.text_area(
            "input_text",
            height=350,
            placeholder="E.g., I've been feeling extremely drained lately, the deadlines are overwhelming and I feel unappreciated...",
            label_visibility="collapsed"
        )

# --- BUTTON IN MIDDLE COLUMN ---
with col_mid:
    # This button now sits between the two panels
    analyze_btn = st.button("Start Analysis")

with col_right:
    with st.container(border=True):
        st.markdown("### 📊 Insight Dashboard")
        
        if not analyze_btn:
            st.write("Waiting for your input to generate insights...")
            # Visual filler for symmetry
            st.markdown("""
                <div style='height: 350px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed #ecf0f1; border-radius: 10px; color: #bdc3c7;'>
                    <span style='font-size: 50px;'>🧠</span>
                    <p>Ready to analyze your text</p>
                </div>
            """, unsafe_allow_html=True)
        
        else:
            if not user_input.strip():
                st.warning("Please provide some text to analyze.")
            elif model is None:
                st.error("Error: Model file 'modelo_burnout_pipeline.pkl' not found.")
            else:
                try:
                    # Model Inference
                    probs = model.predict_proba([user_input])
                    risk_prob = probs[0][1]
                    
                    detected = [w for w in CRITICAL_WORDS if w in user_input.lower()]
                    final_score = min(int(risk_prob * 100) + (len(detected) * EXTRA_POINTS), 100)
                    
                    # Modern Plotly Gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = final_score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        gauge = {
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2c3e50"},
                            'bar': {'color': "#3498db"},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "#ecf0f1",
                            'steps': [
                                {'range': [0, 40], 'color': '#2ecc71'},
                                {'range': [40, 75], 'color': '#f1c40f'},
                                {'range': [75, 100], 'color': '#e74c3c'}
                            ],
                        }
                    ))
                    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#2c3e50", 'family': "Inter"})
                    st.plotly_chart(fig, use_container_width=True)

                    # Result Summary
                    st.markdown("---")
                    if final_score < 40:
                        st.success("**Analysis:** Healthy / Balanced State")
                        st.write("Linguistic patterns suggest a stable professional well-being.")
                    elif final_score < 75:
                        st.warning("**Analysis:** Moderate Stress Detected")
                        st.write("Signs of tension found. Consider re-evaluating your workload.")
                    else:
                        st.error("**Analysis:** High Risk of Burnout")
                        st.write("Language patterns strongly correlate with chronic exhaustion.")
                    
                    if detected:
                        st.caption(f"Risk indicators found: {', '.join(detected)}")

                except Exception as e:
                    st.error(f"Analysis failed: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- BOTTOM INFO SECTION (Formerly Sidebar) ---
col_info_1, col_info_2, col_info_3 = st.columns(3)

with col_info_1:
    st.markdown("""
        <div class="bottom-info-box">
            <div class="bottom-info-title">🛡️ Project Info</div>
            This AI analyzes linguistic patterns to identify early signs of workplace stress and burnout.
        </div>
    """, unsafe_allow_html=True)

with col_info_2:
    st.markdown("""
        <div class="bottom-info-box" style="border-left-color: #f1c40f;">
            <div class="bottom-info-title">💡 Quick Tips</div>
            • Set clear boundaries<br>
            • Take regular micro-breaks<br>
            • Prioritize sleep quality
        </div>
    """, unsafe_allow_html=True)

with col_info_3:
    st.markdown("""
        <div class="bottom-info-box" style="border-left-color: #3498db;">
            <div class="bottom-info-title">🚀 Wellness Goal</div>
            "Empowering Workplace Wellness through intelligent insights and data-driven empathy."
        </div>
    """, unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>
        <b>MindGuard AI</b> • 2026 Academic Research Project <br>
        <i>Note: This tool provides general insights based on text patterns and is not a clinical assessment.</i>
    </div>
""", unsafe_allow_html=True)