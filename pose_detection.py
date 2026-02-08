import cv2
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

model_path = "pose_landmarker.task"

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
)

cam = cv2.VideoCapture(0)
frame_rate = cam.get(cv2.CAP_PROP_FPS) or 30
frame_index = 0

with PoseLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame_timestamp_ms = int(frame_index * 1000 / frame_rate)
        frame_index += 1

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        pose_landmarker_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

        h, w = frame.shape[:2]
        if pose_landmarker_result.pose_landmarks:
            landmarks = pose_landmarker_result.pose_landmarks[0]
            # Points 11, 12, 23, 24: shoulders and hips
            idx_to_point = {}
            for idx in (11, 12, 23, 24):
                lm = landmarks[idx]
                px = int(lm.x * w)
                py = int(lm.y * h)
                idx_to_point[idx] = (px, py)
                cv2.circle(frame, (px, py), 8, (0, 255, 0), -1)

            # Draw lines: shoulder-to-shoulder, hip-to-hip, shoulder-to-hip
            if 11 in idx_to_point and 12 in idx_to_point:
                cv2.line(frame, idx_to_point[11], idx_to_point[12], (0, 255, 0), 2)
            if 23 in idx_to_point and 24 in idx_to_point:
                cv2.line(frame, idx_to_point[23], idx_to_point[24], (0, 255, 0), 2)
            if 11 in idx_to_point and 23 in idx_to_point:
                cv2.line(frame, idx_to_point[11], idx_to_point[23], (255, 0, 0), 2)
            if 12 in idx_to_point and 24 in idx_to_point:
                cv2.line(frame, idx_to_point[12], idx_to_point[24], (255, 0, 0), 2)



        cv2.imshow("Pose", frame)
        if cv2.waitKey(1) == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()
