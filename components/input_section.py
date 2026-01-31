import streamlit as st

def render_input():
    with st.container(border=True):
        st.markdown("### ✍️ Share Your Story")
        st.write("Describe your recent workplace feelings, workload, or general mood:")

        text = st.text_area(
            "input_text",
            height=200,
            placeholder="E.g., I've been feeling extremely drained lately...",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button("Start Analysis")

    return text, analyze
