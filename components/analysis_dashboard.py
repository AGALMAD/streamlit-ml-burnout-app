import streamlit as st
import plotly.graph_objects as go
import time

def render_analysis(model, user_input, analyze_btn):
    with st.container(border=True):
        st.markdown("### 📊 Insight Dashboard")

        if not analyze_btn:
            st.markdown("""
                <div style='text-align: center; color: #bdc3c7; padding: 2rem;'>
                    <span style='font-size: 40px;'>🧠</span>
                    <p>Analysis results will appear here</p>
                </div>
            """, unsafe_allow_html=True)
            return

        if not user_input.strip():
            st.warning("Please provide some text to analyze.")
            return

        model_output = model.predict(user_input)

        prediction = int(model_output["prediction"])
        confidence = model_output["probability"]

        burnout_risk = confidence * 100 if prediction == 1 else (1 - confidence) * 100

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=burnout_risk,
            number={"suffix": "%", "font": {"color": "white"}},
            title={"text": "Burnout Risk", "font": {"color": "white"}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": "white"}},
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
            font={"color": "#ffffff"}
        )

        chart_placeholder = st.empty()
        

        target_value = int(burnout_risk)
        step = 2 if target_value > 50 else 1
        

        if "last_risk" not in st.session_state or st.session_state.last_risk != burnout_risk:
            st.session_state.last_risk = burnout_risk
            current_val = 0
            while current_val <= target_value:
                fig.update_traces(value=current_val)
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                current_val += step
                time.sleep(0.01)
        

        fig.update_traces(value=burnout_risk)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        if burnout_risk < 40:
            st.success("🟢 **Low risk of burnout**")
            st.write("Linguistic patterns indicate a healthy and balanced state.")
        elif burnout_risk < 75:
            st.warning("🟡 **Moderate risk of burnout**")
            st.write("Some stress indicators detected.")
        else:
            st.error("🔴 **High risk of burnout**")
            st.write("Strong linguistic signals detected.")
