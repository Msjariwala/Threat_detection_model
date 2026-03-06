# utils/telegram_alert.py

import requests
import threading
import time


class TelegramAlert:

    def __init__(self, bot_token, chat_id, cooldown=30):
        """
        Telegram alert sender with background threading and cooldown.

        bot_token: Telegram bot API token
        chat_id: Target chat/user ID
        cooldown: Minimum seconds between alerts (prevents flooding)
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.cooldown = cooldown
        self._last_alert_time = 0
        self._lock = threading.Lock()

    def _is_on_cooldown(self):
        """Check if we're within the cooldown period."""
        return (time.time() - self._last_alert_time) < self.cooldown

    def _update_cooldown(self):
        """Mark the current time as last alert time."""
        self._last_alert_time = time.time()

    def send_message(self, message):
        """Send a text message asynchronously (non-blocking)."""
        with self._lock:
            if self._is_on_cooldown():
                return
            self._update_cooldown()

        thread = threading.Thread(
            target=self._send_message_sync,
            args=(message,),
            daemon=True
        )
        thread.start()

    def send_photo(self, image_path, caption=""):
        """Send a photo with caption asynchronously (non-blocking)."""
        with self._lock:
            if self._is_on_cooldown():
                return
            self._update_cooldown()

        thread = threading.Thread(
            target=self._send_photo_sync,
            args=(image_path, caption),
            daemon=True
        )
        thread.start()

    def send_alert(self, image_path, caption=""):
        """
        Send both photo + message in one call (non-blocking).
        This is the preferred method for threat alerts.
        """
        with self._lock:
            if self._is_on_cooldown():
                return
            self._update_cooldown()

        thread = threading.Thread(
            target=self._send_alert_sync,
            args=(image_path, caption),
            daemon=True
        )
        thread.start()

    # --- Synchronous internal methods ---

    def _send_message_sync(self, message):
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message
            }
            resp = requests.post(url, data=payload, timeout=10)
            if resp.status_code == 200:
                print("[TELEGRAM] Message sent successfully")
            else:
                print(f"[TELEGRAM] Message failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[TELEGRAM] Error sending message: {e}")

    def _send_photo_sync(self, image_path, caption):
        try:
            url = f"{self.base_url}/sendPhoto"
            with open(image_path, "rb") as photo:
                files = {"photo": photo}
                data = {
                    "chat_id": self.chat_id,
                    "caption": caption
                }
                resp = requests.post(url, files=files, data=data, timeout=15)
                if resp.status_code == 200:
                    print("[TELEGRAM] Photo sent successfully")
                else:
                    print(f"[TELEGRAM] Photo failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[TELEGRAM] Error sending photo: {e}")

    def _send_alert_sync(self, image_path, caption):
        """Send photo first, then a follow-up text message."""
        self._send_photo_sync(image_path, caption)