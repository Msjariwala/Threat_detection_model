# core/camera_monitor.py

import cv2
import numpy as np


class CameraMonitor:
    def __init__(self, dark_threshold=40, variance_threshold=15):
        """
        dark_threshold: mean pixel value below which frame is considered dark
        variance_threshold: low variance means uniform frame (possibly covered)
        """
        self.dark_threshold = dark_threshold
        self.variance_threshold = variance_threshold
        self.previous_mean = None

    def check_obstruction(self, frame):
        """
        Analyzes a frame and determines if camera is obstructed.

        Returns:
            "NORMAL" or "OBSTRUCTED"
        """

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mean_intensity = np.mean(gray)
        variance = np.var(gray)

        obstructed = False

        # Condition 1: Very dark frame
        if mean_intensity < self.dark_threshold:
            obstructed = True

        # Condition 2: Very low variance (uniform image)
        if variance < self.variance_threshold:
            obstructed = True

        # Condition 3: Sudden brightness drop
        if self.previous_mean is not None:
            if abs(mean_intensity - self.previous_mean) > 80:
                obstructed = True

        self.previous_mean = mean_intensity

        return "OBSTRUCTED" if obstructed else "NORMAL"
    
