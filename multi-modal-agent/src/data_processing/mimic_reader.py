import pandas as pd
import os

# Define the path to the MIMIC-III CSV files
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '../data/text')

def read_csv(file_name):
    """Read a CSV file from the data folder."""
    file_path = os.path.join(DATA_FOLDER, file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File {file_name} not found in {DATA_FOLDER}")

def get_patient_data(patient_id):
    """Fetch patient data from all relevant tables."""
    patients = read_csv("PATIENTS.csv")
    admissions = read_csv("ADMISSIONS.csv")
    labevents = read_csv("LABEVENTS.csv")
    prescriptions = read_csv("PRESCRIPTIONS.csv")

    # Filter data by patient_id
    patient_info = patients[patients['patient_id'] == patient_id]
    patient_admissions = admissions[admissions['patient_id'] == patient_id]
    patient_labevents = labevents[labevents['patient_id'] == patient_id]
    patient_prescriptions = prescriptions[prescriptions['patient_id'] == patient_id]

    return {
        "patient_info": patient_info.to_dict(orient='records'),
        "admissions": patient_admissions.to_dict(orient='records'),
        "labevents": patient_labevents.to_dict(orient='records'),
        "prescriptions": patient_prescriptions.to_dict(orient='records')
    }