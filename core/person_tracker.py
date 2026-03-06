# core/person_tracker.py

import time
import uuid


class PersonTracker:
    def __init__(self):
        self.active_persons = {}

    def update_person(self, name):
        """
        Track a single person by name.
        Returns (person_id, person_data dict).
        """
        current_time = time.time()

        # If this person is already being tracked, update them
        for pid, data in self.active_persons.items():
            if data["name"] == name:
                data["last_seen"] = current_time
                data["dwell"] = current_time - data["first_seen"]
                return pid, data

        # New person detected
        person_id = str(uuid.uuid4())
        self.active_persons[person_id] = {
            "name": name,
            "first_seen": current_time,
            "last_seen": current_time,
            "dwell": 0
        }
        return person_id, self.active_persons[person_id]

    def update_persons(self, names):
        """
        Track multiple persons at once.

        Args:
            names: list of person name strings (e.g. ["Dad", "UNKNOWN", "Mom"])

        Returns:
            list of (person_id, person_data) tuples
        """
        results = []
        for name in names:
            pid, data = self.update_person(name)
            results.append((pid, data))
        return results

    def cleanup(self, timeout=5):
        """Remove persons not seen for `timeout` seconds."""
        current_time = time.time()

        remove_ids = [
            pid for pid, data in self.active_persons.items()
            if current_time - data["last_seen"] > timeout
        ]

        for pid in remove_ids:
            del self.active_persons[pid]