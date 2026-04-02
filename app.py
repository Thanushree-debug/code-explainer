import streamlit as st
from groq import Groq

# MUST be first
st.set_page_config(page_title="AI Code Explainer", page_icon="💻", layout="wide")

# CSS tweaks
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
div[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
    st.title("💻 AI Code Explainer")
    st.markdown("### 🚀 Features")
    st.write("✔ Explain code")
    st.write("✔ Detect bugs")
    st.write("✔ Suggest fixes")
    st.write("✔ Time complexity")
    st.markdown("---")
    st.info("Built using Streamlit + Groq")

# API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header (centered)
st.markdown("""
<h1 style='text-align: center;'>💻 AI Code Explainer</h1>
<p style='text-align: center; color: gray;'>Understand, Debug & Improve Code Instantly</p>
""", unsafe_allow_html=True)

# Language selector (clean placement)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    language = st.selectbox("🌐 Select Language", ["Python", "C", "Java", "JavaScript"])

st.markdown("---")

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🤖"):
        if msg["role"] == "user":
            st.code(msg["content"])
        else:
            st.markdown(msg["content"])

# Input
code = st.chat_input("💬 Paste your code here and press Enter...")

if code:
    # User message
    st.session_state.messages.append({"role": "user", "content": code})
    with st.chat_message("user", avatar="👤"):
        st.code(code)

    # AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing your code... 🤖"):
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

            st.code(answer, language="markdown")

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.markdown("<center>Built with ❤️ using Streamlit + Groq</center>", unsafe_allow_html=True)