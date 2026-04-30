import os
import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
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

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

print("Loading YOLOv8 model... (this may take a moment)")
model = YOLO("yolov8n-oiv7.pt")
print("✅ Model loaded successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Extract base64 image data (format: "data:image/jpeg;base64,...")
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
            
        decoded_data = base64.b64decode(image_data)
        np_data = np.frombuffer(decoded_data, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        if frame is None:
             return jsonify({'error': 'Invalid image format'}), 400

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, tracker="botsort.yaml", verbose=False)
        
        # Get the annotated frame (draws bounding boxes, labels, and track IDs)
        annotated_frame = results[0].plot()
        
        # Count the number of objects currently detected
        num_objects = len(results[0].boxes) if results[0].boxes else 0

        # Convert the annotated frame back to base64 to send to the frontend
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        encoded_image = base64.b64encode(buffer).decode('utf-8')

        response_data = {
            'annotated_image': f"data:image/jpeg;base64,{encoded_image}",
            'num_objects': num_objects
        }
        
        return jsonify(response_data)

    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Running on port 5004 to avoid conflict with Task 3 which is on 5003
    app.run(debug=True, port=5004)
