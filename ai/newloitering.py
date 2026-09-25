import cv2
import time
import sys
import os

from ultralytics import YOLO


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


# ==========================================
# DATABASE IMPORT
# ==========================================

from alert_database import (
    create_database,
    save_alert
)


# ==========================================
# BLOCKCHAIN IMPORT
# ==========================================

from blockchain.blockchain import Blockchain


# ==========================================
# YOLO MODEL
# ==========================================

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "ai",
    "yolo11n.pt"
)

model = YOLO(MODEL_PATH)


# ==========================================
# DATABASE
# ==========================================

create_database()


# ==========================================
# BLOCKCHAIN
# ==========================================

blockchain = Blockchain()


print("\n======================================")
print("     BORDER SURVEILLANCE AI")
print("======================================")

print("Database   : CONNECTED")
print("SHA-256    : ENABLED")
print("Blockchain : CONNECTED")


# ==========================================
# CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Camera could not be opened!")

    exit()


# ==========================================
# HD RESOLUTION
# ==========================================

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)


# ==========================================
# FULL SCREEN
# ==========================================

WINDOW_NAME = (
    "Border Surveillance - AI Monitoring"
)

cv2.namedWindow(
    WINDOW_NAME,
    cv2.WINDOW_NORMAL
)

cv2.setWindowProperty(
    WINDOW_NAME,
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)


# ==========================================
# RESTRICTED ZONE
# ==========================================

ZONE_X1 = 150
ZONE_Y1 = 400

ZONE_X2 = 1130
ZONE_Y2 = 700


# ==========================================
# LOITERING TIME
# ==========================================

LOITER_TIME = 3


# ==========================================
# PERSON TIMERS
# ==========================================

person_start_time = {}

alerted_persons = set()


print("\nCamera      : CAM-01")
print("Zone        : FRONT RESTRICTED AREA")
print("Loiter Time :", LOITER_TIME, "seconds")
print("Press Q to exit")

print("======================================")


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:

        print("Camera error!")

        break


    # ======================================
    # YOLO DETECTION + TRACKING
    # ======================================

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )


    # ======================================
    # PROCESS PERSONS
    # ======================================

    for result in results:

        if result.boxes is None:
            continue


        for box in result.boxes:

            if box.id is None:
                continue


            # Person ID
            person_id = int(
                box.id[0]
            )


            # Bounding box
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            # Confidence
            confidence = float(
                box.conf[0]
            )


            # Center point
            cx = (
                x1 + x2
            ) // 2

            cy = (
                y1 + y2
            ) // 2


            # ==================================
            # CHECK ZONE
            # ==================================

            inside_zone = (

                ZONE_X1 < cx < ZONE_X2

                and

                ZONE_Y1 < cy < ZONE_Y2
            )


            # ==================================
            # INSIDE RESTRICTED ZONE
            # ==================================

            if inside_zone:


                # Start timer
                if person_id not in person_start_time:

                    person_start_time[
                        person_id
                    ] = time.time()

                    print(
                        f"Person #{person_id} "
                        "entered restricted zone"
                    )


                # Calculate time
                elapsed = (

                    time.time()

                    -

                    person_start_time[
                        person_id
                    ]
                )


                # ==================================
                # LOITERING
                # ==================================

                if elapsed >= LOITER_TIME:


                    cv2.putText(
                        frame,
                        (
                            f"LOITERING ALERT - "
                            f"PERSON #{person_id}"
                        ),
                        (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 0, 255),
                        3
                    )


                    # ==================================
                    # SAVE ONLY ONCE
                    # ==================================

                    if person_id not in alerted_persons:


                        print(
                            "\n🚨 LOITERING ALERT DETECTED"
                        )


                        # ==================================
                        # SAVE DATABASE
                        # ==================================

                        event_data, event_hash = save_alert(

                            camera_id="CAM-01",

                            event_type=(
                                "LOITERING_IN_"
                                "RESTRICTED_ZONE"
                            ),

                            confidence=confidence,

                            zone="FRONT_RESTRICTED_AREA"
                        )


                        print(
                            "✓ Alert saved to SQLite"
                        )


                        # ==================================
                        # ADD HASH
                        # ==================================

                        event_data[
                            "event_hash"
                        ] = event_hash


                        # ==================================
                        # BLOCKCHAIN
                        # ==================================

                        block = blockchain.add_event(
                            event_data
                        )


                        print(
                            "✓ Alert recorded "
                            "on blockchain"
                        )


                        # ==================================
                        # BLOCKCHAIN RECORD
                        # ==================================

                        print(
                            "\n===== "
                            "BLOCKCHAIN RECORD ====="
                        )

                        print(
                            "Block Index :",
                            block["index"]
                        )

                        print(
                            "Event ID    :",
                            event_data["event_id"]
                        )

                        print(
                            "Event Hash  :",
                            event_hash
                        )

                        print(
                            "Block Hash  :",
                            block["hash"]
                        )


                        # ==================================
                        # VERIFY
                        # ==================================

                        if blockchain.verify_chain():

                            print(
                                "✓ Blockchain "
                                "integrity: VALID"
                            )

                        else:

                            print(
                                "🚨 Blockchain "
                                "integrity: INVALID"
                            )


                        alerted_persons.add(
                            person_id
                        )


                # ==================================
                # SHOW TIMER
                # ==================================

                else:

                    cv2.putText(

                        frame,

                        (
                            f"Person #{person_id} | "
                            f"{elapsed:.1f}s"
                        ),

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
    # DRAW ZONE
    # ==========================================

    cv2.rectangle(

        annotated,

        (
            ZONE_X1,
            ZONE_Y1
        ),

        (
            ZONE_X2,
            ZONE_Y2
        ),

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
    # CAMERA STATUS
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
    # DISPLAY
    # ==========================================

    cv2.imshow(
        WINDOW_NAME,
        annotated
    )


    # ==========================================
    # EXIT
    # ==========================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()

print("\n======================================")
print("        SYSTEM STOPPED")
print("======================================")