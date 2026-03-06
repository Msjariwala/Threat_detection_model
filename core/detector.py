# core/detector.py

from ultralytics import YOLO
from config import COCO_KNIFE_ID, COCO_SCISSORS_ID


class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        """
        Initializes YOLO model.
        Use yolov8n.pt for lightweight real-time performance.
        """
        self.model = YOLO(model_path)

    def detect(self, frame):
        """
        Detect persons and weapons in frame.

        Returns:
            {
                "persons": [ { "bbox": (x1,y1,x2,y2), "confidence": float } ],
                "weapon_detected": bool
            }
        """

        results = self.model(frame, verbose=False)

        persons = []
        weapon_detected = False

        for r in results:
            boxes = r.boxes

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Person detection (COCO id = 0)
                if cls_id == 0:
                    persons.append({
                        "bbox": (x1, y1, x2, y2),
                        "confidence": conf
                    })

                # Weapon detection
                if cls_id in [COCO_KNIFE_ID, COCO_SCISSORS_ID]:
                    weapon_detected = True

        return {
            "persons": persons,
            "weapon_detected": weapon_detected
        }