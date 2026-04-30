# Task 3: Image Classifier (Emotion Recognition)

A real-time webcam image classifier built using Python, Flask, OpenCV, and the **DeepFace** library (running on TensorFlow/Keras).

This project has been upgraded from a simple local window application to a **Modern Web Application**. It continuously captures video from your webcam via your browser, sends it to the Flask backend, detects faces, and classifies the dominant emotion (e.g., **Happy**, **Sad**, **Neutral**, Angry, Surprise) in real-time, displaying the results in a beautiful interface.

## Features
- **Deep Learning Image Classification**: Powered by a pre-trained Keras model.
- **Modern Web Interface**: Dark mode, glassmorphism UI, real-time overlays.
- **REST API Backend**: Flask handles image processing and connects securely to the frontend.
- **Real-time Overlays**: Bounding boxes and color-coded emotion labels drawn on the HTML5 canvas dynamically.

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Navigate to this directory (`Task3_Image_Classifier`).
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: TensorFlow and DeepFace might take a little while to install due to their size).*
4. Run the web server:
   ```bash
   python app.py
   ```
5. Open your web browser and navigate to: **http://127.0.0.1:5003**
6. **Important:** The very first time you run the backend, DeepFace will automatically download its pre-trained facial weights file and TensorFlow will initialize. Please be patient.
7. Click **Start Camera**, allow webcam access, and make a Happy, Sad, or Neutral face in front of the camera to see the prediction!
