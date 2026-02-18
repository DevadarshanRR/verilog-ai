import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="AI RTL Assistant", layout="wide")

st.title("🧠 AI RTL Design Assistant")
st.markdown("Generate Verilog, Testbench, and Explanation from natural language.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=api_key)

prompt = st.text_area("Enter Hardware Specification")

if st.button("Generate"):

    if not prompt.strip():
        st.warning("Please enter a hardware description.")
    else:
        with st.spinner("Generating..."):

            system_prompt = """
            You are an expert RTL engineer.
            For the given hardware description:
            1. Generate clean synthesizable Verilog.
            2. Generate a pr
