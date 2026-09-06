import cv2
from ultralytics import YOLO
from datetime import datetime

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)

ZONE_X1 = 200
ZONE_Y1 = 150
ZONE_X2 = 450
ZONE_Y2 = 400

alert_active = False

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

    intrusion_detected = False

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            track_id = "Unknown"

            if box.id is not None:
                track_id = int(box.id[0])

            # Check restricted zone
            if (
                ZONE_X1 < cx < ZONE_X2
                and
                ZONE_Y1 < cy < ZONE_Y2
            ):

                intrusion_detected = True

                current_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                print(
                    f"[ALERT] Person #{track_id} "
                    f"entered restricted zone at "
                    f"{current_time}"
                )

    # Draw detection
    annotated_frame = results[0].plot()

    # Draw restricted zone
    cv2.rectangle(
        annotated_frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        2
    )

    if intrusion_detected:

        cv2.putText(
            annotated_frame,
            "INTRUSION ALERT!",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.putText(
            annotated_frame,
            "RESTRICTED AREA",
            (ZONE_X1, ZONE_Y2 + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    else:

        cv2.putText(
            annotated_frame,
            "SYSTEM NORMAL",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Border Surveillance - Alert System",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()