from flask import Flask, render_template, request, jsonify
import os
import json
import logging
import uuid
from openai import OpenAI
from dotenv import load_dotenv  # Import dotenv

load_dotenv()  # Load environment variables from .env

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No API key set for OpenAI. Please set the OPENAI_API_KEY environment variable.")
client = OpenAI(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)

# ==========================
# Configure Logging
# ==========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================
# Helper Functions
# ==========================

def is_test_generation_prompt(prompt):
    """
    Determines if the provided prompt is related to test generation.
    Returns True if related, False otherwise.
    """
    system_message = (
        "You are an assistant that determines whether a given prompt is related to test generation for software testing scenarios. "
        "Reply with 'Yes' or 'No' only."
    )
    user_message = f"Is the following prompt related to test generation?\n\nPrompt: {prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0
        )
        answer = response.choices[0].message.content.strip().lower()
        logger.info(f"Prompt relevance check response: {answer}")
        return answer == "yes"
    except Exception as e:
        logger.error(f"Error in is_test_generation_prompt: {str(e)}")
        return False

def generate_test(prompt, file_content):
    """
    Generates complete Unity test code based on the provided prompt and scene file content.
    The generated test code MUST be based solely on the Arium test automation framework.
    Do NOT include any setup, installation, or general instructions in the final output.
    """
    atrium_syntax = (
        "Arium Framework Syntax Reference:\n"
        "1. Instantiate Arium:\n"
        "   Arium _arium = new Arium();\n"
        "2. Find GameObjects:\n"
        "   _arium.FindGameObject(\"Display\");\n"
        "   _arium.FindGameObject(\"Display\", true);\n"
        "3. Get Components:\n"
        "   _arium.GetComponent<ComponentName>(\"GameObjectName\");\n"
        "4. Perform Actions:\n"
        "   _arium.PerformAction(new UnityPointerClick(), \"GameObjectName\");\n"
        "5. Unity Event System:\n"
        "   UnityEventSystemInteraction<T>.PerformAction(\"GameObjectName\");\n"
    )

    system_message = (
        "You are an expert assistant in generating complete Unity test scripts using the Arium test automation framework. "
        "Your output must be valid C# Unity test code and must be strictly based on the Arium framework. "
        "Do NOT include any setup, installation, or general framework instructions in your final output; output only the necessary test code. "
        "As guidance, refer to the following Arium Framework Syntax:\n"
        f"{atrium_syntax}\n"
        "Use the syntax above as a reference for generating the test code, but do not output these instructions or the syntax in the final code."
    )

    user_message = (
        f"Test Scenario Description:\n{prompt}\n\n"
        f"Scene File Content:\n{file_content}\n\n"
        "Based on the above, generate complete Unity test code using the Arium framework. Output only the code."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500
        )
        assistant_reply = response.choices[0].message.content.strip()
        logger.info("Test generation response received.")
        return {'answer': assistant_reply}

    except Exception as e:
        logger.error(f"Error in generate_test: {str(e)}")
        raise e

# ==========================
# Routes
# ==========================

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles submission of prompts and files to generate tests.
    Expects 'prompt' and 'file' in form data.
    """
    try:
        # Get prompt
        prompt = request.form.get('prompt', '').strip()

        # Get file
        file = request.files.get('file')
        if not file or file.filename == '':
            logger.warning("No file attached.")
            return jsonify({'error': 'Please attach a file to the request.'}), 400

        # Validate file type
        filename = file.filename
        if not filename.lower().endswith(('.yaml', '.yml', '.unity')):
            logger.warning("Invalid file type.")
            return jsonify({'error': 'Please upload a YAML or Unity file.'}), 400

        # Read file content
        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            logger.warning("Unable to read file content.")
            return jsonify({'error': 'Unable to read file content. Please ensure it is a valid YAML or Unity file.'}), 400

        logger.info(f"Received prompt: {prompt}")

        # Validate prompt input
        if not prompt:
            logger.warning("No prompt provided.")
            return jsonify({'error': 'No prompt provided.'}), 400
        if len(prompt) > 128000:
            logger.warning("Prompt is too long.")
            return jsonify({'error': 'Prompt is too long. Please limit to 128000 characters.'}), 400

        # Check if the prompt is related to test generation
        if not is_test_generation_prompt(prompt):
            logger.info("Prompt is not related to test generation.")
            return jsonify({'error': 'This prompt is not related to test generation.'}), 400

        # Generate the test scenario based solely on the provided framework
        test_result = generate_test(prompt, file_content)
        return jsonify(test_result)

    except Exception as e:
        logger.error(f"An error occurred in /submit route: {str(e)}")
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    # Run the Flask app in debug mode (disable in production)
    app.run()
