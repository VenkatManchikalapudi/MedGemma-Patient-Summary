# Sample structured data generation script
# This script generates placeholder structured data in JSON format.

import json
import os

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

print("Sample structured data generated in data/structured/")