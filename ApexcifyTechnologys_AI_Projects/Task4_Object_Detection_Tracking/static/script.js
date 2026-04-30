const video = document.getElementById('webcam');
const annotatedImage = document.getElementById('annotated-image');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const objectCount = document.getElementById('object-count');
const fpsDisplay = document.getElementById('fps-display');
const statusOverlay = document.getElementById('status-overlay');

let stream = null;
let isPredicting = false;
let predictionTimeout = null;
let lastFrameTime = 0;
let framesProcessed = 0;
let fpsInterval = null;

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusOverlay.classList.add('hidden');
        
        // Wait for video metadata
        video.onloadedmetadata = () => {
            isPredicting = true;
            lastFrameTime = performance.now();
            framesProcessed = 0;
            
            // Start FPS counter
            fpsInterval = setInterval(() => {
                const now = performance.now();
                const elapsed = (now - lastFrameTime) / 1000;
                if (elapsed > 0) {
                    const fps = framesProcessed / elapsed;
                    fpsDisplay.textContent = fps.toFixed(1);
                }
                lastFrameTime = now;
                framesProcessed = 0;
            }, 1000);

            startPredicting();
        };
        
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
    
    if (predictionTimeout) {
        clearTimeout(predictionTimeout);
    }
    if (fpsInterval) {
        clearInterval(fpsInterval);
    }
    
    startBtn.disabled = false;
    stopBtn.disabled = true;
    statusOverlay.classList.remove('hidden');
    
    // Reset image and stats
    annotatedImage.src = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";
    objectCount.textContent = '0';
    fpsDisplay.textContent = '0.0';
}

function captureFrame() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Draw current video frame to temp canvas
    // Flip horizontally so the movement feels natural like a mirror
    tempCtx.translate(tempCanvas.width, 0);
    tempCtx.scale(-1, 1);
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
    
    // Convert to base64
    return tempCanvas.toDataURL('image/jpeg', 0.8);
}

async function startPredicting() {
    if (!isPredicting) return;
    
    if (video.videoWidth === 0) {
        predictionTimeout = setTimeout(startPredicting, 500);
        return;
    }
    
    try {
        const frameData = captureFrame();
        
        const response = await fetch('/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: frameData })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.annotated_image) {
                annotatedImage.src = data.annotated_image;
            }
            
            if (data.num_objects !== undefined) {
                objectCount.textContent = data.num_objects;
            }
            
            framesProcessed++;
        }
    } catch (error) {
        console.error("Prediction error:", error);
    }
    
    // Schedule next frame. YOLOv8n is fast, so we can try ~10-15 FPS.
    // Delay of 80ms gives roughly ~12 FPS which looks decent and doesn't melt the server.
    if (isPredicting) {
        predictionTimeout = setTimeout(startPredicting, 80);
    }
}

// Event Listeners
startBtn.addEventListener('click', startCamera);
stopBtn.addEventListener('click', stopCamera);
