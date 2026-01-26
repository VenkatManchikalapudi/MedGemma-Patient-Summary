# Router setup for the project

from flask import Flask, jsonify, request
from src.models.image_model import process_images
from src.models.structured_model import process_structured_data
from src.models.text_model import process_text_data
from src.models.med_test_gemma_model import process_med_test_gemma
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the MedGemma API!"})

@app.route('/images', methods=['GET'])
def fetch_images():
    processed_images = process_images()
    return jsonify({"images": processed_images})

@app.route('/structured-data', methods=['GET'])
def fetch_structured_data():
    processed_data = process_structured_data()
    return jsonify({"structured_data": processed_data})

@app.route('/text', methods=['GET'])
def fetch_text():
    processed_text = process_text_data()
    return jsonify({"text": processed_text})

@app.route('/med-test-gemma', methods=['GET'])
def fetch_med_test_gemma():
    processed_data = process_med_test_gemma()
    return jsonify({"med_test_gemma": processed_data})

@app.route('/gemma-query', methods=['POST'])
def gemma_query():
    user_query = request.json.get('query', '')

    try:
        # Use Ollama Gemma model (2b version) to process the query
        result = subprocess.run(
            ['ollama', 'run', 'gemma:2b', '--prompt', user_query],
            capture_output=True,
            text=True
        )
        llm_response = result.stdout.strip()
        return jsonify({"gemma_response": llm_response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)