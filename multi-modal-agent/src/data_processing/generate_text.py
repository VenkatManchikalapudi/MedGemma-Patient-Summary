# Sample text data generation script
# This script generates placeholder text files for testing purposes.

import os

output_dir = os.path.join(os.getcwd(), "data/text")
os.makedirs(output_dir, exist_ok=True)

# Generate 5 sample text files
for i in range(5):
    file_path = f"{output_dir}/sample_text_{i+1}.txt"
    print(f"Writing text to: {file_path}")
    try:
        with open(f"{output_dir}/sample_text_{i+1}.txt", "w") as f:
            f.write(f"This is sample text file {i+1}.")
        print(f"Successfully wrote: {output_dir}/sample_text_{i+1}.txt")
    except Exception as e:
        print(f"Error writing text {i+1}: {e}")

print("Sample text files generated in data/text/")