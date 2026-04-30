# STEP 1: Import necessary libraries and modules(database objects, SQLAlchemy engine, session, and base class)



from database import get_db, init_db, Appointment
init_db()




# STEP 3: Create data contracts (Pydantic models) for request validation and response formatting
import datetime as dt
from pydantic import BaseModel


class AppointmentRequest(BaseModel):
    patient_name: str
    reason: str
    start_time: dt.datetime  # ISO format datetime string


class AppointmentResponse(BaseModel):
    id : int
    patient_name: str
    reason: str | None
    start_time: dt.datetime  # ISO format datetime string
    canceled: bool
    created_at: dt.datetime  # ISO format datetime string

class CancelAppointmentRequest(BaseModel):
    patient_name: str
    start_time: dt.datetime  # ISO format datetime string

class CancelAppointmentResponse(BaseModel):
    canceled_count: int


# STEP 2: Create FASTAPI application and define API endpoints for CRUD operations on appointments

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

app = FastAPI()

#schedule appointment
@app.post("/schedule_appointment/")
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    #logic to add appointment to the database using SQLAlchemy session
    new_appointment = Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)  # Refresh to get the generated ID and timestamps

    new_appointment_return_obj = AppointmentResponse(
        id = new_appointment.id,
        patient_name = new_appointment.patient_name,
        reason = new_appointment.reason,
        start_time = new_appointment.start_time,
        canceled = new_appointment.canceled,
        created_at = new_appointment.created_at
    )

    return new_appointment_return_obj



#cancel appointment

from sqlalchemy import select

@app.post("/cancel_appointment/")
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):
    #logic to cancel appointment from the database using SQLAlchemy session

    start_dt = dt.datetime.combine(request.date(), dt.time.min)  # Start of the day
    end_dt = start_dt + dt.timedelta(days=1)  # End of the day

    result = db.execute(
        select(Appointment)
        .where(
            Appointment.patient_name == request.patient_name,
            Appointment.start_time >= request.start_dt,
            Appointment.start_time < request.start_dt,
            Appointment.canceled == False  # Assuming appointments are 30 minutes long
        )
    )

    appointments = result.scalars().all()

    if not appointments:
        raise HTTPException(status_code=404, detail="No matching appointment found to cancel.")
    
    for appointment in appointments:
        appointment.canceled = True  # Mark the appointment as canceled

    db.commit()  # Commit the changes to the database

    return CancelAppointmentResponse(canceled_count=len(appointments))



#list appointments
@app.get("/list_appointment/")
def list_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    #logic to retrieve all appointments from the database using SQLAlchemy session

    start_dt = dt.datetime.combine(request.date(), dt.time.min)  # Start of the day
    end_dt = start_dt + dt.timedelta(days=1)  # End of the day

    result = db.execute(
        select(Appointment)
        .where(
            Appointment.patient_name == request.patient_name,
            Appointment.start_time >= request.start_time,
            Appointment.canceled == False
        )
    )

    booked_appointments = []
    for appointment in appointments:
        appointment_obj = AppointmentResponse(
            id=appointment.id,
            patient_name=appointment.patient_name,
            reason=appointment.reason,
            start_time=appointment.start_time,
            canceled=appointment.canceled,
            created_at=appointment.created_at
        )
    appointment_objects.append(booked_appointments)


    return booked_appointments

import uvicorn
if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8000)




# STEP 4: Write actual code to handle database operations (using SQLAlchemy sessions) for each API endpoint


# STEP 5: Streamlit dashboard code to visualize appointments data (optional, can be in a separate file)