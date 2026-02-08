import cv2
import time
import pymongo
import threading
import os
from datetime import datetime
import sys

# --- CONFIGURATION ---
MONGO_URI = "mongodb+srv://123:123@cluster0.a63yfb5.mongodb.net/?appName=Cluster0"
DB_NAME = "hackathon_db"
COLLECTION_NAME = "video_stream"

# VIDEO SETTINGS
FPS = 10.0           # Lowered to 10 for better stability on Pi
SEGMENT_SEC = 15     # Target length
OVERLAP_SEC = 5      # New video every 5 seconds

# CALCULATED CONSTANTS (The Math)
FRAMES_PER_SEGMENT = int(SEGMENT_SEC * FPS) # 15 * 10 = 150 frames
FRAMES_BETWEEN_STARTS = int(OVERLAP_SEC * FPS) # 5 * 10 = 50 frames
RES = (640, 480)

# --- SETUP ---
print("Connecting to Mongo...")
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected!")
except Exception as e:
    print(f"Connection Failed: {e}")
    sys.exit(1)

# --- UPLOAD WORKER ---
def upload_worker(filename, timestamp, duration):
    try:
        print(f"   [UPLOAD] pushing {filename}...")
        with open(filename, "rb") as f:
            video_data = f.read()
        
        doc = {
            "camera_id": "pi_cam_1",
            "timestamp": timestamp,
            "video_data": video_data,
            "duration": duration,
            "processed": False,
            "filename": filename
        }
        collection.insert_one(doc)
        print(f"   [SUCCESS] {filename} in cloud!")
        os.remove(filename) # Auto-delete
        
    except Exception as e:
        print(f"   [ERROR] Upload failed: {e}")

# --- RECORDER CLASS ---
class VideoSegment:
    def __init__(self, start_id):
        self.start_ts = datetime.utcnow()
        self.filename = f"vid_{int(time.time())}.mp4"
        self.frame_count = 0
        self.is_active = True
        
        # XVID is the safest codec for AVI
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.filename, fourcc, FPS, RES, isColor=False)
        
    def add_frame(self, frame):
        if self.is_active:
            self.writer.write(frame)
            self.frame_count += 1
            
            # Check if done based on FRAME COUNT, not time
            if self.frame_count >= FRAMES_PER_SEGMENT:
                self.finish()

    def finish(self):
        self.is_active = False
        self.writer.release()
        print(f"[COMPLETED] {self.filename} ({self.frame_count} frames)")
        
        # Trigger Upload
        t = threading.Thread(target=upload_worker, args=(self.filename, self.start_ts, SEGMENT_SEC))
        t.start()

# --- MAIN LOOP ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, FPS)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, RES[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RES[1])
time.sleep(2)

active_segments = []
master_frame_count = 0 

print(f"--- ROLLING RECORDER (Frame Locked) ---")
print(f"Target: {SEGMENT_SEC}s clips ({FRAMES_PER_SEGMENT} frames)")
print(f"Overlap: New clip every {FRAMES_BETWEEN_STARTS} frames")
print("Press Ctrl+C to stop (Wait at least 20s for first file!)")

try:
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Start NEW segment? (Every 50 frames)
        if master_frame_count % FRAMES_BETWEEN_STARTS == 0:
            new_seg = VideoSegment(master_frame_count)
            active_segments.append(new_seg)
            print(f"[START] Segment {len(active_segments)} active")
            
        # 2. Write to ALL active segments
        # Iterate over a copy [:] so we can remove items safely
        for seg in active_segments[:]:
            seg.add_frame(gray)
            if not seg.is_active:
                active_segments.remove(seg)
                
        master_frame_count += 1
        
        # Small sleep if Pi is running too hot/fast (unlikely)
        # time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping...")
    cap.release()
    client.close()
