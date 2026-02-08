import cv2
import time
import math as m
import mediapipe as mp
from elevenlabs_tts import play_audio

def badPosture(filename = 0):


    returning_list = list()
    angle_tracking_neck = list()
    angle_tracking_back = list()
    offset_tracking_shoulders = list()

    def findDistance(x1, y1, x2, y2):
        dist = m.sqrt((x2-x1)**2+(y2-y1)**2)
        return dist
    # Calculate angle.
    def findAngle(x1, y1, x2, y2):
        theta = m.acos( (y2 -y1)*(-y1) / (m.sqrt(
            (x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
        degree = int(180/m.pi)*theta
        return degree
    def sendWarning(image, font, red, w, h):
        cv2.putText(image, 'Fix posture', (w // 2 - 100, h // 2), font, 1, red, 2)
    # Initialize frame counters.
    good_frames = 0
    bad_frames  = 0
    # Font type.
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Colors.
    blue = (255, 127, 0)
    red = (50, 50, 255)
    green = (127, 255, 0)
    dark_blue = (127, 20, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)
    
    # Initialize mediapipe pose class.
    # start with building BaseOptions

    pth2tsk = 'pose_landmarker_full.task'

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=pth2tsk),
        running_mode=VisionRunningMode.VIDEO
    )

    with PoseLandmarker.create_from_options(options) as landmarker:
        # For webcam input use 0 (integer). For video file use a path string.
        cap = cv2.VideoCapture(filename)
        if not cap.isOpened():
            print("Could not open camera or video. In WSL/Linux, use a video file path or run this script on Windows for webcam.")
            print("Example: badPosture('path/to/video.mp4')")
            return

        # Meta.
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)
        #fourcc = cv2.VideoWriter_fourcc(*'mp4v')


        # Capture frames.
        frame_rate = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_index = 0
        while True:
            success, image = cap.read()
            if not success:
                print("Null.Frames")
                break
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            # Get height and width of the frame.
            h, w = image.shape[:2]

            # Convert the BGR image to RGB.
            rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image - Tasks API requires mp.Image, not numpy array.
            frame_timestamp_ms = int(frame_index * 1000 / frame_rate)
            frame_index += 1
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            keypoints = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

            # Use image in BGR for OpenCV drawing.
            image = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

            # Tasks API: pose_landmarks[0] = first person, access by index (11=left shoulder, etc.)
            if not keypoints.pose_landmarks:
                cv2.imshow('Posture', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue
            landmarks = keypoints.pose_landmarks[0]
            # Indices: 7=left ear, 8=right ear, 11=left shoulder, 12=right shoulder, 23=left hip, 24=right hip
            l_shldr_x = int(landmarks[11].x * w)
            l_shldr_y = int(landmarks[11].y * h)
            r_shldr_x = int(landmarks[12].x * w)
            r_shldr_y = int(landmarks[12].y * h)
            l_ear_x = int(landmarks[7].x * w)
            l_ear_y = int(landmarks[7].y * h)
            l_hip_x = int(landmarks[23].x * w)
            l_hip_y = int(landmarks[23].y * h)

            # Calculate distance between left shoulder and right shoulder points.
            offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

            # Assist to align the camera to point at the side view of the person.
            # Offset threshold 30 is based on results obtained from analysis over 100 samples.
            if offset < 100:
                cv2.putText(image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
            else:
                cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)
            # Calculate angles.
            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            # Draw landmarks.
            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

            # Let's take y - coordinate of P3 100px above x1,  for display elegance.
            # Although we are taking y = 0 while calculating angle between P1,P2,P3.
            cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

            # Similarly, here we are taking y - coordinate 100px above x1. Note that
            # you can take any value for y, not necessarily 100 or 200 pixels.
            cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            # Put text, Posture and angle inclination.
            # Text string for display.
            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

            # Determine whether good posture or bad posture.
            # The threshold angles have been set based on intuition.
            if neck_inclination < 30 and torso_inclination < 10:
                bad_frames = 0
                good_frames += 1

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

                # Join landmarks.
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

                angle_tracking_back = list()
                angle_tracking_neck = list()
                offset_tracking_shoulders = list()

            else:
                good_frames = 0
                bad_frames += 1

                angle_tracking_neck.append(neck_inclination)
                angle_tracking_back.append(torso_inclination)
                # get offset between shoulder points - just x should be fine
                offset_tracking_shoulders.append(findDistance(l_shldr_x, 0, r_shldr_x, 0))

                


                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

                # Join landmarks.
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

            # Calculate the time of remaining in a particular posture.
            good_time = (1 / fps) * good_frames
            bad_time = (1 / fps) * bad_frames

            # Pose time.
            if good_time > 0:
                time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
                cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
            else:
                time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
                cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

            # If you stay in bad posture for more than 5 seconds, show alert.
            if bad_time > 5:


                def getAvg(items: list):
                    sum = 0
                    for item in items:
                        sum += item
                    return sum/len(items)
                returning_list.append(getAvg(angle_tracking_neck), getAvg(angle_tracking_back), getAvg(offset_tracking_shoulders))

                sendWarning(image, font, red, w, h)
                play_audio('sounds/ElevenLabs_2026-02-08T03_10_28_Northern Terry_pvc_sp87_s30_sb90_se38_b_m2.mp3')
            cv2.imshow('Posture', image)
            # Wait so video plays at real speed (~1/fps seconds per frame). For webcam, fps is used too.
            delay_ms = max(1, int(1000 / (fps or 30)))
            if cv2.waitKey(delay_ms) & 0xFF == ord('q'):
                break

        cap.release()
        #video_output.release()
        cv2.destroyAllWindows()

# Use a video file path, or 0 for webcam (when run on Windows).
badPosture(0)