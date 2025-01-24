import streamlit as st

def create_chat_bubble():
    chat_container = st.sidebar.container()
    
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Changed key to make it unique
    if st.sidebar.button("💬 AI Assistant", key="chat_bubble_toggle"):
        st.session_state.show_chat = not st.session_state.show_chat

    if st.session_state.show_chat:
        with chat_container:
            st.markdown("### AI Assistant")
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Changed key to make it unique
            if prompt := st.text_input("Ask me anything...", key="chat_bubble_input"):
                return prompt
    return None