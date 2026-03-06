# event_logger.py

import os
import cv2
import time
from datetime import datetime


class EventLogger:

    def __init__(self, save_folder="threat_events"):
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)
        self.last_saved_time = 0
        self.cooldown = 10  # seconds

    def log_event(self, frame, face_status, dwell_time, score):
        """
        Save a threat event frame to disk if not on cooldown.
        Returns the filepath if saved, or None if skipped.
        """
        current_time = time.time()

        if current_time - self.last_saved_time < self.cooldown:
            return None

        self.last_saved_time = current_time

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{face_status}_{timestamp}.jpg"
        filepath = os.path.join(self.save_folder, filename)

        cv2.imwrite(filepath, frame)
        print(f"[ALERT SAVED] {filename}")

        return filepath