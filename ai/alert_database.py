import sqlite3
import json
import hashlib
import os
from datetime import datetime


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# ==========================================
# DATABASE PATH
# ==========================================

DB_FOLDER = os.path.join(
    PROJECT_ROOT,
    "video"
)

os.makedirs(DB_FOLDER, exist_ok=True)

DB_NAME = os.path.join(
    DB_FOLDER,
    "border_alerts.db"
)


# ==========================================
# SHA-256 HASH
# ==========================================

def generate_hash(event_data):

    event_string = json.dumps(
        event_data,
        sort_keys=True
    )

    return hashlib.sha256(
        event_string.encode("utf-8")
    ).hexdigest()


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT UNIQUE,
            camera_id TEXT,
            event_type TEXT,
            timestamp TEXT,
            confidence REAL,
            zone TEXT,
            status TEXT,
            event_hash TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


# ==========================================
# SAVE ALERT
# ==========================================

def save_alert(camera_id, event_type, confidence, zone):

    event_id = "EVT" + datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )

    timestamp = datetime.now().isoformat()

    event_data = {
        "event_id": event_id,
        "camera_id": camera_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "confidence": confidence,
        "zone": zone,
        "status": "UNVERIFIED"
    }

    event_hash = generate_hash(event_data)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts
        (
            event_id,
            camera_id,
            event_type,
            timestamp,
            confidence,
            zone,
            status,
            event_hash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_id,
        camera_id,
        event_type,
        timestamp,
        confidence,
        zone,
        "UNVERIFIED",
        event_hash
    ))

    conn.commit()
    conn.close()

    print("\n========== ALERT SAVED ==========")
    print("Event ID   :", event_id)
    print("Camera     :", camera_id)
    print("Event      :", event_type)
    print("Confidence :", confidence)
    print("Zone       :", zone)
    print("Status     : UNVERIFIED")
    print("SHA-256    :", event_hash)
    print("=================================")

    return event_data, event_hash


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    create_database()

    save_alert(
        camera_id="CAM-01",
        event_type="PERSON_DETECTED",
        confidence=0.91,
        zone="RESTRICTED_ZONE"
    )

    print("\nDatabase test completed.")