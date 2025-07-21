from app.database.session import Base, engine
from app.models import users, patients ,reports,images,annotations
from app.database.session import SessionLocal  
from sqlalchemy.orm import Session

def init_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()