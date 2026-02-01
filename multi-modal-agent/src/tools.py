from langchain.tools import tool
from pydantic import BaseModel
from src.data_processing.mimic_reader import get_patient_data

class PatientQueryInput(BaseModel):
    patient_id: str

@tool("query_patient_data", return_direct=True)
def query_patient_data(input: PatientQueryInput):
    """Query patient data from MIMIC-III tables by patient ID."""
    return get_patient_data(input.patient_id)