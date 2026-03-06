# config.py

"""
Central configuration file for Smart Doorbell
All scoring logic and system constants are defined here.
"""

# ==============================
# Threat Level Definitions
# ==============================

THREAT_LEVELS = {
    0: "NORMAL",        # Score 0–2
    1: "SUSPICIOUS",    # Score 3–5
    2: "HIGH_THREAT"    # Score >= 6 OR weapon override
}

NORMAL_MAX_SCORE = 2
SUSPICIOUS_MAX_SCORE = 5


# ==============================
# Face Recognition Scoring
# ==============================

FACE_SCORES = {
    "KNOWN": 0,
    "UNKNOWN": 2,
    "COVERED": 3
}


# ==============================
# Dwell Time Rules
# ==============================

DWELL_SCORE_THRESHOLD = 30        # seconds
DWELL_SCORE_POINTS = 2

UNKNOWN_LONG_DWELL_SECONDS = 60
UNKNOWN_LONG_DWELL_BONUS = 2


# ==============================
# Night Time Scoring
# ==============================

NIGHT_SCORE = 2


# ==============================
# Audio Scoring
# ==============================

AUDIO_SCORES = {
    "NORMAL": 0,
    "LOUD_BANGING": 3,
    "AGGRESSIVE_SHOUTING": 3
}


# ==============================
# Camera Obstruction
# ==============================

CAMERA_OBSTRUCTION_SCORE = 5


# ==============================
# Weapon Detection
# ==============================

WEAPON_BASE_SCORE = 6
WEAPON_MIN_LEVEL = 2   # Always HIGH_THREAT

# COCO class IDs
COCO_KNIFE_ID = 43
COCO_SCISSORS_ID = 76


# ==============================
# Special Combo Bonuses
# ==============================

COVERED_NIGHT_BONUS = 3


# ==============================
# Recording Settings
# ==============================

RECORDING_FPS = 20
RECORDING_DURATION_LEVEL1 = 15   # seconds
RECORDING_DURATION_LEVEL2 = 60   # seconds


# ==============================
# General Settings
# ==============================

ENABLE_DEBUG_LOGS = True