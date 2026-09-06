from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI(
    title="Border Surveillance AI",
    description="AI-Based Intelligent Video Analytics Platform",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "system": "Border Surveillance AI",
        "status": "Online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/events")
def get_events():

    connection = sqlite3.connect("../ai/border_surveillance.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            person_id,
            camera_id,
            event_type,
            severity,
            timestamp
        FROM events
        ORDER BY id DESC
    """)

    events = cursor.fetchall()
    connection.close()

    return {
        "total_events": len(events),
        "events": [dict(event) for event in events]
    }


@app.get("/events/table", response_class=HTMLResponse)
def events_table():

    connection = sqlite3.connect("../ai/border_surveillance.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            person_id,
            camera_id,
            event_type,
            severity,
            timestamp
        FROM events
        ORDER BY id DESC
    """)

    events = cursor.fetchall()
    connection.close()

    html = """
    <html>
    <head>
        <title>Border Surveillance - Events</title>
        <style>
            body {
                font-family: Arial;
                margin: 40px;
                background: #f4f4f4;
            }

            h1 {
                text-align: center;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
            }

            th, td {
                padding: 12px;
                border: 1px solid #ddd;
                text-align: center;
            }

            th {
                background: #222;
                color: white;
            }

            tr:nth-child(even) {
                background: #f2f2f2;
            }
        </style>
    </head>

    <body>

        <h1>Border Surveillance Event Log</h1>

        <table>
            <tr>
                <th>ID</th>
                <th>Person ID</th>
                <th>Camera</th>
                <th>Event Type</th>
                <th>Severity</th>
                <th>Timestamp</th>
            </tr>
    """

    for event in events:
        html += f"""
            <tr>
                <td>{event[0]}</td>
                <td>Person #{event[1]}</td>
                <td>{event[2]}</td>
                <td>{event[3]}</td>
                <td>{event[4]}</td>
                <td>{event[5]}</td>
            </tr>
        """

    html += """
        </table>

    </body>
    </html>
    """

    return html