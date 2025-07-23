from ultralytics import YOLO
from datetime import datetime
import cv2
import numpy as np
import csv
import os

LOG_CSV = 'engagement_log.csv'
model = YOLO('best4.pt')
print("Loaded class names:", model.names)

engagement_tracking = {}

def calculate_center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def euclidean_distance(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def detect_and_track_engagement(cv_image, task_name='UnknownTask', conf_threshold=0.4):
    global engagement_tracking

    try:
        results = model.predict(cv_image, conf=conf_threshold, verbose=False)

        detections = []
        customers = []
        staffs = []

        for r in results:
            for box in r.boxes:
                label = model.names[int(box.cls)]
                confidence = float(box.conf)
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                detections.append({'class': label, 'confidence': confidence, 'bbox': xyxy.tolist()})

                center = calculate_center(xyxy)

                if label == 'customer':
                    customers.append({'center': center, 'bbox': xyxy.tolist()})
                    color = (0, 0, 255)  # Red for customer
                elif label == 'staff':
                    staffs.append({'center': center, 'bbox': xyxy.tolist()})
                    color = (0, 255, 0)  # Green for staff
                else:
                    color = (255, 255, 255)

                cv2.rectangle(cv_image, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
                cv2.putText(cv_image, f"{label} {confidence:.2f}", (xyxy[0], xyxy[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for staff_idx, staff in enumerate(staffs):
            for customer_idx, customer in enumerate(customers):
                distance = euclidean_distance(customer['center'], staff['center'])
                print(f"Distance between customer-{customer_idx} and staff-{staff_idx}: {distance:.2f} pixels")

                pair_key = (customer_idx, staff_idx)
                if distance < 500:
                    if pair_key not in engagement_tracking:
                        engagement_tracking[pair_key] = {'start_time': datetime.now(), 'start_distance': distance,
                                                         'customer_bbox': customer['bbox'], 'staff_bbox': staff['bbox']}
                else:
                    if pair_key in engagement_tracking:
                        start_time = engagement_tracking[pair_key]['start_time']
                        duration = (datetime.now() - start_time).total_seconds()
                        end_time = datetime.now()

                        with open(LOG_CSV, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([timestamp, customer_idx, staff_idx, start_time, end_time, duration,
                                             engagement_tracking[pair_key]['start_distance'],
                                             engagement_tracking[pair_key]['customer_bbox'],
                                             engagement_tracking[pair_key]['staff_bbox']])

                        print(f"Engagement logged: Customer-{customer_idx}, Staff-{staff_idx}, Duration: {duration:.2f}s")
                        del engagement_tracking[pair_key]

        print(f"Detections in this frame: {len(detections)}")

        return cv_image

    except Exception as e:
        print(f"Detection failed: {e}")
        return cv_image

def reset_engagement_tracking():
    global engagement_tracking
    engagement_tracking = {}
    print("Engagement tracking has been reset.")
