import cv2
import csv
import os
import time
import subprocess
from detection import detect_and_track_engagement, reset_engagement_tracking

RTSP_URL = 'your live stream data from cmarea feed in rtsp_live_stream'
CSV_FILE = 'engagement_log.csv'

csv_fields = ['timestamp', 'staff_idx', 'staff_bbox', 'customer_idx', 'customer_bbox', 'distance_px', 'engagement_start', 'engagement_end', 'duration_sec']
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()

def process_rtsp_stream():
    frame_count = 0

    while True:
        print(f"Connecting to RTSP stream: {RTSP_URL}")
        cap = cv2.VideoCapture(RTSP_URL)

        if not cap.isOpened():
            print("Failed to open RTSP stream. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        print("✅ Stream opened successfully. Starting continuous detection...")
        reset_engagement_tracking()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Stream lost or error reading frame. Reconnecting...")
                cap.release()
                break

            processed_frame = detect_and_track_engagement(frame)
            cv2.imshow("Detections", processed_frame)

            frame_count += 1
            if frame_count % 30 == 0:
                print(f"📸 Frame #{frame_count} processed.")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

if __name__ == '__main__':
    # Start dashboard.py in background
    subprocess.Popen(['python', 'dashboard.py'])
    print("🚀 Dashboard started at http://localhost:5001")

    process_rtsp_stream()
