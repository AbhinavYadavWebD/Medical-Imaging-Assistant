from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-pro")
response = model.generate_content("Your prompt here")
