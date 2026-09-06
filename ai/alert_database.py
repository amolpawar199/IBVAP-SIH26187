import cv2
import sqlite3
import sys
import os
from datetime import datetime
from ultralytics import YOLO

# ============================================================
# IMPORT BLOCKCHAIN
# ============================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from blockcahin  import Blockchain


# ============================================================
# AI MODEL
# ============================================================

model = YOLO("yolo11n.pt")

# Webcam
cap = cv2.VideoCapture(0)

# Camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# ============================================================
# RESTRICTED ZONE
# ============================================================

ZONE_X1 = 150
ZONE_Y1 = 400
ZONE_X2 = 1130
ZONE_Y2 = 700


# ============================================================
# DATABASE
# ============================================================

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


# ============================================================
# BLOCKCHAIN
# ============================================================

blockchain = Blockchain()


# ============================================================
# PREVENT REPEATED ALERTS
# ============================================================

person_inside = set()


# ============================================================
# START SYSTEM
# ============================================================

print("=" * 60)
print(" SENTINELVISION AI - BORDER SURVEILLANCE")
print("=" * 60)

print("AI Detection       : ONLINE")
print("Database           : ONLINE")
print("Blockchain         : ONLINE")
print("Camera             : CAM-01")
print("=" * 60)

print("Press 'q' to quit.")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        break


    # ========================================================
    # YOLO PERSON DETECTION + TRACKING
    # ========================================================

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )


    # ========================================================
    # PROCESS DETECTIONS
    # ========================================================

    for result in results:

        if result.boxes is None:
            continue


        for box in result.boxes:

            # Make sure tracking ID exists
            if box.id is None:
                continue


            # Person ID
            person_id = int(box.id[0])


            # Bounding box
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            # =================================================
            # PERSON CENTRE
            # =================================================

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2


            # =================================================
            # CHECK RESTRICTED ZONE
            # =================================================

            inside_zone = (
                ZONE_X1 < cx < ZONE_X2
                and
                ZONE_Y1 < cy < ZONE_Y2
            )


            # =================================================
            # PERSON ENTERED ZONE
            # =================================================

            if inside_zone:

                # Alert only once per entry
                if person_id not in person_inside:

                    person_inside.add(person_id)


                    # =========================================
                    # TIMESTAMP
                    # =========================================

                    timestamp = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )


                    # =========================================
                    # EVENT INFORMATION
                    # =========================================

                    event_type = "Restricted Zone Intrusion"
                    severity = "HIGH"
                    camera_id = "CAM-01"


                    # =========================================
                    # SAVE EVENT TO SQLITE
                    # =========================================

                    cursor.execute("""
                    INSERT INTO events
                    (
                        person_id,
                        camera_id,
                        event_type,
                        severity,
                        timestamp
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        person_id,
                        camera_id,
                        event_type,
                        severity,
                        timestamp
                    ))


                    connection.commit()


                    # =========================================
                    # BLOCKCHAIN EVENT
                    # =========================================

                    event_data = {

                        "person_id": person_id,

                        "camera_id": camera_id,

                        "event_type": event_type,

                        "severity": severity,

                        "timestamp": timestamp
                    }


                    # Add event to blockchain
                    block = blockchain.add_event(
                        event_data
                    )


                    # =========================================
                    # CONSOLE ALERT
                    # =========================================

                    print()
                    print("=" * 60)
                    print("🚨 SECURITY ALERT")
                    print("=" * 60)

                    print(
                        f"Person ID     : {person_id}"
                    )

                    print(
                        f"Camera        : {camera_id}"
                    )

                    print(
                        f"Event         : {event_type}"
                    )

                    print(
                        f"Severity      : {severity}"
                    )

                    print(
                        f"Time          : {timestamp}"
                    )

                    print()
                    print("🔗 BLOCKCHAIN RECORD")

                    print(
                        f"Block Index   : {block['index']}"
                    )

                    print(
                        f"Event Hash    : {block['hash']}"
                    )

                    print(
                        f"Previous Hash : {block['previous_hash']}"
                    )

                    print("=" * 60)


            # =================================================
            # PERSON LEFT ZONE
            # =================================================

            else:

                person_inside.discard(
                    person_id
                )


    # ========================================================
    # DRAW RESTRICTED ZONE
    # ========================================================

    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        3
    )


    # ========================================================
    # ZONE LABEL
    # ========================================================

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )


    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    cv2.putText(
        frame,
        "CAM-01 | AI SURVEILLANCE ACTIVE",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )


    # ========================================================
    # SHOW YOLO RESULT
    # ========================================================

    annotated = results[0].plot()


    # Draw zone again over YOLO output
    cv2.rectangle(
        annotated,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        3
    )


    cv2.putText(
        annotated,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )


    cv2.putText(
        annotated,
        "CAM-01 | AI SURVEILLANCE ACTIVE",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.imshow(
        "SentinelVision AI - Border Surveillance",
        annotated
    )


    # ========================================================
    # QUIT
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

print()
print("Checking blockchain integrity...")

print(
    "Blockchain valid:",
    blockchain.verify_chain()
)


cap.release()

connection.close()

cv2.destroyAllWindows()

print("System stopped.")