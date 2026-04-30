# Task 4: Object Detection & Tracking (Web UI)

A real-time Object Detection and Tracking system utilizing your webcam. 

This project uses **YOLOv8** (via the `ultralytics` package) for state-of-the-art object detection, and employs its built-in advanced tracking algorithm (**BoT-SORT**) to assign persistent IDs to objects as they move across frames. It has been upgraded with the **Open Images V7** model (`yolov8n-oiv7.pt`), expanding its detection vocabulary to **600 distinct object classes**.

## Features
- **Object Detection:** Identifies 600 multiple objects in real-time (people, specific sports balls, toys, tools, etc.).
- **Object Tracking:** Assigns a unique ID to each detected object and maintains it across continuous frames.
- **Cyberpunk Web Interface:** A highly styled web UI featuring a scanning laser animation and a dedicated heads-up display.
- **Real-time Stats:** Live FPS (Frames Per Second) counter and Active Object Count display dynamically.
- **REST API Backend**: Flask serves the frontend and handles the YOLOv8 frame processing over base64.

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Navigate to this directory (`Task4_Object_Detection_Tracking`).
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the tracker web server:
   ```bash
   python app.py
   ```
5. Open your web browser and go to: **http://127.0.0.1:5004**
6. Click **Initialize Feed**, grant webcam permissions, and point your camera at different objects!
