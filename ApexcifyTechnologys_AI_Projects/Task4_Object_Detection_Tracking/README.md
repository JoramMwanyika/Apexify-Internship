# Task 4: Object Detection & Tracking

A real-time Object Detection and Tracking system utilizing your webcam. 

This project uses **YOLOv8** (via the `ultralytics` package) for state-of-the-art object detection, and employs its built-in advanced tracking algorithm (**BoT-SORT**) to assign persistent IDs to objects as they move across frames.

## Features
- **Object Detection:** Identifies multiple objects in real-time (people, chairs, cellphones, cups, etc.).
- **Object Tracking:** Assigns a unique ID to each detected object and maintains it across continuous frames.
- **Bonus Implementations:**
  - Real-time FPS (Frames Per Second) counter.
  - Active Object Count display.

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Navigate to this directory (`Task4_Object_Detection_Tracking`).
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the tracker:
   ```bash
   python object_tracker.py
   ```
   *(Note: The first time you run the script, it will automatically download the `yolov8n.pt` pre-trained model weights, which is about 6MB).*
5. A window will open showing your webcam feed with tracked objects, bounding boxes, labels, and tracking IDs!
6. Press the **'q'** key while focused on the webcam window to quit the application.
