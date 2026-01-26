# Image model processing

from src.models.med_test_gemma_model import process_med_test_gemma

def process_images():
    # Use Med Test Gemma model for image processing
    med_test_gemma_result = process_med_test_gemma()
    return {"images": ["image1.png", "image2.png", "image3.png"], "med_test_gemma": med_test_gemma_result}