import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='../frontend')

# Gemini API configuration
GEMINI_API_URL = "https://yellow-diamond12719.my-vm.work/api/request"

@app.route('/api/decompose', methods=['POST'])
def decompose_task():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    task_text = data['text']

    system_instructions = """
You are an expert project manager. Your task is to break down a complex user request into a series of smaller, actionable subtasks.
Each subtask should be a clear, concise instruction that a developer or another AI could execute.
Provide the output as a numbered list. Do not add any extra commentary before or after the list.

Example:
User Request: Create a beautiful, large website.
Your Output:
1. Design the website's color scheme and typography.
2. Create the main landing page with a hero section.
3. Develop the 'About Us' page with company information.
4. Implement a 'Contact Us' form with validation.
5. Set up a blog section with initial articles.
6. Ensure the website is responsive on all devices.
7. Deploy the website to a hosting service.
"""

    payload = {
        "text": f"User Request: {task_text}\nYour Output:",
        "model": "gemini-2.5-flash-lite",
        "system_instructions": system_instructions,
        "internet": False,
        "thinking": False
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        api_response_text = response.json().get('text', '')

        # The AI's response is expected to be a numbered list.
        # We split the response by newlines and filter out any empty lines.
        lines = [line.strip() for line in api_response_text.split('\n') if line.strip()]

        # Make parsing more robust
        subtasks = []
        for line in lines:
            # Check if the line starts with a number and a dot.
            parts = line.split('.', 1)
            if len(parts) > 1 and parts[0].isdigit():
                subtasks.append(parts[1].strip())
            else:
                subtasks.append(line)


        return jsonify({'subtasks': subtasks})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to connect to Gemini API: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Use Gunicorn for production, but this is fine for development
    app.run(debug=True, port=5000)
