# main.py — Smart Doorbell (Optimized)

import cv2
import time
from core.face_recognizer import FaceRecognizer
from core.threat import ThreatScoreEngine
from core.person_tracker import PersonTracker
from event_logger import EventLogger
from utils.telegram_alert import TelegramAlert


# =============================================
# Initialize components
# =============================================

print("[INIT] Loading known faces...")
recognizer = FaceRecognizer(distance_threshold=0.5)
recognizer.load_known_faces_from_folder("known_faces")
recognizer.start()  # Start background recognition thread

logger = EventLogger()

telegram = TelegramAlert(
    bot_token="8689810105:AAHADQJlVImC6sUwOQqwNvuWUwo-H28vCwU",
    chat_id="6546395188",
    cooldown=30
)

tracker = PersonTracker()
threat_engine = ThreatScoreEngine()

cap = cv2.VideoCapture(0)

# FPS tracking
fps_counter = 0
fps_value = 0
fps_timer = time.time()

print("[INIT] Smart Doorbell running. Press 'q' to quit.")

# =============================================
# Main loop
# =============================================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- Submit frame for background recognition ---
    recognizer.submit_frame(frame)

    # --- Read latest recognition results (non-blocking) ---
    face_results = recognizer.get_results()

    # --- Track all detected faces ---
    face_names = [r["name"] for r in face_results] if face_results else ["UNKNOWN"]
    tracked = tracker.update_persons(face_names)

    # --- Find the highest-threat face for scoring ---
    worst_face_status = "UNKNOWN"
    worst_dwell = 0
    for pid, pdata in tracked:
        if pdata["name"] == "UNKNOWN" and pdata["dwell"] >= worst_dwell:
            worst_face_status = "UNKNOWN"
            worst_dwell = pdata["dwell"]
        elif pdata["name"] != "UNKNOWN":
            # Known faces are not threats, but track dwell anyway
            if worst_face_status != "UNKNOWN":
                worst_dwell = max(worst_dwell, pdata["dwell"])

    # If all faces are known, use the first one
    if all(r["name"] != "UNKNOWN" for r in face_results) and face_results:
        worst_face_status = face_results[0]["name"]
        worst_dwell = tracked[0][1]["dwell"] if tracked else 0

    # --- Evaluate threat ---
    result = threat_engine.calculate(
        face_status=worst_face_status,
        dwell_time=worst_dwell,
        is_nighttime=False,
        audio_status="NORMAL",
        camera_status="NORMAL",
        weapon_detected=False
    )

    # --- Draw bounding boxes for ALL detected faces ---
    for face in face_results:
        box = face["box"]
        name = face["name"]

        x = box["x"]
        y = box["y"]
        w = box["w"]
        h = box["h"]

        if name == "UNKNOWN":
            color = (0, 0, 255)   # Red
        else:
            color = (0, 255, 0)   # Green

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Find dwell time for this person
        person_dwell = 0
        for pid, pdata in tracked:
            if pdata["name"] == name:
                person_dwell = pdata["dwell"]
                break

        label = f"{name} | Dwell: {int(person_dwell)}s"
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # --- Handle HIGH THREAT alerts ---
    if result.level == 2:
        filepath = logger.log_event(frame, worst_face_status, worst_dwell, result.score)
        if filepath:
            caption = (
                f"\U0001F6A8 HIGH THREAT DETECTED\n"
                f"Person: {worst_face_status}\n"
                f"Dwell: {int(worst_dwell)} sec\n"
                f"Score: {result.score}"
            )
            telegram.send_alert(filepath, caption)

    # --- HUD: Threat level + FPS ---
    cv2.putText(frame,
                f"Threat: {result.level}  Score: {result.score}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # FPS counter
    fps_counter += 1
    elapsed = time.time() - fps_timer
    if elapsed >= 1.0:
        fps_value = fps_counter / elapsed
        fps_counter = 0
        fps_timer = time.time()

    cv2.putText(frame,
                f"FPS: {fps_value:.1f}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)

    cv2.imshow("Smart Doorbell", frame)

    tracker.cleanup()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =============================================
# Cleanup
# =============================================

recognizer.stop()
cap.release()
cv2.destroyAllWindows()
print("[EXIT] Smart Doorbell stopped.")