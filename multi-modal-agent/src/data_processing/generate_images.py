# Sample image data generation script
# This script generates placeholder images for testing purposes.

from PIL import Image
import os

output_dir = os.path.join(os.getcwd(), "data/images")
os.makedirs(output_dir, exist_ok=True)

# Generate 5 sample images
for i in range(5):
    img = Image.new('RGB', (100, 100), color=(i * 50, i * 50, i * 50))
    try:
        img.save(f"{output_dir}/sample_image_{i+1}.png")
        print(f"Successfully saved: {output_dir}/sample_image_{i+1}.png")
    except Exception as e:
        print(f"Error saving image {i+1}: {e}")

print("Sample images generated in data/images/")