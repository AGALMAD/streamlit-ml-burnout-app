import streamlit as st

def render_chatbot(client):
    with st.popover("💬 Open Wellness Assistant", use_container_width=True):
        st.markdown("### 🤖 Burnout Coach")
        st.caption("Proactive tips and advice for your mental well-being.")


        system_prompt = (
            "You are a proactive Workplace Wellness Coach. Your primary goal is to help users "
            "by providing actionable tips, practical advice, and proven strategies to combat burnout. "
            "When a user shares a concern, briefly acknowledge it empathetically and then "
            "immediately offer 1-3 specific, easy-to-implement tips (e.g., the Pomodoro technique, "
            "setting digital boundaries, 'micro-breaks', or specific breathing exercises). "
            "Keep your tone encouraging and professional. ALWAYS respond in English."
        )


        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hello! I'm your MindGuard coach. If you're feeling overwhelmed, I'm here to provide tips and strategies. How can I help you improve your workday today?"
            }]

        messages_container = st.container(height=350)

        with messages_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        if prompt := st.chat_input("Ask for a tip or share how you feel..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with messages_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            with messages_container.chat_message("assistant"):
                try:
                    def stream_groq_response():

                        messages_for_api = [{"role": "system", "content": system_prompt}]
                        for m in st.session_state.messages:
                            messages_for_api.append({"role": m["role"], "content": str(m["content"])})

                        stream = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=messages_for_api,
                            stream=True,
                        )
                        for chunk in stream:
                            content = chunk.choices[0].delta.content
                            if content:
                                yield content

                    full_response = st.write_stream(stream_groq_response())
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")