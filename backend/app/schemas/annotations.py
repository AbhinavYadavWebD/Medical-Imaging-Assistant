from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x: int = Field(..., example=10)
    y: int = Field(..., example=20)
    width: int = Field(..., example=100)
    height: int = Field(..., example=80)

class AnnotationCreate(BaseModel):
    image_id: int
    label: str
    bounding_box: BoundingBox

class AnnotationOut(AnnotationCreate):
    id: int

    class Config:
        from_attributes = True
