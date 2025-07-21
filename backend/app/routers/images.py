import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import SessionLocal
from app.models.images import Image
from app.models.patients import Patient
from app.schemas.images import ImageOut

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ImageOut)
def upload_image(
    patient_id: int = Form(...),
    description: str = Form(None),
    scan_type: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    image = Image(
        patient_id=patient_id,
        filename=file.filename,
        description=description,
        scan_type=scan_type,
        upload_time=datetime.utcnow()
    )

    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.get("/", response_model=list[ImageOut])
def get_all_images(db: Session = Depends(get_db)):
    return db.query(Image).all()

@router.get("/patient/{patient_id}", response_model=list[ImageOut])
def get_images_by_patient(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Image).filter(Image.patient_id == patient_id).all()
