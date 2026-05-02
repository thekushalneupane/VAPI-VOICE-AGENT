from database import get_db, init_db, Appointment
init_db()

import datetime as dt
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

# --- Pydantic Models ---

class AppointmentRequest(BaseModel):
    patient_name: str
    reason: str
    start_time: dt.datetime

class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    reason: str | None
    start_time: dt.datetime
    canceled: bool
    created_at: dt.datetime

class CancelAppointmentRequest(BaseModel):
    patient_name: str
    start_time: dt.datetime

class CancelAppointmentResponse(BaseModel):
    canceled_count: int

# --- App ---

app = FastAPI()

# Schedule Appointment
@app.post("/schedule_appointment/")
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return AppointmentResponse(
        id=new_appointment.id,
        patient_name=new_appointment.patient_name,
        reason=new_appointment.reason,
        start_time=new_appointment.start_time,
        canceled=new_appointment.canceled,
        created_at=new_appointment.created_at
    )

# Cancel Appointment
@app.post("/cancel_appointment/")
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):
    start_dt = dt.datetime.combine(request.start_time.date(), dt.time(0, 0))
    end_dt = start_dt + dt.timedelta(days=1)

    result = db.execute(
        select(Appointment)
        .where(Appointment.patient_name == request.patient_name)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)
        .where(Appointment.canceled == False)
    )

    appointments = result.scalars().all()

    if not appointments:
        raise HTTPException(status_code=404, detail="No matching appointment found to cancel.")

    for appointment in appointments:
        appointment.canceled = True

    db.commit()

    return CancelAppointmentResponse(canceled_count=len(appointments))

# List Appointments by Patient
@app.get("/list_appointment/")
def list_appointment(patient_name: str, db: Session = Depends(get_db)):
    result = db.execute(
        select(Appointment)
        .where(Appointment.patient_name == patient_name)
    )

    appointments = result.scalars().all()

    return [AppointmentResponse(
        id=a.id,
        patient_name=a.patient_name,
        reason=a.reason,
        start_time=a.start_time,
        canceled=a.canceled,
        created_at=a.created_at
    ) for a in appointments]

# All Appointments (for dashboard)
@app.get("/all_appointments/")
def all_appointments(db: Session = Depends(get_db)):
    result = db.execute(
        select(Appointment).order_by(Appointment.start_time.desc())
    )
    appointments = result.scalars().all()

    return [AppointmentResponse(
        id=a.id,
        patient_name=a.patient_name,
        reason=a.reason,
        start_time=a.start_time,
        canceled=a.canceled,
        created_at=a.created_at
    ) for a in appointments]

import uvicorn
if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000)