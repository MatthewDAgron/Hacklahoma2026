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
FPS = 10.0           
SEGMENT_SEC = 15     # Target length
OVERLAP_SEC = 5      # New video every 5 seconds

# CALCULATED CONSTANTS
FRAMES_PER_SEGMENT = int(SEGMENT_SEC * FPS) # 150 frames
FRAMES_BETWEEN_STARTS = int(OVERLAP_SEC * FPS) # 50 frames
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
        
        # --- RESTORED TO AVI ---
        self.filename = f"vid_{int(time.time())}.avi"
        
        # --- RESTORED TO XVID (Safe Codec) ---
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(self.filename, fourcc, FPS, RES, isColor=False)
        self.frame_count = 0
        self.is_active = True
        
    def add_frame(self, frame):
        if self.is_active:
            self.writer.write(frame)
            self.frame_count += 1
            
            if self.frame_count >= FRAMES_PER_SEGMENT:
                self.finish()

    def finish(self):
        self.is_active = False
        self.writer.release()
        print(f"[COMPLETED] {self.filename} ({self.frame_count} frames)")
        
        # DIRECT UPLOAD (No Conversion)
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

print(f"--- ROLLING RECORDER (AVI MODE) ---")
print(f"Target: {SEGMENT_SEC}s clips ({FRAMES_PER_SEGMENT} frames)")
print("Press Ctrl+C to stop")

try:
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Start NEW segment?
        if master_frame_count % FRAMES_BETWEEN_STARTS == 0:
            new_seg = VideoSegment(master_frame_count)
            active_segments.append(new_seg)
            print(f"[START] Segment {len(active_segments)} active")
            
        # Write to active segments
        for seg in active_segments[:]:
            seg.add_frame(gray)
            if not seg.is_active:
                active_segments.remove(seg)
                
        master_frame_count += 1

except KeyboardInterrupt:
    print("\nStopping...")
    cap.release()
    client.close()