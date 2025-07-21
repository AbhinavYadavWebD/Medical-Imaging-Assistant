from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database.session import SessionLocal
from app.models.reports import Report
from app.models.patients import Patient
from app.schemas import reports as report_schema

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=report_schema.ReportOut)
def create_report(report: report_schema.ReportCreate, db: Session = Depends(get_db)):
    new_report = Report(**report.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return report_schema.ReportOut.from_orm(new_report)

@router.put("/{report_id}", response_model=report_schema.ReportOut)
def update_report(report_id: int, updated: report_schema.ReportCreate, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated.dict().items():
        setattr(report, key, value)

    db.commit()
    db.refresh(report)
    return report_schema.ReportOut.from_orm(report)

@router.delete("/{report_id}", status_code=204)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"message": "Report deleted"}

@router.get("/", response_model=list[report_schema.ReportOut])
def get_all_reports(query: str = "", db: Session = Depends(get_db)):
    reports = db.query(Report).options(joinedload(Report.patient)).all()
    results = []
    for report in reports:
        patient_name = report.patient.full_name if report.patient else "Unknown"
        report_data = report_schema.ReportOut.from_orm(report).dict()
        report_data["patient_name"] = patient_name
        results.append(report_data)
    return results

@router.get("/{report_id}", response_model=report_schema.ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).options(joinedload(Report.patient)).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    patient_name = report.patient.full_name if report.patient else "Unknown"
    report_data = report_schema.ReportOut.from_orm(report).dict()
    report_data["patient_name"] = patient_name
    return report_data
