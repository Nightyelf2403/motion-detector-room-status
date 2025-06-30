
# Motion Detector using OpenCV

## Overview

This project implements a real-time motion detection system using OpenCV in Python. It captures video from a webcam, detects movement using background subtraction (MOG2), highlights the largest moving object, displays the system state on screen, and records annotated video. States include "My Room: Object" when motion is detected and "My Room: Vacant" otherwise.

---

## Features

- ✅ Real-time motion detection from webcam  
- ✅ Background subtraction using MOG2 (Gaussian Mixture-based)  
- ✅ Automatic state management with timers ("Object" / "Vacant")  
- ✅ Bounding box over detected motion  
- ✅ Recording indicator (red circle)  
- ✅ Saves video with overlays as `output.avi`

---

## Setup Instructions

1. **Install required packages**:
   ```bash
   pip install opencv-python
````

2. **Run the program**:

   ```bash
   python motion_detector.py
   ```

3. **Quit with** `q` to stop the detection and save the video.

---

## How It Works

The motion detection system works in the following stages:

### 1. Preprocessing

* Converts each frame to grayscale
* Applies Gaussian blur to reduce noise

### 2. Background Subtraction

* Uses `cv.createBackgroundSubtractorMOG2()`
* Detects dynamic regions (i.e., moving objects)

### 3. Foreground Masking and Contours

* Generates a binary mask of moving regions
* Detects contours
* Draws a bounding rectangle over the largest contour if it exceeds the noise threshold

### 4. State Tracking

* If motion is detected, sets state to "Object"
* If no motion is detected for 1 second, state becomes "Vacant"

### 5. Annotation

* Displays current state ("My Room: Object"/"Vacant") on frame
* Adds a red circle in the corner as a recording indicator

---


📹 **Output Video**: `output.avi`

---

## Block Diagram

Below is a block diagram that outlines the logic and data flow of the motion detector:

![Block Diagram](./block_diagram.png)

---

## Assumptions & Constraints

* **Static Camera**: Assumes camera is fixed in place
* **Indoor Use**: Lighting is stable and consistent
* **Low Noise**: Input feed is assumed to be relatively clean
* **Single Object Focus**: Tracks the largest moving object only
* **Empirical Thresholds**: Tuning required for different environments

---

## Source Code (Excerpt)

```python
if current_state == "Object":
    cv.putText(frame, "My Room: Object", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
else:
    cv.putText(frame, "My Room: Vacant", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

cv.circle(frame, (frame_width - 30, 30), 10, (0, 0, 255), -1)
```

---

## References

* [PyImageSearch: Motion Detection Tutorial](https://pyimagesearch.com/)
* [OpenCV-Python Docs](https://docs.opencv.org/)
* **DeepSeek AI**: Assisted with UI annotation logic (putText, circle overlays)

---

## Author

**Lalith Aditya Chunduri**


```


```
