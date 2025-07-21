from sqlalchemy import Column, Integer, String, Date
from app.database.session import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    date_of_birth = Column(Date)
    gender = Column(String)
    contact_number = Column(String)
    address = Column(String)
    reports = relationship("Report", back_populates="patient", cascade="all, delete-orphan")