from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String)
    description = Column(String, nullable=True)
    scan_type = Column(String, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    reports = relationship("Report", back_populates="image", uselist=False)

    patient = relationship("Patient", backref="images")
    annotations = relationship("Annotation", back_populates="image", cascade="all, delete-orphan")

