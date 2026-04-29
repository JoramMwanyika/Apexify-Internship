# Task 3: Image Classifier (Emotion Recognition)

A real-time webcam image classifier built using Python, OpenCV, and the **DeepFace** library (which runs on TensorFlow/Keras).

This project continuously captures video from your webcam, detects faces, and classifies the dominant emotion (e.g., **Happy**, **Sad**, **Neutral**, Angry, Surprise) in real-time.

## Features
- Deep Learning powered image classification using a pre-trained Keras model.
- Real-time webcam integration.
- Bounding box and label overlay on detected faces.

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Navigate to this directory (`Task3_Image_Classifier`).
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: TensorFlow and DeepFace might take a little while to install due to their size).*
4. Run the classifier:
   ```bash
   python classifier.py
   ```
5. A window will open showing your webcam feed. 
   - **Important:** The very first time you run this, DeepFace will automatically download its pre-trained facial weights file (approx. a few hundred MBs). Please be patient.
6. Make a Happy, Sad, or Neutral face in front of the camera to see the prediction!
7. Press the **'q'** key while focused on the webcam window to quit the application.
