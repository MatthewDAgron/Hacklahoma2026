import cv2

# REPLACE WITH YOUR PI'S IP ADDRESS
PI_IP = "10.204.115.220" 
STREAM_URL = f"http://{PI_IP}:5000/video_feed"

print(f"Connecting to live stream at {STREAM_URL}...")

# OpenCV can open URLs just like local webcams!
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Error: Could not open stream. Is the Pi script running?")
    exit()

while True:
    ret, frame = cap.read()
    
    if ret:
        # --- DO YOUR CODE PROCESSING HERE ---
        # Example: Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Show it on screen (for debugging)
        cv2.imshow('Live Processing from Pi', gray)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Frame lost...")
        break

cap.release()
cv2.destroyAllWindows()