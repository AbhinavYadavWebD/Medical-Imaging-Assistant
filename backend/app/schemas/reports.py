from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReportCreate(BaseModel):
    patient_id: int
    title: str
    findings: str
    recommendations: str
    image_id: Optional[int] = None  

class ReportOut(BaseModel):
    id: int
    patient_id: int
    title: str
    findings: str
    recommendations: str
    created_at: datetime
    patient_name: Optional[str] = "Unknown"
    image_id: Optional[int]

    class Config:
        from_attributes = True
