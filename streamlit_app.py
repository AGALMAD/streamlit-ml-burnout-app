import streamlit as st
import ollama
from services.predictor import TextPredictor

from components.header import render_header
from components.input_section import render_input
from components.analysis_dashboard import render_analysis
from components.chatbot import render_chatbot
from components.footer import render_footer

st.set_page_config(page_title="MindGuard AI", layout="wide", page_icon="🧠")

with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

model = TextPredictor()
client = ollama.Client(host='http://host.docker.internal:11434')

render_header()

col_left, col_center, col_right = st.columns([1, 1.5, 1], gap="large")

with col_center:
    user_input, analyze_btn = render_input()
    render_analysis(model, user_input, analyze_btn)

with col_right:
    render_chatbot(client)

render_footer()
