import streamlit as st

def render_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>
            <b>MindGuard AI</b> • 2026 Academic Research Project <br>
            <i>Note: This tool provides general insights and is not a clinical assessment.</i>
        </div>
    """, unsafe_allow_html=True)
