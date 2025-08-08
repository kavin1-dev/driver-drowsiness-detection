import cv2

# Step 1: Create a VideoCapture object for the default camera (0)
cap = cv2.VideoCapture(0)

# Step 2: Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Step 3: Read frames in a loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Display the resulting frame
    cv2.imshow("Webcam Feed", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Step 4: Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
