#Lalith Aditya Chunduri
#Resources: AI, ImageSearchTutorial, OpenCv Tutorial
import cv2 as cv
import numpy as np
import time

# Initialize webcam
webcam = cv.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

frame_width = int(webcam.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(webcam.get(cv.CAP_PROP_FRAME_HEIGHT))

# Initialize background subtractor for motion detection
background_subtractor = cv.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
video_writer = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))

# State variables to track motion and recording status
motion_detected = False
last_motion_time = time.time()
current_state = "Vacant"

# Function to handle trackbar events
def nothing(x):
    pass

# Create a window with trackbars for Canny edge detection thresholds
cv.namedWindow('controls')
cv.createTrackbar("lower", 'controls', 0, 225, nothing)
cv.setTrackbarPos("lower", 'controls', 43)
cv.createTrackbar("upper", 'controls', 0, 225, nothing)
cv.setTrackbarPos("upper", 'controls', 127)

# Main loop to process each frame of the video stream
while True:
    ret, frame = webcam.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert the frame to grayscale and apply Gaussian blur to reduce noise
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (7, 7), 0)

    #Detect the foreground (moving objects) using background subtraction
    foreground_mask = background_subtractor.apply(blurred)
    _, foreground_mask = cv.threshold(foreground_mask, 250, 255, cv.THRESH_BINARY)

    #Find contours in the foreground mask
    contours, _ = cv.findContours(foreground_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    motion_detected = False

    #Analyze contours and draw bounding rectangle
    if contours:
        # Sort contours by area and select the largest one
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        largest_contour = contours[0]

        # Draw bounding rectangle
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        motion_detected = True

    #Update the state based on motion detection
    if motion_detected:
        last_motion_time = time.time()  # Update the last motion time
        current_state = "Object"
    elif time.time() - last_motion_time > 1:  # If no motion for 1 seconds, set state to "Vacant"
        current_state = "Vacant"

    #Display the current state on the video frame
    if current_state == "Object":
        # Use FONT_HERSHEY_COMPLEX for "Object" state
        cv.putText(frame, "My Room: Object", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
    else:
        # Use FONT_HERSHEY_SCRIPT_SIMPLEX for "Vacant" state
        cv.putText(frame, "My Room: Vacant", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

    #Write the frame to the output video file
    video_writer.write(frame)


    cv.circle(frame, (frame_width - 30, 30), 10, (0, 0, 255), -1)  # Red circle at top-right corner

   
    cv.imshow("Motion Detector", frame)

    # Exit the loop if 'q' is pressed
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break


webcam.release()
video_writer.release()
cv.destroyAllWindows()

print("Motion detection completed. Video saved as 'output.avi'.")