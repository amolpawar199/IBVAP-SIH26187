import cv2
import sqlite3
import time
from ultralytics import YOLO
from datetime import datetime

model = YOLO("yolo11n.pt")
cap = cv2.VideoCapture(0)

# Restricted zone
ZONE_X1 = 200
ZONE_Y1 = 150
ZONE_X2 = 450
ZONE_Y2 = 400

# Loitering time
LOITER_TIME = 10

# Database
connection = sqlite3.connect("border_surveillance.db")
cursor = connection.cursor()

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

# Store entry time of each person
person_start_time = {}

# Prevent repeated alerts
alerted_persons = set()

print("Loitering Detection Started!")
print("Press 'q' to quit.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        break

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            if box.id is None:
                continue

            person_id = int(box.id[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Centre point
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            inside_zone = (
                ZONE_X1 < cx < ZONE_X2 and
                ZONE_Y1 < cy < ZONE_Y2
            )

            if inside_zone:

                # Start timer when person enters
                if person_id not in person_start_time:
                    person_start_time[person_id] = time.time()

                elapsed = time.time() - person_start_time[person_id]

                # Loitering detected
                if elapsed >= LOITER_TIME:

                    cv2.putText(
                        frame,
                        f"LOITERING ALERT - PERSON #{person_id}",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        3
                    )

                    # Save only once
                    if person_id not in alerted_persons:

                        timestamp = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                        cursor.execute("""
                        INSERT INTO events
                        (person_id, camera_id, event_type, severity, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                        """, (
                            person_id,
                            "CAM-01",
                            "Loitering in Restricted Zone",
                            "HIGH",
                            timestamp
                        ))

                        connection.commit()

                        alerted_persons.add(person_id)

                        print(
                            f"[LOITERING ALERT] "
                            f"Person #{person_id} "
                            f"stayed for {elapsed:.1f} seconds"
                        )

                else:

                    cv2.putText(
                        frame,
                        f"Person #{person_id}: "
                        f"{elapsed:.1f}s",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

            else:

                # Remove timer when person leaves
                person_start_time.pop(person_id, None)

    # Draw restricted zone
    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    # Display detections
    annotated = results[0].plot()

    # Draw zone again after annotation
    cv2.rectangle(
        annotated,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "Border Surveillance - Loitering Detection",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
connection.close()
cv2.destroyAllWindows()