from __future__ import annotations  # Allows modern type hints in older Python versions

from sqlalchemy import text  # Wraps raw SQL strings so SQLAlchemy can execute them

from database import engine, init_db  # Import DB connection and table creator

def run_sql(quer: str):
    init_db()  # Create tables if they don't exist yet

    with engine.begin() as connection:  # Open a transaction (auto commits on success)
        result = connection.execute(text(quer))  # Execute the SQL query
        return result.fetchall() if result.returns_rows else result.rowcount
        # If SELECT — return all rows, if INSERT/UPDATE/DELETE — return affected row count


#query = "INSERT INTO appointments (patient_name, reason, start_time, canceled, created_at) VALUES ('John Doe', 'Checkup', '2026-05-01 10:00:00', False, '2026-04-30 12:00:00')"  # Example SQL query to insert an appointment
query = "SELECT * FROM appointments"  # Example SQL query to select all appointments
print(run_sql(query))  # Run the query and print the results