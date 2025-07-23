import cv2
import time

RTSP_URL = 'rtsp://admin:AiCRI2o24@192.168.6.249:554/cam/realmonitor?channel=1&subtype=00'

def test_continuous_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("❌ Failed to open RTSP stream.")
        return

    print("✅ Stream opened successfully. Starting continuous read...")
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to read frame. Attempting reconnection...")
            cap.release()
            time.sleep(5)
            cap = cv2.VideoCapture(rtsp_url)
            continue

        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            print(f"📸 Frame #{frame_count} read after {elapsed:.2f} seconds.")
            cv2.imshow('Test Frame', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_continuous_stream(RTSP_URL)
