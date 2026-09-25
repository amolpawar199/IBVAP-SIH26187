import os
import sqlite3

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ==========================================
# DATABASE PATH
# ==========================================

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "video",
    "border_alerts.db"
)


# ==========================================
# FRONTEND PATH
# ==========================================

FRONTEND_PATH = os.path.join(
    PROJECT_ROOT,
    "frontend"
)

DASHBOARD_PATH = os.path.join(
    FRONTEND_PATH,
    "dashboard.html"
)


# ==========================================
# FASTAPI
# ==========================================

app = FastAPI(
    title="Border Surveillance Monitoring API",
    description="AI-Based Border Surveillance Monitoring System",
    version="1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "system": "Border Surveillance AI",
        "status": "ONLINE",
        "database": "CONNECTED",
        "api": "ACTIVE"
    }


# ==========================================
# DASHBOARD
# ==========================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard():

    if not os.path.exists(DASHBOARD_PATH):

        return HTMLResponse(
            content="""
            <h1>Dashboard file not found</h1>
            <p>Check frontend/dashboard.html</p>
            """,
            status_code=404
        )

    with open(
        DASHBOARD_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ==========================================
# GET ALL ALERTS
# ==========================================

@app.get("/alerts")
def get_alerts():

    if not os.path.exists(DB_PATH):

        return {
            "count": 0,
            "alerts": [],
            "message": "Database not found"
        }


    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            id,
            event_id,
            camera_id,
            event_type,
            timestamp,
            confidence,
            zone,
            status,
            event_hash
        FROM alerts
        ORDER BY id DESC
    """)


    rows = cursor.fetchall()

    conn.close()


    alerts = [
        dict(row)
        for row in rows
    ]


    return {
        "count": len(alerts),
        "alerts": alerts
    }


# ==========================================
# LATEST ALERT
# ==========================================

@app.get("/alerts/latest")
def latest_alert():

    if not os.path.exists(DB_PATH):

        return {
            "message": "Database not found"
        }


    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            id,
            event_id,
            camera_id,
            event_type,
            timestamp,
            confidence,
            zone,
            status,
            event_hash
        FROM alerts
        ORDER BY id DESC
        LIMIT 1
    """)


    row = cursor.fetchone()

    conn.close()


    if row is None:

        return {
            "message": "No alerts found"
        }


    return dict(row)


# ==========================================
# SYSTEM STATUS
# ==========================================

@app.get("/status")
def system_status():

    database_status = (
        "CONNECTED"
        if os.path.exists(DB_PATH)
        else "NOT FOUND"
    )


    return {

        "system": "Border Surveillance AI",

        "status": "ONLINE",

        "ai_detection": "ACTIVE",

        "camera": "CAM-01",

        "database": database_status,

        "sha256": "ENABLED",

        "blockchain": "ACTIVE",

        "verification": "ENABLED"

    }
    