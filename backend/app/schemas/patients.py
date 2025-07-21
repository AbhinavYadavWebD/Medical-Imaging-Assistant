from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import relationship

class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    contact_number: str
    address: str

class PatientOut(PatientCreate):
    id: int
    
    class Config:
        orm_mode = True
