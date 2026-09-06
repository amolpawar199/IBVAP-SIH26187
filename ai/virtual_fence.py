import cv2
from ultralytics import YOLO

# Load model
model = YOLO("yolo11n.pt")

# Webcam
cap = cv2.VideoCapture(0)

# Restricted Zone Coordinates
ZONE_X1 = 200
ZONE_Y1 = 150
ZONE_X2 = 450
ZONE_Y2 = 400

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    # Draw Restricted Zone
    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0,0,255),
        2
    )

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,0,255),
        2
    )

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Person center
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Draw center point
            cv2.circle(frame, (cx, cy), 5, (255,0,0), -1)

            # Check intrusion
            if (ZONE_X1 < cx < ZONE_X2 and
                ZONE_Y1 < cy < ZONE_Y2):

                cv2.putText(
                    frame,
                    "INTRUSION ALERT!",
                    (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3
                )

    annotated = results[0].plot()

    # Combine drawings
    frame = annotated

    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0,0,255),
        2
    )

    cv2.imshow("Virtual Fence", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows() 