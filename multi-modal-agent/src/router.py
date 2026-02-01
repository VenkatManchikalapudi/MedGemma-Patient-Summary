# Router setup for the project

from flask import Flask, jsonify, request
import subprocess
import sqlite3
import json
import os

# Initialize the Flask app
app = Flask(__name__)

# Define the path to the SQLite database - use absolute path
DB_FILE = os.path.join(os.path.dirname(__file__), "data/medgemma.db")

def query_database(query, params=()):
    """Helper function to query the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

# Define routes directly in Flask
@app.route('/images', methods=['GET'])
def get_images():
    """Fetch processed images."""
    from models.image_model import process_images
    return jsonify(process_images())

@app.route('/structured-data', methods=['GET'])
def get_structured_data():
    """Fetch processed structured data."""
    from models.structured_model import process_structured_data
    return jsonify(process_structured_data())

@app.route('/text', methods=['GET'])
def get_text_data():
    """Fetch processed text data."""
    from models.text_model import process_text_data
    return jsonify({"text": process_text_data()})

@app.route('/med-test-gemma', methods=['GET'])
def get_med_test_gemma():
    """Fetch MedGemma test data."""
    from models.med_test_gemma_model import process_med_test_gemma
    return jsonify(process_med_test_gemma())

@app.route('/gemma-query', methods=['POST'])
def gemma_query():
    """Process user query using Med-Gemma."""
    query = request.json.get('query', '')
    result = subprocess.run(
        ['ollama', 'run', 'gemma:2b', '--prompt', query],
        capture_output=True,
        text=True
    )
    return jsonify({"result": result.stdout.strip()})

@app.route('/admissions', methods=['GET'])
def get_admissions():
    """Fetch all admissions data."""
    return jsonify(query_database("SELECT * FROM ADMISSIONS"))

@app.route('/labevents', methods=['GET'])
def get_labevents():
    """Fetch all lab events data."""
    return jsonify(query_database("SELECT * FROM LABEVENTS"))

@app.route('/patients', methods=['GET'])
def get_patients():
    """Fetch all patients data."""
    return jsonify(query_database("SELECT * FROM PATIENTS"))

@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    """Fetch all prescriptions data."""
    return jsonify(query_database("SELECT * FROM PRESCRIPTIONS"))

@app.route('/admissions/<patient_id>', methods=['GET'])
def get_patient_admissions(patient_id):
    """Fetch admissions data for a specific patient."""
    return jsonify(query_database("SELECT * FROM ADMISSIONS WHERE patient_id = ?", (patient_id,)))

@app.route('/labevents/<patient_id>', methods=['GET'])
def get_patient_labevents(patient_id):
    """Fetch lab events data for a specific patient."""
    return jsonify(query_database("SELECT * FROM LABEVENTS WHERE patient_id = ?", (patient_id,)))

@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient_details(patient_id):
    """Fetch patient details for a specific patient."""
    return jsonify(query_database("SELECT * FROM PATIENTS WHERE patient_id = ?", (patient_id,)))

@app.route('/prescriptions/<patient_id>', methods=['GET'])
def get_patient_prescriptions(patient_id):
    """Fetch prescriptions data for a specific patient."""
    return jsonify(query_database("SELECT * FROM PRESCRIPTIONS WHERE patient_id = ?", (patient_id,)))

@app.route('/process', methods=['POST'])
def process_request():
    """Route to dynamically decide which model to use based on the patient ID and database lookup."""
    data = request.json
    patient_id = data.get('patient_id')

    # Look up the patient ID in the database
    patient_data = query_database("SELECT * FROM PATIENTS WHERE patient_id = ?", (patient_id,))

    if not patient_data:
        return jsonify({"error": "Patient ID not found in the database"}), 404

    # Decide the modality based on the patient data (example logic)
    if 'image' in patient_data[0]:
        modality = "image"
    elif 'structured' in patient_data[0]:
        modality = "structured"
    elif 'text' in patient_data[0]:
        modality = "text"
    else:
        modality = "med-test-gemma"

    payload = patient_data[0]  # Use the patient data as the payload

    # Forward the request to the appropriate model
    if modality == "image":
        from models.image_model import process_images
        return jsonify(process_images(payload))
    elif modality == "structured":
        from models.structured_model import process_structured_data
        return jsonify(process_structured_data(payload))
    elif modality == "text":
        from models.text_model import process_text_data
        return jsonify(process_text_data(payload))
    elif modality == "med-test-gemma":
        from models.med_test_gemma_model import process_med_test_gemma
        return jsonify(process_med_test_gemma(payload))
    else:
        return jsonify({"error": "Unsupported modality"}), 400

def send_to_llm(modality, data):
    """Send data to the appropriate LLM based on the modality."""
    if modality == "text":
        # Use MedGemma for text queries
        return subprocess.run(
            ['ollama', 'run', 'medgemma', '--prompt', str(data)],
            capture_output=True,
            text=True
        ).stdout.strip()
    else:
        return "Unsupported modality"

@app.route('/query/<patient_id>', methods=['GET'])
def query_patient_text(patient_id):
    """Query text data by patient ID and send to Gemma 2b."""
    text_data = query_database("SELECT * FROM TEXT WHERE patient_id = ?", (patient_id,))
    return jsonify({
        "response": send_to_llm("text", text_data)
    })

# Export the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=7000)  # Changed port to 7000 to avoid conflict