import streamlit as st

def render_chatbot(client):
    with st.popover("💬 Open Assistant", use_container_width=True):
        st.markdown("### 🤖 Wellness Assistant")
        st.caption("Chat with our AI for burnout prevention tips.")

        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hello! I'm your MindGuard assistant. How are you feeling today?"
            }]

        messages_container = st.container(height=300)

        with messages_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        if prompt := st.chat_input("Type your message..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with messages_container.chat_message("assistant"):
                response = "I'm listening. Tell me more."
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
