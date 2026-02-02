import streamlit as st

def render_header():
    st.markdown('<h1 class="hero-title">MindGuard AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Decoding Workplace Stress through Linguistic Intelligence</p>',
        unsafe_allow_html=True
    )
