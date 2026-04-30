import streamlit as st
import requests
import datetime as dt
import pandas as pd

# --- Config ---
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Delhi Eye Care Hospital",
    page_icon="👁️",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0a0f1e;
        color: #e8eaf0;
    }

    .main { background-color: #0a0f1e; }

    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
        color: #7eb8f7;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1a5fd4, #0e3a8a);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        transition: 0.2s;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2270e8, #1a5fd4);
        transform: translateY(-1px);
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: #111827 !important;
        color: #e8eaf0 !important;
        border: 1px solid #1f3460 !important;
        border-radius: 8px !important;
    }

    .card {
        background: #111827;
        border: 1px solid #1f3460;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }

    .card-active {
        border-left: 4px solid #1a5fd4;
    }

    .card-canceled {
        border-left: 4px solid #ef4444;
        opacity: 0.6;
    }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .badge-active { background: #1a3a6e; color: #7eb8f7; }
    .badge-canceled { background: #3a1a1a; color: #f87171; }

    .stat-box {
        background: #111827;
        border: 1px solid #1f3460;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }

    .stat-number {
        font-family: 'DM Serif Display', serif;
        font-size: 2.2rem;
        color: #7eb8f7;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #8899aa;
        margin-top: 4px;
    }

    .header-bar {
        background: linear-gradient(135deg, #0e1f3d, #0a0f1e);
        border-bottom: 1px solid #1f3460;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }

    div[data-testid="stSidebar"] {
        background-color: #080d1a !important;
        border-right: 1px solid #1f3460;
    }

    .success-msg {
        background: #0d2a1f;
        border: 1px solid #16a34a;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #4ade80;
        margin-top: 0.5rem;
    }

    .error-msg {
        background: #2a0d0d;
        border: 1px solid #dc2626;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #f87171;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Header ---
st.markdown("""
<div class="header-bar">
    <h1 style="text-align:center; margin:0; font-size:2rem;">👁️ Delhi Eye Care Hospital</h1>
    <p style="text-align:center; color:#8899aa; margin:4px 0 0 0; font-size:0.9rem;">Appointment Management Dashboard</p>
</div>
""", unsafe_allow_html=True)


# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("", ["📋 All Appointments", "➕ Book Appointment", "❌ Cancel Appointment"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='color:#8899aa; font-size:0.8rem;'>Vikram Voice Agent Backend<br>Delhi Eye Care Hospital</div>", unsafe_allow_html=True)


# --- Helper: Fetch All Appointments ---
def fetch_all_appointments():
    try:
        # We'll use the list endpoint with a broad search
        # Since list requires patient_name, we fetch via SQLite directly for dashboard
        from database import SessionLocal, Appointment
        db = SessionLocal()
        appointments = db.query(Appointment).order_by(Appointment.start_time.desc()).all()
        db.close()
        return appointments
    except Exception as e:
        st.error(f"Could not connect to database: {e}")
        return []


# --- Page: All Appointments ---
if page == "📋 All Appointments":
    appointments = fetch_all_appointments()

    # Stats
    total = len(appointments)
    active = sum(1 for a in appointments if not a.canceled)
    canceled = sum(1 for a in appointments if a.canceled)
    today = sum(1 for a in appointments if not a.canceled and a.start_time and a.start_time.date() == dt.date.today())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{total}</div><div class="stat-label">Total Appointments</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{active}</div><div class="stat-label">Active</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{canceled}</div><div class="stat-label">Canceled</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{today}</div><div class="stat-label">Today</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter
    filter_opt = st.selectbox("Filter", ["All", "Active Only", "Canceled Only"])

    st.markdown("### Appointments")

    filtered = appointments
    if filter_opt == "Active Only":
        filtered = [a for a in appointments if not a.canceled]
    elif filter_opt == "Canceled Only":
        filtered = [a for a in appointments if a.canceled]

    if not filtered:
        st.markdown('<div class="card">No appointments found.</div>', unsafe_allow_html=True)
    else:
        for a in filtered:
            card_class = "card-canceled" if a.canceled else "card-active"
            badge_class = "badge-canceled" if a.canceled else "badge-active"
            badge_text = "Canceled" if a.canceled else "Active"
            time_str = a.start_time.strftime("%d %b %Y, %I:%M %p") if a.start_time else "N/A"
            st.markdown(f"""
            <div class="card {card_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong style="font-size:1rem;">{a.patient_name}</strong>
                        <span style="color:#8899aa; margin-left:10px; font-size:0.85rem;">{a.reason or 'N/A'}</span>
                    </div>
                    <span class="badge {badge_class}">{badge_text}</span>
                </div>
                <div style="color:#8899aa; font-size:0.82rem; margin-top:6px;">🕐 {time_str} &nbsp;|&nbsp; ID: #{a.id}</div>
            </div>
            """, unsafe_allow_html=True)


# --- Page: Book Appointment ---
elif page == "➕ Book Appointment":
    st.markdown("### Book New Appointment")

    with st.form("book_form"):
        patient_name = st.text_input("Patient Name")
        reason = st.selectbox("Reason", ["Regular Eye Checkup", "LASIK Consultation", "Cataract Surgery", "Retina Care", "Glaucoma Treatment", "Other"])
        date = st.date_input("Date", min_value=dt.date.today())
        time = st.time_input("Time", value=dt.time(9, 0))
        submitted = st.form_submit_button("Book Appointment")

    if submitted:
        if not patient_name.strip():
            st.markdown('<div class="error-msg">Please enter patient name.</div>', unsafe_allow_html=True)
        else:
            start_time = dt.datetime.combine(date, time)
            payload = {
                "patient_name": patient_name.strip(),
                "reason": reason,
                "start_time": start_time.isoformat()
            }
            try:
                res = requests.post(f"{API_URL}/schedule_appointment/", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.markdown(f'<div class="success-msg">✅ Appointment booked for <strong>{patient_name}</strong> on {start_time.strftime("%d %b %Y at %I:%M %p")}.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-msg">Error: {res.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-msg">Could not reach backend: {e}</div>', unsafe_allow_html=True)


# --- Page: Cancel Appointment ---
elif page == "❌ Cancel Appointment":
    st.markdown("### Cancel Appointment")

    with st.form("cancel_form"):
        patient_name = st.text_input("Patient Name")
        date = st.date_input("Appointment Date")
        submitted = st.form_submit_button("Cancel Appointment")

    if submitted:
        if not patient_name.strip():
            st.markdown('<div class="error-msg">Please enter patient name.</div>', unsafe_allow_html=True)
        else:
            start_time = dt.datetime.combine(date, dt.time(0, 0))
            payload = {
                "patient_name": patient_name.strip(),
                "start_time": start_time.isoformat()
            }
            try:
                res = requests.post(f"{API_URL}/cancel_appointment/", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.markdown(f'<div class="success-msg">✅ Canceled <strong>{data["canceled_count"]}</strong> appointment(s) for <strong>{patient_name}</strong>.</div>', unsafe_allow_html=True)
                elif res.status_code == 404:
                    st.markdown('<div class="error-msg">No matching appointment found.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-msg">Error: {res.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-msg">Could not reach backend: {e}</div>', unsafe_allow_html=True)