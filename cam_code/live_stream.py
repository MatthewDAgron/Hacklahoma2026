# *****************************************
# RUNS OF THE PI !!!!!!!!!!!!!!!!!!!!!!!!!
# *****************************************
from flask import Flask, Response
import cv2
import time

app = Flask(__name__)

# Camera Setup
cap = cv2.VideoCapture(0)
# Lower resolution for smoother streaming over Wi-Fi
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 20)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            # Yield the frame in MJPEG format
            # This is the standard format browsers and OpenCV understand
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Pi Camera Live</h1><img src='/video_feed'>"

if __name__ == '__main__':
    # 0.0.0.0 means "Listen on all network interfaces"
    app.run(host='0.0.0.0', port=5000, threaded=True)