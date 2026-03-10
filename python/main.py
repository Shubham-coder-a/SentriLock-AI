from wifi_scanner import scan_wifi
import time

print("SentriLock AI Security System Started\n")

print("Initializing modules...\n")

print("RFID Scanner Ready")
print("WiFi Scanner Ready")
print("Camera Monitor Ready")

print("\nSystem Active\n")

while True:
    scan_wifi()

    print("\nNext scan in 10 seconds...\n")

    time.sleep(10)