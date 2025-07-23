# Customer Engagement Dashboard

This project is a real-time customer-staff engagement tracker with a web-based dashboard built using **Flask**. It detects and logs interactions from a live RTSP video stream using **YOLO**-based object detection.

## Features

- 🧠 Customer/staff detection using YOLO
- 🔁 Continuous RTSP stream processing
- 📝 CSV logging of engagements with timestamps and durations
- 🌐 Live dashboard auto-refreshing every 2 seconds
- 📊 Frontend built with vanilla HTML/CSS + JavaScript

## Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/AyeCham/custmoer_behavior_detection.git
   cd YOUR_REPO

2. Create a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies:
    pip install -r requirements.txt

4. Run the system
    python app.py

## File structure
├── app.py               # RTSP stream + detection
├── detection.py         # YOLO detection logic
├── dashboard.py         # Flask dashboard server
├── engagement_log.csv   # Logs customer-staff interactions
└── best.pt              # custom model for staff and customer detection
├── .gitignore
└── README.md
