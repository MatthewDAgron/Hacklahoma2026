import pymongo
import os
import sys

# --- CONFIGURATION ---
MONGO_URI = "mongodb+srv://123:123@cluster0.a63yfb5.mongodb.net/?appName=Cluster0"
DB_NAME = "hackathon_db"
COLLECTION_NAME = "video_stream"
DOWNLOAD_DIR = "downloads"

# --- SETUP ---
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

print("Connecting to MongoDB...")
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    
    # Get total count
    count = col.count_documents({})
    print(f"Found {count} videos in the cloud.")
    
except Exception as e:
    print(f"Connection Failed: {e}")
    sys.exit(1)

# --- DOWNLOAD LOOP ---
cursor = col.find({})

print(f"--- DOWNLOADING TO FOLDER: {DOWNLOAD_DIR}/ ---")

downloaded = 0
for doc in cursor:
    try:
        # Get filename (or make one up if missing)
        filename = doc.get("filename", f"unknown_{int(doc['timestamp'].timestamp())}.avi")
        
        # Ensure it saves into the folder
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        
        # Get Binary Data
        video_data = doc.get("video_data")
        
        if video_data:
            with open(filepath, "wb") as f:
                f.write(video_data)
            downloaded += 1
            print(f"[{downloaded}/{count}] Saved {filename} ({len(video_data)/1024:.1f} KB)")
        else:
            print(f"[SKIP] Document {doc['_id']} had no video data.")
            
    except Exception as e:
        print(f"[ERROR] Could not download doc: {e}")

print("--- DOWNLOAD COMPLETE ---")
