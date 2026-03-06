# core/face_recognizer.py

import os
import numpy as np
import cv2
import threading
import time
from deepface import DeepFace
from scipy.spatial.distance import cosine


class FaceRecognizer:
    def __init__(self, model_name="Facenet", distance_threshold=0.4):
        """
        Optimized face recognizer with background-threaded inference.

        model_name: Facenet / VGG-Face / ArcFace (Facenet is balanced)
        distance_threshold: lower = stricter matching
        """
        self.model_name = model_name
        self.distance_threshold = distance_threshold

        self.known_embeddings = []  # list of np arrays
        self.known_names = []       # list of str (person name per embedding)

        # --- Threading for non-blocking recognition ---
        self._lock = threading.Lock()
        self._latest_frame = None
        self._latest_results = []  # list of {"name": str, "box": dict}
        self._running = False
        self._thread = None

        # --- Performance tuning ---
        self._process_interval = 0.15  # seconds between recognition cycles (~6-7 Hz)

        # Pre-warm the model so first frame isn't extra slow
        self._warm_up_model()

    def _warm_up_model(self):
        """Run a dummy inference to load the model into memory."""
        try:
            dummy = np.zeros((160, 160, 3), dtype=np.uint8)
            DeepFace.represent(
                dummy,
                model_name=self.model_name,
                enforce_detection=False,
                detector_backend="skip"
            )
        except Exception:
            pass

    # -------------------------------------------------
    # Known face loading
    # -------------------------------------------------

    def load_known_faces(self, embeddings, names):
        """Load whitelist embeddings directly."""
        self.known_embeddings = embeddings
        self.known_names = names

    def load_known_faces_from_folder(self, folder_path):
        """
        Load known faces from a folder. Supports two layouts:

        Flat files:   known_faces/PersonName.jpg       → name = "PersonName"
        Subfolders:   known_faces/PersonName/img1.jpg  → name = "PersonName"
                      known_faces/PersonName/img2.jpg  → (multiple images = better accuracy)
        """
        embeddings = []
        names = []

        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)

            if os.path.isdir(entry_path):
                # --- Subfolder: each image inside belongs to this person ---
                person_name = entry
                for img_file in os.listdir(entry_path):
                    if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                        img_path = os.path.join(entry_path, img_file)
                        emb = self._extract_embedding_from_path(img_path)
                        if emb is not None:
                            embeddings.append(emb)
                            names.append(person_name)
                            print(f"  ✓ Loaded face: {person_name} ({img_file})")

            elif entry.lower().endswith((".jpg", ".png", ".jpeg")):
                # --- Flat file: filename is the person name ---
                person_name = os.path.splitext(entry)[0]
                emb = self._extract_embedding_from_path(entry_path)
                if emb is not None:
                    embeddings.append(emb)
                    names.append(person_name)
                    print(f"  ✓ Loaded face: {person_name}")

        self.known_embeddings = embeddings
        self.known_names = names
        print(f"  Total known face embeddings: {len(embeddings)}")

    def _extract_embedding_from_path(self, img_path):
        """Extract embedding from an image file path."""
        try:
            img = cv2.imread(img_path)
            if img is None:
                return None
            return self._extract_embedding(img)
        except Exception:
            return None

    def _extract_embedding(self, face_img):
        """Extract embedding using DeepFace."""
        try:
            result = DeepFace.represent(
                face_img,
                model_name=self.model_name,
                enforce_detection=False
            )
            return np.array(result[0]["embedding"])
        except Exception:
            return None

    # -------------------------------------------------
    # Background-threaded recognition
    # -------------------------------------------------

    def start(self):
        """Start the background recognition thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._recognition_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the background recognition thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def submit_frame(self, frame):
        """Submit a new frame for recognition (non-blocking)."""
        with self._lock:
            self._latest_frame = frame.copy()

    def get_results(self):
        """
        Get the latest recognition results (non-blocking).

        Returns:
            list of {"name": str, "box": {"x": int, "y": int, "w": int, "h": int}}
        """
        with self._lock:
            return list(self._latest_results)

    def _recognition_loop(self):
        """Background loop that processes frames at a controlled rate."""
        while self._running:
            frame = None
            with self._lock:
                if self._latest_frame is not None:
                    frame = self._latest_frame.copy()

            if frame is not None:
                results = self._process_frame(frame)
                with self._lock:
                    self._latest_results = results

            time.sleep(self._process_interval)

    def _process_frame(self, frame):
        """
        Run face detection + recognition on a frame.
        Returns a list of face results (supports multiple faces).
        """
        try:
            representations = DeepFace.represent(
                img_path=frame,
                model_name=self.model_name,
                enforce_detection=True,
                detector_backend="opencv"
            )
        except Exception:
            return []

        results = []
        for rep in representations:
            embedding = rep["embedding"]
            facial_area = rep["facial_area"]

            # Match against all known embeddings
            best_distance = float("inf")
            best_name = "UNKNOWN"

            for i, known_emb in enumerate(self.known_embeddings):
                dist = cosine(embedding, known_emb)
                if dist < best_distance:
                    best_distance = dist
                    best_name = self.known_names[i]

            if best_distance >= self.distance_threshold:
                best_name = "UNKNOWN"

            results.append({
                "name": best_name,
                "box": facial_area
            })

        return results

    # -------------------------------------------------
    # Legacy synchronous API (kept for backward compat)
    # -------------------------------------------------

    def recognize(self, frame):
        """
        Synchronous single-face recognition (legacy).
        Prefer using start() + submit_frame() + get_results() for performance.
        """
        results = self._process_frame(frame)
        if not results:
            return "UNKNOWN", None
        first = results[0]
        return first["name"], first["box"]