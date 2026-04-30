import os
# Force TensorFlow to use legacy Keras 2, which DeepFace requires in TF 2.16+
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import cv2
from deepface import DeepFace
import sys

def run_classifier():
    print("🤖 Initializing Emotion Classifier (Happy/Sad/Neutral)...")
    print("Please wait while the model loads. This might take a moment on the first run as weights are downloaded.")
    
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit(1)
        
    print("✅ Webcam opened successfully. Press 'q' to quit.")
    
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame from webcam.")
            break
            
        try:
            # DeepFace.analyze detects the face and classifies emotions.
            # We set enforce_detection to False so it doesn't crash if no face is visible.
            results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            
            # DeepFace can return a list of results if multiple faces are found
            if isinstance(results, list):
                result = results[0]
            else:
                result = results
                
            # Extract dominant emotion
            emotion = result['dominant_emotion']
            
            # Map emotions to Happy/Sad/Neutral if possible
            if emotion in ['happy', 'sad', 'neutral']:
                display_text = f"Emotion: {emotion.capitalize()}"
            else:
                # E.g., angry, surprise, fear, disgust -> show as well or group them
                display_text = f"Emotion: {emotion.capitalize()}"
                
            # If a face bounding box is provided
            if 'region' in result:
                x = result['region']['x']
                y = result['region']['y']
                w = result['region']['w']
                h = result['region']['h']
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Display emotion text above the rectangle
                cv2.putText(frame, display_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # fallback text if no region
                cv2.putText(frame, display_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        except Exception as e:
            # If no face is detected or an error occurs, just show "No Face Detected"
            cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
        # Display the resulting frame
        cv2.imshow('Emotion Classifier', frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_classifier()
