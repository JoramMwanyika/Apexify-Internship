import cv2
import time
import torch
# PyTorch 2.6+ changed default weights_only=True, which breaks ultralytics 8.2.2.
# We monkeypatch torch.load to default to False before importing ultralytics.
original_load = torch.load
def patched_load(*args, **kwargs):
    kwargs.setdefault('weights_only', False)
    return original_load(*args, **kwargs)
torch.load = patched_load

import ultralytics
from ultralytics import YOLO

def run_tracker():
    print("🤖 Initializing Object Detection & Tracking...")
    print("Loading YOLOv8 model (this may take a moment to download the nano model on first run)...")
    
    # Load the YOLOv8 nano model (fastest, great for real-time webcam)
    model = YOLO("yolov8n-oiv7.pt") 
    
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
        
    print("✅ Webcam opened successfully. Press 'q' to quit.")
    
    # Variables for FPS calculation
    prev_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
            
        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        # tracker="botsort.yaml" is ultralytics' built-in advanced tracker
        # persist=True keeps object IDs across frames
        results = model.track(frame, persist=True, tracker="botsort.yaml", verbose=False)
        
        # Get the annotated frame (draws bounding boxes, labels, and track IDs)
        annotated_frame = results[0].plot()
        
        # Count the number of objects currently detected in this frame
        # (results[0].boxes contains all the detections)
        num_objects = len(results[0].boxes) if results[0].boxes else 0
        
        # Overlay FPS and Object Count on the top-left
        fps_text = f"FPS: {int(fps)}"
        count_text = f"Objects detected: {num_objects}"
        
        # Draw a semi-transparent black background rectangle for text readability
        cv2.rectangle(annotated_frame, (10, 10), (350, 80), (0, 0, 0), -1)
        
        cv2.putText(annotated_frame, fps_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(annotated_frame, count_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Display the frame
        cv2.imshow("YOLOv8 Object Tracking", annotated_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
            
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_tracker()
