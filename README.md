# Chiroprac-Tech

Real-time posture monitoring for desk workers. A Raspberry Pi streams live camera feed to a processing server that runs pose estimation and posture analysis, then displays the annotated video on a web dashboard.

---

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Quick Start (Live Stream)](#quick-start-live-stream)
- [Detailed Setup](#detailed-setup)
- [Alternative Workflows](#alternative-workflows)
- [Troubleshooting](#troubleshooting)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CHIROPRAC-TECH PIPELINE                              │
└─────────────────────────────────────────────────────────────────────────────────┘

  Raspberry Pi 4B                    Your Machine (Windows/Mac/Linux)
  ┌──────────────────┐              ┌──────────────────────────────────────────┐
  │  Logitech USB    │              │                                          │
  │  Camera          │              │  1. posture_stream_server.py (port 5001)  │
  │       │          │   MJPEG      │     - Pulls Pi stream                     │
  │       ▼          │   over LAN   │     - MediaPipe pose detection            │
  │  live_stream.py  │ ────────────▶│     - Posture heuristics (neck/torso)     │
  │  (port 5000)     │              │     - Serves processed MJPEG              │
  │                  │              │                    │                      │
  └──────────────────┘              │                    │                      │
                                    │                    ▼                      │
                                    │  2. Next.js frontend (port 3000)          │
                                    │     - /live-metrics displays stream       │
                                    └──────────────────────────────────────────┘
```

**Flow:** Pi camera → `live_stream.py` (raw MJPEG) → `posture_stream_server.py` (pose + posture overlay) → Next.js `/live-metrics` page.

---

## Prerequisites

### Hardware

- **Raspberry Pi 4B** (or 3B+)
- **Logitech USB camera** (or compatible webcam)
- **Your dev machine** (Windows, Mac, or Linux) — for running the posture server and frontend
- **Same local network** — Pi and dev machine must be reachable

### Software

| Component | Requirement |
|-----------|-------------|
| Pi | Python 3.8+, OpenCV, Flask |
| Dev machine | Python 3.10+, Node.js 18+, npm or pnpm |
| Pi OS | Raspberry Pi OS (32-bit legacy recommended if boot/display issues) |

---

## Project Structure

```
Hacklahoma2026/
├── cam_code/                    # Scripts that run on the Pi
│   ├── live_stream.py           # ★ Primary: MJPEG stream from camera (port 5000)
│   ├── rolling_video.py         # Legacy: Record segments, upload to MongoDB
│   ├── processor.py             # Test: Pull Pi stream, grayscale processing
│   └── pull_all.py              # Legacy: Download videos from MongoDB
│
├── posture_stream_server.py     # ★ Primary: Pose + posture processing (port 5001)
├── pose_landmarker_full.task    # MediaPipe model (required)
├── bbl_test_task.py             # Standalone posture script (webcam/video file)
│
├── frontend/
│   └── ui/                      # Next.js dashboard
│       ├── app/live-metrics/    # ★ Live posture feed page
│       └── ...
│
├── sounds/                      # Audio alert for bad posture
├── requirements.txt
└── README.md
```

---

## Configuration

### Pi IP Address

The posture server pulls the stream from the Pi. Set the Pi's IP in:

**`posture_stream_server.py`** (line ~13):

```python
PI_IP = "10.204.115.220"  # Replace with your Pi's IP
```

**`processor.py`** and **`cam_code/processor.py`** (if used):

```python
PI_IP = "10.204.115.220"
```

Find the Pi's IP:

```bash
# On the Pi
hostname -I
# or
ip addr show
```

### MongoDB (Legacy Rolling Video)

If using `rolling_video.py` or `pull_all.py`, set:

- `rolling_video.py`: `MONGO_URI`, `DB_NAME`, `COLLECTION_NAME`
- `pull_all.py`: same variables
- `backend_infograb.py`: `.env` with `MONGO_STR`

---

## Quick Start (Live Stream)

### 1. On the Raspberry Pi

```bash
# SSH or plug in monitor + keyboard
cd /path/to/Hacklahoma2026

# Install dependencies (one-time)
pip install flask opencv-python

# Run the camera stream
python cam_code/live_stream.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

Test: open `http://<PI_IP>:5000` in a browser — you should see the live feed.

### 2. On Your Dev Machine

```bash
cd Hacklahoma2026

# Python deps (one-time)
pip install -r requirements.txt

# Start posture processing server
python posture_stream_server.py
```

You should see:
```
Connecting to Pi stream at http://10.204.115.220:5000/video_feed...
Serving processed posture feed at http://0.0.0.0:5001/video_feed
 * Running on http://127.0.0.1:5001
```

### 3. Start the Frontend

```bash
cd frontend/ui

# Install deps (one-time)
npm install

# Run dev server
npm run dev
```

You should see:
```
  ▲ Next.js 16.x.x
  - Local:   http://localhost:3000
```

### 4. Open the Dashboard

Go to **http://localhost:3000/live-metrics**

The stream uses `window.location.hostname:5001`, so it works with:
- `localhost:3000` → stream from `localhost:5001`
- `172.29.80.1:3000` → stream from `172.29.80.1:5001`

---

## Detailed Setup

### Pi Setup

1. **Flash Raspberry Pi OS** (32-bit legacy if you had boot/display issues).
2. **Enable camera:** `sudo raspi-config` → Interface Options → Camera → Enable.
3. **Install Python packages:**

   ```bash
   pip install flask opencv-python
   ```

4. **Copy the repo** to the Pi (USB, SCP, or Git):

   ```bash
   scp -r Hacklahoma2026 pi@<PI_IP>:~/
   ```

5. **Run the stream:**

   ```bash
   cd ~/Hacklahoma2026
   python cam_code/live_stream.py
   ```

### Dev Machine Setup

1. **Clone the repo** (or copy it locally).

2. **Create virtual environment (recommended):**

   ```bash
   cd Hacklahoma2026
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Pi IP** in `posture_stream_server.py` (see [Configuration](#configuration)).

5. **Ensure `pose_landmarker_full.task`** is in the project root (it should be).

6. **Install Node dependencies for frontend:**

   ```bash
   cd frontend/ui
   npm install
   ```

### Run Order

1. Pi: `python cam_code/live_stream.py`
2. Dev: `python posture_stream_server.py`
3. Dev: `cd frontend/ui && npm run dev`
4. Browser: `http://localhost:3000/live-metrics`

---

## Alternative Workflows

### Rolling Video → MongoDB (Legacy)

Records overlapping 15s segments, uploads to MongoDB. No real-time posture processing.

**On Pi:**

```bash
pip install pymongo opencv-python
# Edit rolling_video.py: MONGO_URI, DB_NAME, COLLECTION_NAME
python cam_code/rolling_video.py
```

**Download videos:**

```bash
# On dev machine
python cam_code/pull_all.py
# Saves to downloads/
```

### Standalone Posture Test (No Pi)

Run posture detection on webcam or video file:

```bash
python bbl_test_task.py
# Uses webcam (0) by default. Edit last line: badPosture('videos/input.avi')
# Press 'q' to quit
```

### Raw Pi Stream Test

Pull and display the Pi stream without posture processing:

```bash
# Edit processor.py with Pi IP
python cam_code/processor.py
# Press 'q' to quit
```

---

## Troubleshooting

### "Could not open Pi stream"

- Pi is running `live_stream.py`.
- Pi and dev machine are on the same network.
- Firewall allows port 5000 on the Pi.
- `PI_IP` in `posture_stream_server.py` is correct.
- Test: `curl -I http://<PI_IP>:5000/video_feed`

### "Could not open camera" on Pi

- Camera is connected.
- Camera enabled in `raspi-config`.
- Try `ls /dev/video*` — you should see `/dev/video0`.

### Stream is slow or choppy

- Lower `INFERENCE_H` in `posture_stream_server.py` (e.g., 192).
- Increase `DETECT_EVERY_N` (e.g., 3) to run pose less often.
- Use wired Ethernet for the Pi.
- Reduce resolution in `live_stream.py` (e.g., 320x240).

### Pi crashes or freezes

- Use 32-bit OS and reduce resolution/FPS.
- Avoid heavy processing on the Pi; keep it to streaming only.

### Live-metrics shows "Loading stream..." or blank

- Posture server is running on port 5001.
- Browser can reach the dev machine on that port.
- If using a different host (e.g., WSL IP), ensure the frontend and posture server use the same host.

### "pose_landmarker_full.task not found"

- File must be in the directory you run `posture_stream_server.py` from (project root).

---

## Commands Reference

| Command | Where | Purpose |
|---------|-------|---------|
| `python cam_code/live_stream.py` | Pi | Start camera MJPEG stream (port 5000) |
| `python posture_stream_server.py` | Dev | Start posture processing (port 5001) |
| `cd frontend/ui && npm run dev` | Dev | Start Next.js (port 3000) |
| `python bbl_test_task.py` | Dev | Standalone posture on webcam |
| `python cam_code/processor.py` | Dev | Raw Pi stream viewer |
| `python cam_code/rolling_video.py` | Pi | Legacy: record + upload to MongoDB |
| `python cam_code/pull_all.py` | Dev | Legacy: download videos from MongoDB |

---

## License

See [LICENSE](LICENSE).
