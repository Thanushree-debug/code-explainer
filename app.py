import streamlit as st
from groq import Groq

# Use Streamlit secrets (for deployment)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Code Explainer", page_icon="💻")

st.title("💻 AI Code Explainer")
st.markdown("### 🚀 Understand Code Instantly with AI")
st.write("Paste your code below and I'll explain it!")

language = st.selectbox("Select Language", ["Python", "C", "Java", "JavaScript"])
code = st.text_area("Paste your code here", height=200)

if st.button("Try Example"):
    st.code("for i in range(5):\n    print(i)")
    if code:
        with st.spinner("Thinking... 🤖"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"Explain this {language} in simple beginner friendly English:\n\n{code}"
                    }
                ]
            )
            st.success("Explanation:")
            st.markdown(response.choices[0].message.content)
    else:
        st.warning("Please paste some code first!")
