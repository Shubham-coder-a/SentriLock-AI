import os
from datetime import datetime

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "security_log.txt")


def log_alert(message):

    # folder create अगर नहीं है
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    # time add
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # write log
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")