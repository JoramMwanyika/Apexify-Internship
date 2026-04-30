import os
# Force TensorFlow to use legacy Keras 2, which DeepFace requires in TF 2.16+
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from deepface import DeepFace

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

print("Loading DeepFace model... (This might take a moment)")
# Initialize the model to avoid slow down on the first request
try:
    DeepFace.build_model("Emotion")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
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

        # Analyze using DeepFace
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if isinstance(results, list):
            result = results[0]
        else:
            result = results

        emotion = result.get('dominant_emotion', 'unknown')
        region = result.get('region', None)

        response_data = {
            'emotion': emotion,
            'region': region
        }
        
        return jsonify(response_data)

    except Exception as e:
        # Avoid crashing the server if there's a detection error
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
