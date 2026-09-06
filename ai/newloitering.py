import cv2
import sqlite3
import time
from ultralytics import YOLO
from datetime import datetime

# ==========================================
# 1. YOLO MODEL
# ==========================================
model = YOLO("yolo11n.pt")


# ==========================================
# 2. CAMERA
# ==========================================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened!")
    exit()

# Request HD resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# ==========================================
# 3. FULL-SCREEN WINDOW
# ==========================================
WINDOW_NAME = "Border Surveillance - Loitering Detection"

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

cv2.setWindowProperty(
    WINDOW_NAME,
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)


# ==========================================
# 4. FRONT RESTRICTED ZONE
# ==========================================
ZONE_X1 = 150
ZONE_Y1 = 400
ZONE_X2 = 1130
ZONE_Y2 = 700


# ==========================================
# 5. LOITERING TIME
# ==========================================
LOITER_TIME = 3


# ==========================================
# 6. DATABASE
# ==========================================
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


# ==========================================
# 7. PERSON TIMERS
# ==========================================
person_start_time = {}

# Prevent repeated alerts
alerted_persons = set()


print("======================================")
print("   BORDER SURVEILLANCE SYSTEM")
print("   LOITERING DETECTION ACTIVE")
print("======================================")
print("Camera       : CAM-01")
print("Zone         : FRONT RESTRICTED AREA")
print("Loiter Time  :", LOITER_TIME, "seconds")
print("Press Q to exit")
print("======================================")


# ==========================================
# 8. MAIN LOOP
# ==========================================
while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera error!")
        break


    # ======================================
    # AI PERSON DETECTION + TRACKING
    # ======================================
    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )


    # ======================================
    # PROCESS DETECTED PERSONS
    # ======================================
    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            # No tracking ID
            if box.id is None:
                continue

            person_id = int(box.id[0])

            # Person bounding box
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            # ==================================
            # PERSON CENTER POINT
            # ==================================
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2


            # ==================================
            # CHECK FRONT RESTRICTED ZONE
            # ==================================
            inside_zone = (
                ZONE_X1 < cx < ZONE_X2
                and
                ZONE_Y1 < cy < ZONE_Y2
            )


            # ==================================
            # PERSON ENTERED RESTRICTED ZONE
            # ==================================
            if inside_zone:

                # Start timer
                if person_id not in person_start_time:

                    person_start_time[person_id] = time.time()

                    print(
                        f"Person #{person_id} "
                        f"entered restricted zone"
                    )


                # Calculate time
                elapsed = (
                    time.time()
                    -
                    person_start_time[person_id]
                )


                # ==================================
                # LOITERING DETECTED
                # ==================================
                if elapsed >= LOITER_TIME:

                    # Alert text
                    cv2.putText(
                        frame,
                        f"LOITERING ALERT - PERSON #{person_id}",
                        (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 0, 255),
                        3
                    )


                    # ==================================
                    # SAVE ALERT ONLY ONCE
                    # ==================================
                    if person_id not in alerted_persons:

                        timestamp = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )


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
                            f"stayed for "
                            f"{elapsed:.1f} seconds"
                        )


                # ==================================
                # SHOW TIMER
                # ==================================
                else:

                    cv2.putText(
                        frame,
                        f"Person #{person_id} | "
                        f"{elapsed:.1f}s",
                        (
                            x1,
                            max(y1 - 10, 30)
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
                    )


            # ==================================
            # PERSON LEFT ZONE
            # ==================================
            else:

                person_start_time.pop(
                    person_id,
                    None
                )


    # ==========================================
    # YOLO ANNOTATION
    # ==========================================
    annotated = results[0].plot()


    # ==========================================
    # DRAW FRONT RESTRICTED ZONE
    # ==========================================
    cv2.rectangle(
        annotated,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        4
    )


    # ==========================================
    # ZONE LABEL
    # ==========================================
    cv2.putText(
        annotated,
        "RESTRICTED ZONE",
        (
            ZONE_X1 + 20,
            ZONE_Y1 + 40
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 255),
        3
    )


    # ==========================================
    # CAMERA INFORMATION
    # ==========================================
    cv2.putText(
        annotated,
        "CAM-01 | AI SURVEILLANCE ACTIVE",
        (30, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


    # ==========================================
    # FULL-SCREEN DISPLAY
    # ==========================================
    cv2.imshow(
        WINDOW_NAME,
        annotated
    )


    # ==========================================
    # PRESS Q TO EXIT
    # ==========================================
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# 9. CLEANUP
# ==========================================
cap.release()

connection.close()

cv2.destroyAllWindows()

print("======================================")
print("   SYSTEM STOPPED")
print("======================================")