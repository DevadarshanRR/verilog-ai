import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="AI RTL Design Assistant", layout="wide")

st.title("AI RTL Design Assistant")
st.markdown("Natural Language to Verilog, Testbench and Explanation")

# Sidebar configuration
st.sidebar.header("Configuration")

model_choice = st.sidebar.selectbox(
    "Model",
    ["llama3-8b-8192"]
)

temperature = st.sidebar.slider("Creativity Level", 0.0, 1.0, 0.3)

optimization_mode = st.sidebar.selectbox(
    "Optimization Mode",
    ["Balanced", "Area Optimized", "Speed Optimized", "Power Optimized"]
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set.")
    st.stop()

client = Groq(api_key=api_key)

user_prompt = st.text_area("Enter Hardware Specification", height=150)

if st.button("Generate"):

    if not user_prompt.strip():
        st.warning("Please enter a hardware specification.")
    else:
        with st.spinner("Generating RTL..."):

            system_prompt = f"""
You are a professional RTL design engineer.

Optimization mode: {optimization_mode}

For the given hardware specification:
1. Generate clean synthesizable Verilog.
2. Generate a proper testbench.
3. Provide a simple explanation.
4. Mention approximate flip-flop usage.

Format output under:
### Verilog
### Testbench
### Explanation
"""

            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )

            result = response.choices[0].message.content

            sections = result.split("###")

            verilog = ""
            testbench = ""
            explanation = ""

            for section in sections:
                if "Verilog" in section:
                    verilog = section
                elif "Testbench" in section:
                    testbench = section
                elif "Explanation" in section:
                    explanation = section

            tab1, tab2, tab3 = st.tabs(["Verilog", "Testbench", "Explanation"])

            with tab1:
                st.code(verilog, language="verilog")
                st.download_button("Download Verilog File", verilog, file_name="design.v")

            with tab2:
                st.code(testbench, language="verilog")

            with tab3:
                st.write(explanation)
