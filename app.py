import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="AI RTL Assistant", layout="wide")

st.title("AI RTL Design Assistant")

api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

prompt = st.text_area("Enter Hardware Specification")

if st.button("Generate"):

    if not prompt.strip():
        st.warning("Please enter a description.")
    else:
        with st.spinner("Generating..."):

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You generate clean synthesizable Verilog code only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1024
            )

            result = response.choices[0].message.content

            st.code(result, language="verilog")
