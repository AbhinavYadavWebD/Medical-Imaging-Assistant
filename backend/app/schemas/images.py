from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageOut(BaseModel):
    id: int
    patient_id: int
    filename: str
    description: Optional[str] = None
    scan_type: Optional[str] = None
    upload_time: datetime

    class Config:
        orm_mode = True
