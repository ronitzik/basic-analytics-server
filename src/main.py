from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from typing import Any

# Create the FastAPI app
app = FastAPI()

# SQLite connection function with timeout and WAL enabled
def get_db_connection():
    conn = sqlite3.connect("events.db", timeout=10)  # Wait up to 10 seconds for the lock
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn


# Define the data model for the request body using Pydantic
class Event(BaseModel):
    userid: str
    eventname: str

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
