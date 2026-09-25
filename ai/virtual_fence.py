import cv2
import time
from ultralytics import YOLO

from alert_database import save_alert


# ==============================
# LOAD YOLO MODEL
# ==============================
model = YOLO("yolo11n.pt")


# ==============================
# WEBCAM
# ==============================
cap = cv2.VideoCapture(0)


# ==============================
# RESTRICTED ZONE
# ==============================
ZONE_X1 = 200
ZONE_Y1 = 150
ZONE_X2 = 450
ZONE_Y2 = 400


# ==============================
# CAMERA ID
# ==============================
CAMERA_ID = "CAM01"


# ==============================
# ALERT COOLDOWN
# ==============================
last_alert_time = {}

ALERT_COOLDOWN = 10   # seconds


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera frame not received.")
        break


    # ==============================
    # YOLO TRACKING
    # ==============================
    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )


    # ==============================
    # DRAW DETECTION
    # ==============================
    annotated = results[0].plot()


    # ==============================
    # DRAW RESTRICTED ZONE
    # ==============================
    cv2.rectangle(
        annotated,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        annotated,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )


    intrusion_detected = False


    # ==============================
    # CHECK DETECTED PERSONS
    # ==============================
    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            # Bounding box
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Person center
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2


            # ==============================
            # TRACKING ID
            # ==============================
            track_id = None

            if box.id is not None:
                track_id = int(box.id[0])


            # ==============================
            # CONFIDENCE
            # ==============================
            confidence = float(box.conf[0])


            # Draw center point
            cv2.circle(
                annotated,
                (cx, cy),
                5,
                (255, 0, 0),
                -1
            )


            # ==============================
            # RESTRICTED ZONE CHECK
            # ==============================
            inside_zone = (
                ZONE_X1 < cx < ZONE_X2
                and
                ZONE_Y1 < cy < ZONE_Y2
            )


            if inside_zone:

                intrusion_detected = True


                # Alert cooldown
                current_time = time.time()

                previous_alert = last_alert_time.get(
                    track_id,
                    0
                )


                if current_time - previous_alert >= ALERT_COOLDOWN:

                    print("\n🚨 INTRUSION DETECTED!")

                    print(
                        "Person ID:",
                        track_id
                    )

                    print(
                        "Confidence:",
                        round(confidence, 2)
                    )


                    # ==============================
                    # SAVE ALERT
                    # ==============================
                    save_alert(
                        camera_id=CAMERA_ID,
                        event_type="PERSON_INTRUSION",
                        confidence=round(confidence, 2),
                        zone="RESTRICTED_ZONE"
                    )


                    # Update alert time
                    last_alert_time[track_id] = current_time


    # ==============================
    # ALERT DISPLAY
    # ==============================
    if intrusion_detected:

        cv2.putText(
            annotated,
            "INTRUSION ALERT!",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )


    # ==============================
    # DISPLAY
    # ==============================
    cv2.imshow(
        "Border Surveillance - Virtual Fence",
        annotated
    )


    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==============================
# RELEASE
# ==============================
cap.release()
cv2.destroyAllWindows()