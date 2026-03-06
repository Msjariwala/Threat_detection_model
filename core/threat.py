# core/threat.py

from dataclasses import dataclass
from config import (
    FACE_SCORES,
    DWELL_SCORE_THRESHOLD,
    DWELL_SCORE_POINTS,
    NIGHT_SCORE,
    AUDIO_SCORES,
    CAMERA_OBSTRUCTION_SCORE,
    WEAPON_BASE_SCORE,
    WEAPON_MIN_LEVEL,
    COVERED_NIGHT_BONUS,
    UNKNOWN_LONG_DWELL_SECONDS,
    UNKNOWN_LONG_DWELL_BONUS,
    NORMAL_MAX_SCORE,
    SUSPICIOUS_MAX_SCORE,
    THREAT_LEVELS
)


@dataclass
class ThreatResult:
    score: int
    level: int
    triggered_rules: list
    recommended_action: str
    reasoning_summary: str


class ThreatScoreEngine:

    def calculate(self,
                  face_status,
                  dwell_time,
                  is_nighttime,
                  audio_status,
                  camera_status,
                  weapon_detected):

        score = 0
        triggered_rules = []

        # -----------------------------
        # 🔥 WEAPON OVERRIDE
        # -----------------------------
        if weapon_detected:
            score = WEAPON_BASE_SCORE
            triggered_rules.append("Weapon detected → base score set to 6")

            if is_nighttime:
                score += 2
                triggered_rules.append("Weapon + Night bonus +2")

            if face_status == "COVERED":
                score += 2
                triggered_rules.append("Weapon + Covered face bonus +2")

            level = max(WEAPON_MIN_LEVEL, self._determine_level(score))

            return self._build_result(score, level, triggered_rules)

        # -----------------------------
        # 🧍 Face Scoring
        # -----------------------------
        face_score = FACE_SCORES.get(face_status, 0)
        score += face_score
        triggered_rules.append(f"Face status ({face_status}) → +{face_score}")

        # -----------------------------
        # ⏱ Dwell Time
        # -----------------------------
        if dwell_time > DWELL_SCORE_THRESHOLD:
            score += DWELL_SCORE_POINTS
            triggered_rules.append(f"Dwell > {DWELL_SCORE_THRESHOLD}s → +{DWELL_SCORE_POINTS}")

        # Special: Unknown + Long Dwell
        if face_status == "UNKNOWN" and dwell_time > UNKNOWN_LONG_DWELL_SECONDS:
            score += UNKNOWN_LONG_DWELL_BONUS
            triggered_rules.append("Unknown + >60s dwell → +2 bonus")

        # -----------------------------
        # 🌙 Night Time
        # -----------------------------
        if is_nighttime:
            score += NIGHT_SCORE
            triggered_rules.append("Night time → +2")

        # Special: Covered + Night
        if face_status == "COVERED" and is_nighttime:
            score += COVERED_NIGHT_BONUS
            triggered_rules.append("Covered + Night combo → +3 bonus")

        # -----------------------------
        # 🔊 Audio
        # -----------------------------
        audio_score = AUDIO_SCORES.get(audio_status, 0)
        score += audio_score
        if audio_score > 0:
            triggered_rules.append(f"Audio ({audio_status}) → +{audio_score}")

        # -----------------------------
        # 📷 Camera Obstruction
        # -----------------------------
        if camera_status == "OBSTRUCTED":
            score += CAMERA_OBSTRUCTION_SCORE
            triggered_rules.append("Camera obstructed → +5")

        # -----------------------------
        # Determine Level
        # -----------------------------
        level = self._determine_level(score)

        return self._build_result(score, level, triggered_rules)

    # -----------------------------
    # Helper Methods
    # -----------------------------

    def _determine_level(self, score):
        if score <= NORMAL_MAX_SCORE:
            return 0
        elif score <= SUSPICIOUS_MAX_SCORE:
            return 1
        return 2

    def _build_result(self, score, level, triggered_rules):

        level_name = THREAT_LEVELS[level]

        if level == 0:
            action = "Log event only"
        elif level == 1:
            action = "Record short clip + send alert"
        else:
            action = "Trigger alarm + continuous recording + emergency alert"

        reasoning = f"Threat Level: {level_name} | Score: {score}"

        return ThreatResult(
            score=score,
            level=level,
            triggered_rules=triggered_rules,
            recommended_action=action,
            reasoning_summary=reasoning
        )