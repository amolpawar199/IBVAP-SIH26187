import cv2

# Open the default webcam (0 is usually the built-in webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam opened successfully! Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Can't receive frame.")
        break

    # Display the resulting frame
    cv2.imshow('OpenCV Webcam Test', frame)

    # Stop the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam capture and close all windows
cap.release()
cv2.destroyAllWindows() 
