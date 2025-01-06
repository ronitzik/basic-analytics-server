from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta
from typing import Any, List

# Create the FastAPI app
app = FastAPI()

# SQLite connection function with timeout and WAL enabled
def get_db_connection():
    conn = sqlite3.connect("events.db", timeout=10)  # Wait up to 10 seconds for the lock
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Create the events table if it doesn't exist
def create_events_table():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eventtimestamputc TEXT NOT NULL,
                userid TEXT NOT NULL,
                eventname TEXT NOT NULL
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

# Call the function to create the table when the app starts
create_events_table()

# Define the request body model using Pydantic
class GetReportsRequest(BaseModel):
    lastseconds: int
    userid: str

class Event(BaseModel):
    userid: str
    eventname: str

# Define the response model using Pydantic
class ReportResponse(BaseModel):
    eventtimestamputc: str
    userid: str
    eventname: str

# Root endpoint to show a welcome message
@app.get("/")
async def root():
    """
    Welcome endpoint to display a message when the app loads.

    Returns:
    - A welcome message as a dictionary.
    """
    return {"message": "Welcome to my app!"}

# POST endpoint to process the event
@app.post("/process_event")
async def process_event(event: Event) -> dict[str, Any]:
    """
    Process event and store it in the SQLite database.

    Parameters:
    - event: Event object containing userid and eventname

    Returns:
    - A response message indicating the success or failure of the operation
    """
    # Get the current UTC timestamp
    event_timestamp_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Connect to the database and insert the event data
    conn = get_db_connection()
    try:
        # Insert event data into the table
        conn.execute(
            "INSERT INTO events (eventtimestamputc, userid, eventname) VALUES (?, ?, ?)",
            (event_timestamp_utc, event.userid, event.eventname)
        )
        conn.commit()
        return {"message": "Event processed successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# POST endpoint to get reports based on last X seconds for a given userid
@app.post("/get_reports")
async def get_reports(request: GetReportsRequest) -> List[ReportResponse]:
    """
    Get reports for a specific user that happened within the last X seconds.

    Parameters:
    - request: A request object containing lastseconds (int) and userid (str)

    Returns:
    - A list of events that occurred within the last X seconds for the given user
    """
    # Calculate the time threshold (X seconds ago from now)
    time_threshold = datetime.utcnow() - timedelta(seconds=request.lastseconds)
    time_threshold_str = time_threshold.strftime('%Y-%m-%d %H:%M:%S')

    # Connect to the database and query for events within the time range
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT eventtimestamputc, userid, eventname FROM events WHERE userid = ? AND eventtimestamputc >= ?",
            (request.userid, time_threshold_str)
        )
        rows = cursor.fetchall()

        # Prepare the response list
        reports = [
            ReportResponse(
                eventtimestamputc=row["eventtimestamputc"],
                userid=row["userid"],
                eventname=row["eventname"]
            )
            for row in rows
        ]

        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
