import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI RTL Design Assistant",
    layout="wide"
)

st.title("AI RTL Design Assistant")
st.write("Generate synthesizable Verilog from hardware specifications.")

# Get API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=api_key)

# User input
prompt = st.text_area(
    "Enter Hardware Specification",
    placeholder="Example: Design a 4-bit synchronous counter with reset."
)

# Generate button
if st.button("Generate"):

    if not prompt.strip():
        st.warning("Please enter a hardware specification.")
    else:
        try:
            with st.spinner("Generating Verilog code..."):

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert RTL engineer. Generate clean, synthesizable Verilog code only. Do not include explanations."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=1024
                )

                result = response.choices[0].message.content

                st.subheader("Generated Verilog Code")
                st.code(result, language="verilog")

        except Exception as e:
            st.error(f"API Error: {str(e)}")
