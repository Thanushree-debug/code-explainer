import streamlit as st
from groq import Groq
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="stChatMessage"] {
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="AI Code Explainer", page_icon="💻")

# API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Language selector
language = st.selectbox("Select Language", ["Python", "C", "Java", "JavaScript"])
st.title("💻 AI Code Explainer")
st.markdown("🚀 Chat with AI to understand your code")

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.code(msg["content"])
        else:
            st.markdown(msg["content"])

# User input
code = st.chat_input("Paste your code here...")

if code:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": code})
    with st.chat_message("user"):
        st.code(code)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Explain this {language} code in simple beginner friendly English.

Also include:
1. Step-by-step explanation
2. Time complexity (Big-O)
3. Any errors or bugs
4. Suggest improvements
5. Short summary

Code:
{code}
"""
                    }
                ]
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})