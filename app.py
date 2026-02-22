import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="LogiXForge",
    layout="wide"
)

# Custom Dark RTL Engineering Theme
st.markdown("""
<style>
body {
    background-color: #0b0f14;
    color: #e6edf3;
}

.stTextArea textarea {
    background-color: #161b22;
    color: #e6edf3;
    border-radius: 8px;
}

.stButton button {
    background-color: #238636;
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

code {
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("LogiXForge")
st.caption("Advanced AI RTL Design Assistant")

# Sidebar controls
with st.sidebar:
    st.header("Model Configuration")

    model_choice = st.selectbox(
        "Select Model",
        [
            "llama-3.1-8b-instant"
        ]
    )

    temperature = st.slider(
        "Creativity Level",
        0.0,
        1.0,
        0.2,
        0.1
    )

    st.markdown("---")
    st.write("Generate synthesizable Verilog designs from natural language specifications.")

# API Key
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Chat-style prompt input
user_prompt = st.text_area(
    "Describe your hardware design",
    placeholder="Example: Design a pipelined 8-bit ALU with carry and overflow detection."
)

# Generate button
if st.button("Generate RTL Design"):

    if not user_prompt.strip():
        st.warning("Please enter a hardware specification.")
    else:
        try:
            with st.spinner("Synthesizing logic..."):

                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are a professional RTL engineer.

1. First output clean, synthesizable Verilog code only.
2. After the code, write a section titled EXPLANATION.
3. In EXPLANATION, briefly describe architecture, signals, and working.
"""
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    temperature=temperature,
                    max_tokens=2000
                )

                output = response.choices[0].message.content

                # Split Code and Explanation
                if "EXPLANATION" in output:
                    parts = output.split("EXPLANATION")
                    code_part = parts[0]
                    explanation_part = parts[1]
                else:
                    code_part = output
                    explanation_part = "Explanation not generated."

                # Tabs
                tab1, tab2 = st.tabs(["Verilog Code", "Design Explanation"])

                with tab1:
                    st.code(code_part.strip(), language="verilog")
                    st.download_button(
                        label="Download Verilog File",
                        data=code_part.strip(),
                        file_name="logixforge_design.v",
                        mime="text/plain"
                    )

                with tab2:
                    st.write(explanation_part.strip())

        except Exception as e:
            st.error(f"API Error: {str(e)}")
