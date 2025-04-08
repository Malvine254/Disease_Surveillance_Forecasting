import os
import pandas as pd
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify, render_template, session
import logging
import re
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_CHAT_MODEL = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://armelyopenai.openai.azure.com/')

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE

current_date = datetime.now().strftime("%B %d, %Y")

app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(level=logging.DEBUG)

# Load entire CSV data as context for OpenAI
def load_csv_for_openai(file_path):
    try:
        df = pd.read_csv(file_path)
        csv_full_text = df.to_csv(index=False)
        return csv_full_text
    except Exception as e:
        logging.error("Failed to load CSV: %s", e)
        return "The dataset could not be loaded."

# Build prompt with full CSV context
def build_prompt_with_history(question, csv_data=None):
    if 'conversation_history' not in session:
        session['conversation_history'] = []

    session['conversation_history'].append(("user", question))

    prompt_messages = [
        {"role": "system", "content": f"You are an AI assistant specialized in analyzing CSV data. Today's date is {current_date}."}
    ]

    if csv_data:
        prompt_messages.append({"role": "system", "content": f"Here is the complete dataset:\n{csv_data}"})

    for role, content in session['conversation_history']:
        prompt_messages.append({"role": role, "content": content})

    return prompt_messages

# Get OpenAI response
def get_openai_response(final_prompt):
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_CHAT_MODEL,
            messages=final_prompt,
            deployment_id=OPENAI_CHAT_MODEL
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error("OpenAI API Error: %s", e)
        return "Sorry, an error occurred."

# Format response to HTML
def format_response_to_html(response_text):
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', response_text)
    formatted_text = formatted_text.replace('\n', '<br>')
    return formatted_text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        query = request.json.get("message") or "Provide examples of records to search"
        csv_data_full = load_csv_for_openai('docs/knowledge_base.csv')
        final_prompt = build_prompt_with_history(query, csv_data=csv_data_full)
        final_answer = get_openai_response(final_prompt)

        session['conversation_history'].append(("assistant", final_answer))
        formatted_answer = format_response_to_html(final_answer)

        if any(keyword in query.lower() for keyword in ["chart", "graph", "visual", "plot", "pie"]):
            df = pd.read_csv('docs/knowledge_base.csv')
            categories, values = df.iloc[:, 0], df.iloc[:, 1]

            plt.figure(figsize=(8, 8) if "pie" in query.lower() else (10, 6))
            if "pie" in query.lower():
                plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
            else:
                plt.bar(categories, values)

            img = BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            img_base64 = base64.b64encode(img.getvalue()).decode()

            return jsonify({"summary": formatted_answer, "chart_image": img_base64})

        return jsonify({"summary": formatted_answer, "chart_image": None})

    except Exception as e:
        logging.error("Error: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route("/reset", methods=["POST"])
def reset_conversation():
    session.pop('conversation_history', None)
    return jsonify({"message": "Conversation reset."})

if __name__ == "__main__":
    app.run(debug=True)