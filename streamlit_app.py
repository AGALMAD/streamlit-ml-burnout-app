import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# 1. Page Configuration
st.set_page_config(page_title="MindGuard AI", layout="wide", page_icon="🧠")

# 2. Custom CSS
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



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

# --- DASHBOARD LAYOUT (Centered) ---
col_left, col_center, col_right = st.columns([1, 1.5, 1], gap="large")

# === COLUMN 1: LEFT SIDEBAR (INFO) ===
with col_left:
    # Spacer column as requested
    st.markdown("<br>", unsafe_allow_html=True)

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

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>
        <b>MindGuard AI</b> • 2026 Academic Research Project <br>
        <i>Note: This tool provides general insights based on text patterns and is not a clinical assessment.</i>
    </div>
""", unsafe_allow_html=True)

# === COLUMN 3: RIGHT SPACER / CHATBOT LOCATION ===
with col_right:
    # Vertical Spacer to push chatbot down to match dashboard alignment
    st.markdown("<br>" * 15, unsafe_allow_html=True)
    
    # === CHATBOT UI ===
    with st.popover(" ", use_container_width=False):
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
        if prompt := st.chat_input("Message...", key="chat_input_floating"):
            # Add user message to state
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message instantly
            st.chat_message("user").markdown(prompt)

            # --- RESPONSE LOGIC ---
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # RESPONSE LOGIC (Rule-based)
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