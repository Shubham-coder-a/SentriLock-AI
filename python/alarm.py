import threading
import winsound


def intruder_alarm():

    def play():
        for i in range(5):
            winsound.Beep(1500, 500)  # frequency, duration

    threading.Thread(target=play, daemon=True).start()



# import pygame
# import threading
# import os

# def intruder_alarm():

#     def play():

#         pygame.mixer.init()

#         base = os.path.dirname(__file__)
#         sound_path = os.path.join(base, "sounds/alarm.wav")

#         pygame.mixer.music.load(sound_path)
#         pygame.mixer.music.play()

#     threading.Thread(target=play, daemon=True).start()