from playsound import playsound
import threading

def intruder_alarm():

    threading.Thread(target=playsound, args=("sounds/alarm.wav",), daemon=True).start()