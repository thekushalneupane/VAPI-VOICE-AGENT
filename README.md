# 👁️ Eye Care Hospital — AI Voice Agent

An AI-powered voice assistant for Eye Care Hospital that handles appointment booking, cancellations, and patient inquiries over the phone — fully integrated with a real-time dashboard for hospital staff.

---

## 🚀 Features

- **Voice Agent (Vikram)** — AI receptionist built on Vapi AI that handles inbound calls
- **Appointment Booking** — patients can book appointments by voice, saved directly to the database
- **Appointment Cancellation** — patients can cancel existing appointments via voice
- **Hospital Information** — Vikram answers questions about services, timings, and location
- **Staff Dashboard** — Streamlit dashboard for hospital staff to view and manage all appointments

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Voice Agent | Vapi AI |
| Backend API | FastAPI + Uvicorn |
| Database | SQLite (via SQLAlchemy ORM) |
| Dashboard | Streamlit |
| Deployment | Railway (backend) |

---

## 📁 Project Structure

```
VAPI-VOICE-AGENT/
├── backend.py        # FastAPI backend with appointment endpoints
├── database.py       # SQLAlchemy models and database setup
├── dashboard.py      # Streamlit dashboard for staff
├── Procfile          # Railway deployment config
├── pyproject.toml    # Project dependencies
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/schedule_appointment/` | Book a new appointment |
| POST | `/cancel_appointment/` | Cancel an existing appointment |
| GET | `/list_appointment/` | List appointments by patient name |
| GET | `/all_appointments/` | Fetch all appointments (for dashboard) |

---

## ⚙️ Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/thekushalneupane/VAPI-VOICE-AGENT.git
cd VAPI-VOICE-AGENT
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Run the backend
```bash
uv run backend.py
```

### 4. Run the dashboard (in a separate terminal)
```bash
uv run streamlit run dashboard.py
```

### 5. Expose backend for Vapi (development only)
```bash
ngrok http 8000
```

---

## 🌐 Deployment

- **Backend** — deployed on [Railway](https://railway.app)
- **Dashboard** — run locally or deploy on [Streamlit Cloud](https://streamlit.io/cloud)

---

## 🤖 Voice Agent (Vikram)

Vikram is configured on Vapi AI with three tools:
- `schedule_appointment` — books appointments via the backend API
- `cancel_appointment` — cancels appointments via the backend API  
- `check_doctors_availability` — checks doctor availability for a given date

---

