import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Code Explainer")
st.write("Paste your code below and I'll explain it!")

code = st.text_area("Paste your code here")

if st.button("Explain!"):
    if code:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": f"Explain this code in simple beginner friendly English:\n\n{code}"}
            ]
        )
        st.write(response.choices[0].message.content)
    else:
        st.warning("Please paste some code first!")
