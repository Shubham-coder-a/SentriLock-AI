import cv2
import os
import time
from datetime import datetime


def capture_intruder():

    # wait a little before opening camera
    time.sleep(1)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not opened")
        return None

    ret, frame = cap.read()

    if ret:

        if not os.path.exists("intruders"):
            os.makedirs("intruders")

        filename = datetime.now().strftime("intruder_%Y%m%d_%H%M%S.jpg")
        path = os.path.join("intruders", filename)

        cv2.imwrite(path, frame)

        print(f"📸 Intruder photo saved: {path}")

        cap.release()
        cv2.destroyAllWindows()

        return path

    else:
        print("❌ Failed to capture image")
        cap.release()
        cv2.destroyAllWindows()
        return None