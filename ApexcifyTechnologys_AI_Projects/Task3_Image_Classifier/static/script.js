const video = document.getElementById('webcam');
const canvas = document.getElementById('overlay');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const statusDot = document.querySelector('.status-indicator .dot');
const statusText = document.querySelector('.status-indicator .text');
const emotionDisplay = document.getElementById('emotion-display');

let stream = null;
let isPredicting = false;
let predictionInterval = null;

// Map emotions to icons and colors
const emotionMap = {
    'happy': { icon: 'fa-face-laugh-beam', color: '#10b981' },
    'sad': { icon: 'fa-face-sad-tear', color: '#3b82f6' },
    'angry': { icon: 'fa-face-angry', color: '#ef4444' },
    'surprise': { icon: 'fa-face-surprise', color: '#f59e0b' },
    'fear': { icon: 'fa-face-grimace', color: '#8b5cf6' },
    'neutral': { icon: 'fa-face-meh', color: '#94a3b8' },
    'disgust': { icon: 'fa-face-dizzy', color: '#84cc16' },
    'unknown': { icon: 'fa-face-meh-blank', color: '#94a3b8' }
};

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        
        // Wait for video metadata to set canvas size
        video.onloadedmetadata = () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        };

        startBtn.disabled = true;
        stopBtn.disabled = false;
        
        statusDot.className = 'dot green';
        statusText.textContent = 'Camera On';
        
        // Start prediction loop
        isPredicting = true;
        startPredicting();
        
    } catch (err) {
        console.error("Error accessing webcam:", err);
        alert("Could not access webcam. Please ensure permissions are granted.");
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    
    video.srcObject = null;
    isPredicting = false;
    
    if (predictionInterval) {
        clearTimeout(predictionInterval);
    }
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    startBtn.disabled = false;
    stopBtn.disabled = true;
    
    statusDot.className = 'dot red';
    statusText.textContent = 'Camera Off';
    
    updateEmotionDisplay('unknown');
}

function updateEmotionDisplay(emotion) {
    const config = emotionMap[emotion] || emotionMap['unknown'];
    
    emotionDisplay.className = `emotion-display ${emotion}`;
    
    if (emotion === 'unknown') {
        emotionDisplay.innerHTML = `
            <i class="fa-regular ${config.icon}"></i>
            <span>Waiting for face...</span>
        `;
    } else {
        // Capitalize first letter
        const capitalized = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        emotionDisplay.innerHTML = `
            <i class="fa-regular ${config.icon}"></i>
            <span>${capitalized}</span>
        `;
    }
}

function captureFrame() {
    // Create a temporary canvas to get the frame image data
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Draw current video frame to temp canvas
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
    
    // Convert to base64
    return tempCanvas.toDataURL('image/jpeg', 0.8);
}

async function startPredicting() {
    if (!isPredicting) return;
    
    // Check if video is playing and has dimensions
    if (video.videoWidth === 0) {
        predictionInterval = setTimeout(startPredicting, 500);
        return;
    }
    
    try {
        const frameData = captureFrame();
        
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: frameData })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Clear previous drawings
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if (data.region && data.emotion && data.emotion !== 'unknown') {
                const { x, y, w, h } = data.region;
                
                // Draw bounding box
                ctx.strokeStyle = emotionMap[data.emotion]?.color || '#00ff00';
                ctx.lineWidth = 3;
                ctx.strokeRect(x, y, w, h);
                
                // Draw emotion text on canvas
                ctx.fillStyle = emotionMap[data.emotion]?.color || '#00ff00';
                ctx.font = '24px Inter';
                ctx.fillText(data.emotion.toUpperCase(), x, y - 10);
                
                // Update UI display
                updateEmotionDisplay(data.emotion);
            } else {
                updateEmotionDisplay('unknown');
            }
        }
    } catch (error) {
        console.error("Prediction error:", error);
    }
    
    // Schedule next frame (approx 3-4 frames per second to avoid overloading backend)
    if (isPredicting) {
        predictionInterval = setTimeout(startPredicting, 250);
    }
}

// Event Listeners
startBtn.addEventListener('click', startCamera);
stopBtn.addEventListener('click', stopCamera);
