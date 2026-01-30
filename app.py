import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="MindGuard AI", layout="wide", page_icon="🧠")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to enable the AI assistant.")

# 2. Advanced CSS
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f4f7f9;
        color: #2c3e50;
    }

    /* Disable text area resize */
    textarea {
        resize: none !important;
    }

    /* Reduce default top padding of Streamlit app */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Styled Containers (The Vertical Blocks) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border-top: 8px solid #3498db !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        padding: 30px !important;
        margin-bottom: 2rem !important;
    }

    /* Main Title Animation Look */
    .hero-title {
        text-align: center;
        padding: 0.5rem 0;
        background: linear-gradient(90deg, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* Action Button Container */
    .stButton {
        display: flex;
        justify-content: center;
        padding: 1rem 0; 
    }

    /* Modern & Striking Button */
    .stButton button {
        width: 100% !important;
        max-width: 400px;
        border-radius: 50px;
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        height: 3.5rem;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
    }

    .stButton button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 25px rgba(255, 75, 43, 0.4);
    }
    
    /* Bottom Info Section Styles */
    .bottom-info-box {
        background-color: white;
        color: #2c3e50; 
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2ecc71;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
        transition: transform 0.2s;
        margin-bottom: 1rem;
    }
    .bottom-info-box:hover {
        transform: scale(1.02);
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

# --- DASHBOARD LAYOUT (3 Columns) ---
col_left, col_center, col_right = st.columns([1, 2, 1], gap="large")

# === COLUMN 1: LEFT SIDEBAR (INFO) ===
with col_left:
    st.markdown("### 📚 Resources")
    st.markdown("""
        <div class="bottom-info-box">
            <div class="bottom-info-title">🛡️ Project Info</div>
            This AI analyzes linguistic patterns to identify early signs of burnout.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="bottom-info-box" style="border-left-color: #f1c40f;">
            <div class="bottom-info-title">💡 Quick Tips</div>
            • Set boundaries<br>
            • Take micro-breaks<br>
            • Prioritize sleep
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="bottom-info-box" style="border-left-color: #3498db;">
            <div class="bottom-info-title">🚀 Goal</div>
            "Empowering Wellness through data-driven empathy."
        </div>
    """, unsafe_allow_html=True)

# === COLUMN 2: CENTER STAGE (MAIN APP) ===
with col_center:
    with st.container(border=True):
        st.markdown("### ✍️ Share Your Story")
        st.write("Describe your recent workplace feelings, workload, or general mood:")
        
        user_input = st.text_area(
            "input_text",
            height=200, 
            placeholder="E.g., I've been feeling extremely drained lately...",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True) 
        
        # --- ACTION BUTTON ---
        analyze_btn = st.button("Start Analysis")

    # --- BLOCK 2: OUTPUT ---
    with st.container(border=True):
        st.markdown("### 📊 Insight Dashboard")
        
        if not analyze_btn:
            st.markdown("""
                <div style='text-align: center; color: #bdc3c7; padding: 2rem;'>
                    <span style='font-size: 40px;'>🧠</span>
                    <p>Analysis results will appear here</p>
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
                    
                    # Gauge Chart
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
                    fig.update_layout(height=180, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#2c3e50", 'family': "Inter"})
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

# === COLUMN 3: RIGHT SIDEBAR (CHATBOT) ===
with col_right:
    with st.container(border=True):
        st.markdown("### 🤖 Assistant")
        st.caption("Chat with our AI.")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm here to listen. How are you feeling right now?"}]

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Message...", key="chat_input_right"):
            # Add user message to state
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message instantly
            st.chat_message("user").markdown(prompt)

            # --- RESPONSE LOGIC ---
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # OPTION A: OPENAI API
                if api_key:
                    try:
                        client = OpenAI(api_key=api_key)
                        messages_for_api = [
                            {"role": "system", "content": "You are MindGuard, a compassionate and empathetic AI assistant specialized in workplace mental health. Keep answers concise, supportive, and safe. Do not provide medical diagnoses."}
                        ] + [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]

                        stream = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=messages_for_api,
                            stream=True,
                        )
                        
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)

                    except Exception as e:
                        st.error(f"Error: {e}")
                        full_response = "I'm having trouble connecting. Please check your API Key."
                        message_placeholder.markdown(full_response)

                # OPTION B: FALLBACK MOCK (Rule-based)
                else:
                    import time
                    time.sleep(0.5) 
                    p_lower = prompt.lower()
                    if "stress" in p_lower or "overwhelmed" in p_lower:
                        full_response = "I understand. High stress levels can be paralyzing. Have you tried the 4-7-8 breathing technique?"
                    elif "sleep" in p_lower or "tired" in p_lower:
                        full_response = "Exhaustion often exacerbates burnout. Are you able to disconnect from screens an hour before bed?"
                    elif "deadlines" in p_lower or "work" in p_lower:
                        full_response = "Workload pressure is real. Breaking tasks into tiny, 5-minute chunks might help you regain control."
                    elif "yes" in p_lower:
                        full_response = "That's great! Small steps lead to big changes. How did that make you feel?"
                    elif "no" in p_lower:
                        full_response = "That's okay. Everyone finds their own path. What usually helps you disconnect?"
                    else:
                        full_response = "I'm listening. Tell me more about how that affects your day-to-day work."
                    
                    message_placeholder.markdown(full_response)

            # Add assistant response to state
            st.session_state.messages.append({"role": "assistant", "content": full_response})


st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>
        <b>MindGuard AI</b> • 2026 Academic Research Project <br>
        <i>Note: This tool provides general insights based on text patterns and is not a clinical assessment.</i>
    </div>
""", unsafe_allow_html=True)