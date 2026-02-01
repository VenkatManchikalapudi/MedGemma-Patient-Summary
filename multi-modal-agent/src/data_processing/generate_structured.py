# Sample structured data generation script
# This script generates placeholder structured data in JSON format.

import json
import os
import sqlite3
import pandas as pd

# Define the path to the text data folder
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '../data/text')

# Define the SQLite database file
DB_FILE = os.path.join(os.path.dirname(__file__), '../data/medgemma.db')

# List of files to load into SQLite
FILES_TO_LOAD = [
    "PRESCRIPTIONS.csv",
    "LABEVENTS.csv",
    "PATIENTS.csv",
    "ADMISSIONS.csv"
]

output_dir = os.path.join(os.getcwd(), "data/structured")
os.makedirs(output_dir, exist_ok=True)

# Generate 5 sample JSON files
for i in range(5):
    data = {
        "id": i + 1,
        "name": f"Sample Name {i+1}",
        "value": i * 10
    }
    file_path = f"{output_dir}/sample_data_{i+1}.json"
    print(f"Writing JSON to: {file_path}")
    try:
        with open(f"{output_dir}/sample_data_{i+1}.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"Successfully wrote: {output_dir}/sample_data_{i+1}.json")
    except Exception as e:
        print(f"Error writing JSON {i+1}: {e}")

def load_csv_to_sqlite():
    """Load specified CSV files into an SQLite database."""
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for file_name in FILES_TO_LOAD:
        file_path = os.path.join(DATA_FOLDER, file_name)
        if os.path.exists(file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Use the file name (without extension) as the table name
            table_name = os.path.splitext(file_name)[0]

            # Load the DataFrame into the SQLite database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Loaded {file_name} into table {table_name}.")
        else:
            print(f"File {file_name} does not exist in the data folder.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    load_csv_to_sqlite()
print("Sample structured data generated in data/structured/")