import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create Gemini model
try:
    model = genai.GenerativeModel("gemini-2.5-flash")  # Updated to stable, high-capacity model
except Exception as e:
    print(f"Error initializing model: {str(e)}")
    exit(1)

# Generate response
try:
    response = model.generate_content("Generate a radiology report for a chest X-ray.")
    if not response.text:
        raise ValueError("Empty response from Gemini API")
    print(response.text)
except Exception as e:
    print(f"Error generating content: {str(e)}")