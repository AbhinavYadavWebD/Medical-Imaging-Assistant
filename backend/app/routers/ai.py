import os
import google.generativeai as genai
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import SessionLocal
from app.models.images import Image
from app.models.reports import Report
from app.schemas.reports import ReportOut
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
try:
    model = genai.GenerativeModel("gemini-2.5-flash")  # Using stable, multimodal model
except Exception as e:
    raise Exception(f"Failed to initialize Gemini model: {str(e)}")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate-report/{image_id}", response_model=ReportOut)
def generate_report(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Retrieve file_path or construct from filename
    file_path = image.file_path if image.file_path else os.path.join(os.path.abspath("uploads"), image.filename)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=500, detail=f"Image file not found at {file_path}")

    # Load image content from file
    try:
        with open(file_path, 'rb') as f:
            image_content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading image file: {str(e)}")

    prompt = f"""
You are an expert radiologist. Please generate a structured medical report based on the provided chest X-ray image.

Image Details:
- Filename: {image.filename}
- Description: {image.description or 'No description provided'}
- Scan Type: Chest X-ray

Required Output:
- Findings
- Recommendations

Analyze the uploaded X-ray image and provide a detailed interpretation.
"""

    try:
        response = model.generate_content([
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_content}}  # Adjust mime_type if needed
                ]
            }
        ])
        if not response.text:
            raise HTTPException(status_code=500, detail="Empty response from Gemini API")
        gpt_output = response.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

    report = Report(
        patient_id=image.patient_id,
        title=f"AI Report for {image.filename}",
        findings=gpt_output,
        recommendations="See findings section. Generated via Gemini.",
        created_at=datetime.utcnow()
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report