from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.annotations import Annotation
from app.schemas.annotations import AnnotationCreate, AnnotationOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AnnotationOut)
def create_annotation(annotation: AnnotationCreate, db: Session = Depends(get_db)):
    new_ann = Annotation(
        image_id=annotation.image_id,
        label=annotation.label,
        bounding_box=annotation.bounding_box.dict()  # Convert nested model to dict
    )
    db.add(new_ann)
    db.commit()
    db.refresh(new_ann)
    return new_ann

@router.get("/image/{image_id}", response_model=list[AnnotationOut])
def get_annotations_for_image(image_id: int, db: Session = Depends(get_db)):
    return db.query(Annotation).filter(Annotation.image_id == image_id).all()
