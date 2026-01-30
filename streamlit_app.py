import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import ollama
from services.predictor import TextPredictor

# Page Configuration
st.set_page_config(page_title="MindGuard AI", layout="wide", page_icon="🧠")

# Custom CSS
with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load Pre-trained Model
model = TextPredictor()


# Initialize Ollama Client for Docker
# 'host.docker.internal' allows the container to talk to Ollama on your host machine
#client = ollama.Client(host='http://host.docker.internal:11434')



# --- HEADER ---
st.markdown('<h1 class="hero-title">MindGuard AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Decoding Workplace Stress through Linguistic Intelligence</p>', unsafe_allow_html=True)

# --- DASHBOARD LAYOUT ---
col_left, col_center, col_right = st.columns([1, 1.5, 1], gap="large")

with col_left:
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
        analyze_btn = st.button("Start Analysis")

   # --- ANALYSIS OUTPUT ---
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
                st.error("Error: Model not loaded.")

            else:
                # Analyze Input Text
                model_output = model.predict(user_input)

                prediction = int(model_output["prediction"])
                confidence = model_output["probability"]

                # Convert to burnout risk percentage
                if prediction == 1:
                    burnout_risk = confidence * 100
                else:
                    burnout_risk = (1 - confidence) * 100

                # Chart Visualization
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=burnout_risk,
                    number={"suffix": "%"},
                    title={"text": "Burnout Risk"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#3498db"},
                        "steps": [
                            {"range": [0, 40], "color": "#2ecc71"},
                            {"range": [40, 75], "color": "#f1c40f"},
                            {"range": [75, 100], "color": "#e74c3c"}
                        ]
                    }
                ))

                fig.update_layout(
                    height=240,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#2c3e50"}
                )

                st.plotly_chart(fig, use_container_width=True)

                # Textual Interpretation
                st.markdown("---")

                if burnout_risk < 40:
                    st.success("🟢 **Low risk of burnout**")
                    st.write("Linguistic patterns indicate a healthy and balanced state.")

                elif burnout_risk < 75:
                    st.warning("🟡 **Moderate risk of burnout**")
                    st.write("Some stress indicators detected. Consider adjusting workload or routines.")

                else:
                    st.error("🔴 **High risk of burnout**")
                    st.write("Strong linguistic signals associated with chronic exhaustion detected.")

# === COLUMN 3: AI CHATBOT (OLLAMA) ===
with col_right:
    with st.popover("💬 Open Assistant", use_container_width=True):
        st.markdown("### 🤖 Wellness Assistant")
        st.caption("Chat with our AI for burnout prevention tips.")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your MindGuard assistant. How are you feeling today?"}]

        # Create a container for messages to keep them above the input
        messages_container = st.container(height=300)
        with messages_container:
            # Display history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Type your message...", key="chat_input_floating"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with messages_container.chat_message("user"):
                st.markdown(prompt)

            # Response Logic with Ollama (Phi-3)
            with messages_container.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # System Prompt for burnout tips
                system_prompt = (
                    "You are a professional workplace wellness coach. Your goal is to provide "
                    "short, empathetic, and actionable tips to reduce burnout and stress. "
                    "Suggest techniques like Pomodoro, box breathing, digital detox, or setting boundaries. "
                    "Keep responses concise and supportive."
                )

                try:
                    # Request to the local Ollama instance
                    response = client.chat(
                        model='phi3',
                        messages=[{'role': 'system', 'content': system_prompt}] + st.session_state.messages,
                        stream=True,
                    )

                    for chunk in response:
                        full_response += chunk['message']['content']
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    st.error("Connection Error: Make sure Ollama is running on your host.")
                    full_response = "I'm having trouble connecting to my brain right now. Please try again later."
                    message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>
        <b>MindGuard AI</b> • 2026 Academic Research Project <br>
        <i>Note: This tool provides general insights and is not a clinical assessment.</i>
    </div>
""", unsafe_allow_html=True)