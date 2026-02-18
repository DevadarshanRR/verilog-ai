import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not set in environment variables.")

client = Groq(api_key=api_key)


def generate_verilog(description):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a Verilog HDL expert. Generate clean synthesizable Verilog code only."},
            {"role": "user", "content": description}
        ]
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def home():
    verilog_code = ""
    error_message = ""

    if request.method == "POST":
        description = request.form.get("description")

        if description:
            try:
                verilog_code = generate_verilog(description)
            except Exception as e:
                error_message = str(e)
        else:
            error_message = "Please enter a hardware specification."

    return render_template(
        "index.html",
        verilog_code=verilog_co
