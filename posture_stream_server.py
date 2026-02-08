"""
Posture Stream Server: Pulls live feed from Pi, runs bbl_test_task posture
detection on each frame, and serves the processed MJPEG to the website.
"""
import os
import cv2
import math as m
import threading
from flask import Flask, Response
import mediapipe as mp

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# REPLACE WITH YOUR PI'S IP ADDRESS
PI_IP = "10.204.115.220"
STREAM_URL = f"http://{PI_IP}:5000/video_feed"

app = Flask(__name__)

# Optional: play audio on bad posture (import only if sounds exist)
try:
    from elevenlabs_tts import play_audio
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False


def find_distance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_angle(x1, y1, x2, y2):
    if y1 == 0:
        return 0
    denom = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1
    if denom == 0:
        return 0
    ratio = (y2 - y1) * (-y1) / denom
    ratio = max(-1, min(1, ratio))
    theta = m.acos(ratio)
    return int(180 / m.pi * theta)


# Run pose detection every N frames; skip frames reuse last overlay (higher = smoother video, less posture updates)
DETECT_EVERY_N = 4
# Inference resolution (smaller = faster). None = use full frame.
INFERENCE_H = 160

def generate_posture_frames():
    """Generator: read from Pi stream, run posture detection, yield JPEG frames."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    green = (127, 255, 0)
    red = (50, 50, 255)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    pth2tsk = "pose_landmarker_full.task"
    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=pth2tsk),
        running_mode=VisionRunningMode.IMAGE,
    )

    cap = cv2.VideoCapture(STREAM_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer to reduce lag
    if not cap.isOpened():
        print("Could not open Pi stream. Is live_stream.py running on the Pi?")
        return

    with PoseLandmarker.create_from_options(options) as landmarker:
        frame_index = 0
        good_frames = 0
        bad_frames = 0
        last_audio_time = 0
        cached_overlay = None  # (image_with_overlay, landmarks, good_frames, bad_frames) or None

        while True:
            success, image = cap.read()
            if not success:
                break

            h, w = image.shape[:2]
            scale = 1.0
            if INFERENCE_H and h > INFERENCE_H:
                scale = h / INFERENCE_H
                small_h = INFERENCE_H
                small_w = int(w / scale)
                rgb_small = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (small_w, small_h))
            else:
                rgb_small = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            do_detect = (frame_index % DETECT_EVERY_N) == 0

            if do_detect:
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_small)
                keypoints = landmarker.detect(mp_image)
            else:
                keypoints = cached_overlay if cached_overlay else None

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if not keypoints or not keypoints.pose_landmarks:
                ret, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 75])
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
                continue

            cached_overlay = keypoints  # reuse on skipped frames
            landmarks = keypoints.pose_landmarks[0]
            l_shldr_x = int(landmarks[11].x * w)
            l_shldr_y = int(landmarks[11].y * h)
            r_shldr_x = int(landmarks[12].x * w)
            r_shldr_y = int(landmarks[12].y * h)
            l_ear_x = int(landmarks[7].x * w)
            l_ear_y = int(landmarks[7].y * h)
            l_hip_x = int(landmarks[23].x * w)
            l_hip_y = int(landmarks[23].y * h)

            offset = find_distance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
            if offset < 100:
                cv2.putText(image, str(int(offset)) + " Aligned", (w - 150, 30), font, 0.9, green, 2)
            else:
                cv2.putText(image, str(int(offset)) + " Not Aligned", (w - 150, 30), font, 0.9, red, 2)

            neck_inclination = find_angle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = find_angle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
            cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
            cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            angle_text_string = "Neck : " + str(int(neck_inclination)) + "  Torso : " + str(int(torso_inclination))

            if neck_inclination < 30 and torso_inclination < 10:
                bad_frames = 0
                good_frames += 1
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)
            else:
                good_frames = 0
                bad_frames += 1
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

            fps = cap.get(cv2.CAP_PROP_FPS) or 20
            good_time = (1 / fps) * good_frames
            bad_time = (1 / fps) * bad_frames

            if good_time > 0:
                cv2.putText(image, f"Good Posture Time : {round(good_time, 1)}s", (10, h - 20), font, 0.9, green, 2)
            else:
                cv2.putText(image, f"Bad Posture Time : {round(bad_time, 1)}s", (10, h - 20), font, 0.9, red, 2)

            can_play = last_audio_time == 0 or (frame_index - last_audio_time) > 150
            if bad_time > 5 and HAS_AUDIO and can_play:
                last_audio_time = frame_index
                bad_frames = 0
                good_frames = 0
                cv2.putText(image, "Fix posture", (w // 2 - 100, h // 2), font, 1, red, 2)
                sound_path = os.path.join(PROJECT_ROOT, "sounds", "mickey.mp3")
                threading.Thread(target=play_audio, args=(sound_path,), daemon=True).start()

            ret, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 75])
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    cap.release()


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_posture_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/")
def index():
    return "<h1>Posture Stream (bbl_test_task processing)</h1><img src='/video_feed'>"


if __name__ == "__main__":
    print(f"Connecting to Pi stream at {STREAM_URL}...")
    print("Serving processed posture feed at http://0.0.0.0:5001/video_feed")
    app.run(host="0.0.0.0", port=5001, threaded=True)
