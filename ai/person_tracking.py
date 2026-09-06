import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Person tracking started!")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Run YOLO tracking
    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    # Draw tracking results
    annotated_frame = results[0].plot()

    cv2.imshow(
        "Border Surveillance - Person Tracking",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()