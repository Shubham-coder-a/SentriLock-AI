import cv2
import os
from datetime import datetime


def capture_intruder():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if ret:

        if not os.path.exists("intruders"):
            os.makedirs("intruders")

        filename = datetime.now().strftime("intruder_%Y%m%d_%H%M%S.jpg")

        path = os.path.join("intruders", filename)

        cv2.imwrite(path, frame)

        print(f"📷 Intruder photo saved: {path}")

    cap.release()