import sqlite3
from datetime import datetime

# Create / open database
connection = sqlite3.connect("border_surveillance.db")

cursor = connection.cursor()

# Create events table
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    camera_id TEXT,
    event_type TEXT,
    severity TEXT,
    timestamp TEXT
)
""")

connection.commit()


def save_event(person_id, camera_id, event_type, severity):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO events
    (person_id, camera_id, event_type, severity, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        person_id,
        camera_id,
        event_type,
        severity,
        timestamp
    ))

    connection.commit()

    print("Event saved successfully!")
    print("Person ID:", person_id)
    print("Camera:", camera_id)
    print("Event:", event_type)
    print("Severity:", severity)
    print("Time:", timestamp)


# Test event
save_event(
    person_id=1,
    camera_id="CAM-01",
    event_type="Restricted Zone Intrusion",
    severity="HIGH"
)

connection.close()