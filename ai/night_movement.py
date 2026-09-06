import cv2
from ultralytics import YOLO
from datetime import datetime

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)

# Brightness threshold
NIGHT_THRESHOLD = 70

print("Night Movement Detection Started!")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        break

    # Calculate average brightness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = gray.mean()

    # Person detection
    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    person_detected = False

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            confidence = float(box.conf[0])

            if confidence > 0.5:
                person_detected = True

    # Night movement condition
    if brightness < NIGHT_THRESHOLD and person_detected:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cv2.putText(
            frame,
            "NIGHT MOVEMENT ALERT!",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )

        print(
            f"[NIGHT ALERT] Person detected "
            f"at {timestamp}"
        )

    else:

        cv2.putText(
            frame,
            "SYSTEM NORMAL",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.putText(
        frame,
        f"Brightness: {brightness:.1f}",
        (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    annotated = results[0].plot()

    cv2.imshow(
        "Border Surveillance - Night Detection",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()