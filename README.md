# 🔔 AI-Powered Smart Doorbell System

> 🚀 A real-time intelligent surveillance system that detects threats using **Face Recognition + Weapon Detection + Behavioral Analysis**

---

## 🧠 Overview

The **AI Smart Doorbell** is an advanced security system that goes beyond traditional cameras.
It analyzes **who is at the door**, **how long they stay**, and **what they carry**, to determine a **real-time threat level**.

---

## ⚡ Key Features

### 👤 Face Recognition

* पहचान known vs unknown visitors
* Uses optimized face embeddings for fast recognition
* Runs asynchronously for smooth performance

### ⏱️ Dwell Time Analysis

* Tracks how long a person stays near the door
* Suspicious behavior → increases threat score

### 🔪 Weapon Detection (YOLOv8)

* Detects potential threats like weapons
* Optimized with:

  * Frame skipping
  * Image resizing
  * Temporal smoothing

### 🧠 Hybrid Threat Scoring Engine

Combines multiple signals:

* Face status (known / unknown / covered)
* Dwell time
* Weapon presence
* Environmental conditions

```text
Final Score = Face + Dwell + Audio + Camera + Weapon Bonus
```

✔ Ensures:

* Realistic behavior analysis
* Immediate risk escalation when needed

---

## 🚨 Threat Levels

| Level | Description | Action                 |
| ----- | ----------- | ---------------------- |
| 🟢 0  | Normal      | Log only               |
| 🟡 1  | Suspicious  | Record + Alert         |
| 🔴 2  | High Threat | Alarm + Telegram Alert |

---

## 📸 Real-Time Features

* 🔲 Bounding boxes for:

  * Faces
  * Detected persons
* 📊 Live threat score display
* ⚡ FPS monitoring
* 🚨 "WEAPON DETECTED" alert overlay

---

## 📲 Instant Alerts

* Sends **real-time alerts via Telegram**
* Includes:

  * Captured image
  * Threat score
  * Dwell time
  * Person identity

---

## 🏗️ System Architecture

```text
Camera Feed
    ↓
YOLO Detection (every 5 frames)
    ↓
Face Recognition (async)
    ↓
Person Tracking (dwell time)
    ↓
Threat Score Engine (Hybrid AI Logic)
    ↓
Alert System (Telegram + Logging)
    ↓
Live Display UI
```

---

## ⚙️ Optimizations

To ensure real-time performance:

* 🚀 YOLO runs every 5 frames
* 📉 Frame resizing (640x360)
* 🔄 Temporal smoothing for weapon detection
* 🧵 Async face recognition
* ⚡ Lightweight model (YOLOv8n)

---

## 🛠️ Tech Stack

* 🐍 Python
* 🎥 OpenCV
* 🤖 YOLOv8 (Ultralytics)
* 🧠 Face Recognition (Embeddings)
* 📡 Telegram Bot API

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/smart-doorbell.git
cd smart-doorbell
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add Known Faces

* Place images inside:

```
known_faces/
```

### 4️⃣ Run System

```bash
python main.py
```

---

## 📂 Project Structure

```text
core/
 ├── detector.py
 ├── face_recognizer.py
 ├── person_tracker.py
 ├── threat.py

utils/
 ├── telegram_alert.py

main.py
config.py
event_logger.py
```

---

## 🎯 Use Cases

* 🏠 Smart Home Security
* 🏢 Office Entry Monitoring
* 🏫 Campus Surveillance
* 🚪 Smart Access Control Systems

---

## 🔮 Future Improvements

* 🔫 Custom weapon detection model (guns, knives)
* 🌙 Night-time auto detection
* 🔊 Sound anomaly detection
* ☁️ Cloud deployment (AWS / Vercel / Edge AI)
* 📱 Mobile app integration

---

## 🏆 Why This Project Stands Out

✔ Combines **Computer Vision + Behavioral AI**
✔ Real-time processing with optimizations
✔ Explainable threat scoring
✔ Practical, deployable system

---

## 👨‍💻 Author

**Mohit Jariwala**
🚀 AI/ML Developer | Computer Vision Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!

---

