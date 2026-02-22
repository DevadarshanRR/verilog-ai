import streamlit as st
from groq import Groq

# ---------------- Page Config ----------------
st.set_page_config(page_title="logX", layout="wide")

# ---------------- Custom Dark Theme ----------------
st.markdown("""
<style>
body {
    background-color: #0b0f14;
    color: #e6edf3;
}

/* Text Area Styling */
.stTextArea textarea {
    background-color: #161b22;
    color: #e6edf3;
    border-radius: 12px;
    border: 1px solid #30363d;
    padding: 15px;
}

/* Circular Arrow Button */
div.stButton > button {
    background-color: #238636;
    color: white;
    border-radius: 50%;
    height: 50px;
    width: 50px;
    font-size: 20px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background-color: #2ea043;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("logX")
st.caption("AI RTL Design Assistant")

# ---------------- API Setup ----------------
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# ---------------- Load Available Models ----------------
try:
    model_list = client.models.list()
    available_models = sorted([model.id for model in model_list.data])
except:
    available_models = ["llama-3.1-8b-instant"]

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Configuration")

    model_choice = st.selectbox(
        "Select Model",
        available_models
    )

    temperature = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.2,
        0.1
    )

    st.markdown("---")
    st.write("Natural Language → Synthesizable Verilog")

# ---------------- Chat Input Layout ----------------
col1, col2 = st.columns([10, 1])

with col1:
    user_prompt = st.text_area(
        "",
        placeholder="Design a 3-stage pipeline MIPS processor.",
        label_visibility="collapsed"
    )

with col2:
    send_clicked = st.button("⬆")

# ---------------- Generate Logic ----------------
if send_clicked:

    if not user_prompt.strip():
        st.warning("Enter a hardware specification.")
    else:
        try:
            with st.spinner("Synthesizing logic..."):

                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {
                            
    "role": "system",
    "content": """
You are a senior FPGA and ASIC RTL design engineer.

Your task is to generate production-quality, fully synthesizable Verilog RTL.

Strict Design Rules:

1. All designs must be fully synthesizable (no simulation-only constructs).
2. Always implement complete FSM logic including:
   - State encoding
   - Next-state logic
   - Proper reset behavior
3. No incomplete frameworks or placeholder comments.
4. All registers must be reset explicitly.
5. Avoid unintended latches (always assign default values in combinational blocks).
6. Use non-blocking assignments for sequential logic.
7. Use blocking assignments for combinational logic.
8. Parameterize designs where appropriate.
9. Include proper flag generation (overflow, zero, carry, error signals if relevant).
10. For pipelined designs:
    - Clearly define pipeline stages.
    - Register outputs between stages.
11. For counters or timing logic:
    - Handle overflow conditions correctly.
    - Reset counters properly.
12. For communication modules (UART, SPI, I2C, FIFO):
    - Implement proper state transitions.
    - Handle edge detection.
    - Include error detection if applicable.
13. Ensure clean modular structure.
14. Avoid redundant logic.
15. Code must be interview-level and production-ready.

Output format:
- First provide complete Verilog code.
- Then provide a section titled EXPLANATION explaining architecture and design decisions.
"""


                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    temperature=0.1,
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
                tab1, tab2 = st.tabs(["Verilog Code", "Explanation"])

                with tab1:
                    st.code(code_part.strip(), language="verilog")
                    st.download_button(
                        label="Download .v file",
                        data=code_part.strip(),
                        file_name="logX_design.v",
                        mime="text/plain"
                    )

                with tab2:
                    st.write(explanation_part.strip())

        except Exception as e:
            st.error(f"API Error: {str(e)}")
