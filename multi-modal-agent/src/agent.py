from flask import Flask, request, jsonify
import subprocess
import json
import sqlite3
import os

# Initialize the agent as a Flask app
app = Flask(__name__)

# Define the path to the SQLite database
DB_FILE = os.path.join(os.path.dirname(__file__), "data/medgemma.db")

def query_database(query, params=()):
    """Helper function to query the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except Exception as e:
        return {"error": str(e)}

def call_medgemma(prompt):
    """Call MedGemma via Ollama."""
    try:
        result = subprocess.run(
            ['ollama', 'run', 'medgemma', '--prompt', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error calling MedGemma: {str(e)}"

def pick_tool(modality, data):
    """Decide which tool to use based on the modality."""
    if modality == "text":
        return call_medgemma(data)
    elif modality == "structured":
        return "Structured data processing is not yet implemented."
    else:
        return "Unsupported modality."

@app.route('/process', methods=['POST'])
def process_request():
    """Process a client request by using the agent."""
    try:
        req_data = request.json
        query = req_data.get("query")
        patient_id = req_data.get("patient_id")

        if not query:
            return jsonify({"error": "Query is required."}), 400

        # If patient_id is provided, fetch patient data first
        context = ""
        if patient_id:
            admissions = query_database("SELECT * FROM ADMISSIONS WHERE patient_id = ?", (patient_id,))
            labevents = query_database("SELECT * FROM LABEVENTS WHERE patient_id = ? LIMIT 10", (patient_id,))
            prescriptions = query_database("SELECT * FROM PRESCRIPTIONS WHERE patient_id = ? LIMIT 10", (patient_id,))
            
            context = f"Patient Data:\nAdmissions: {json.dumps(admissions)}\nLab Events: {json.dumps(labevents)}\nPrescriptions: {json.dumps(prescriptions)}\n\n"
        
        # Use MedGemma to process the query with context
        full_prompt = f"{context}Query: {query}"
        result = call_medgemma(full_prompt)
        
        return jsonify({
            "result": result,
            "context": context if patient_id else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient_data(patient_id):
    """Get all data for a specific patient."""
    try:
        admissions = query_database("SELECT * FROM ADMISSIONS WHERE patient_id = ?", (patient_id,))
        labevents = query_database("SELECT * FROM LABEVENTS WHERE patient_id = ? LIMIT 20", (patient_id,))
        prescriptions = query_database("SELECT * FROM PRESCRIPTIONS WHERE patient_id = ? LIMIT 20", (patient_id,))
        
        return jsonify({
            "patient_id": patient_id,
            "admissions": admissions,
            "labevents": labevents,
            "prescriptions": prescriptions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the MedGemma Agent!"})

if __name__ == '__main__':
    print("Starting MedGemma Agent on port 8000...")
    app.run(debug=True, port=8000)