from datetime import datetime

def log_alert(message):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = f"[{current_time}] {message}\n"

    with open("logs/security_log.txt", "a") as file:
        file.write(log_message)