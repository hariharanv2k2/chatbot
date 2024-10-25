import os
import google.generativeai as genai
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Ensure that the API key is set and configure the client
    api_key = os.getenv("API_KEY")
    if not api_key:
        return jsonify({"error": "API_KEY environment variable is not set."}), 500

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Retrieve user message from form data
    user_message = request.form.get('message', '')

    # Generate content based on user message
    response = model.generate_content(user_message)
    print(response)
    
    # Assuming response has an attribute 'text' which holds the generated content
    generated_text = response.text if hasattr(response, 'text') else str(response)

    cleaned_response = generated_text.replace('**', '')

    # Extract data from the cleaned response into a list of bullet points
    data_points = []
    lines = cleaned_response.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("#") or line.startswith("*") or line.startswith("-"):
            data_point = line.lstrip("*-#").strip()
            if line.startswith("-"):
                data_points.append(f"- {data_point}")
            elif line.startswith("*"):
                data_points.append(f"* {data_point}")
            elif line.startswith("#"):
                data_points.append(f"# {data_point}")
    
    formatted_response = '\n'.join(lines)
    # Return JSON response with extracted data
    return jsonify({"response": formatted_response, "data_points": data_points})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
#AIzaSyAzpts5lhPiCjT0fSwpwaaSidrmiRuinhg
