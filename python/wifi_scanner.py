import subprocess
import re
import time
from known_devices import KNOWN_DEVICES
from logger import log_alert
from vendor_lookup import get_vendor
from device_tracker import check_new_devices
from hostname_lookup import get_hostname
from alarm import intruder_alarm
from camera_capture import capture_intruder
from telegram_alert import send_alert, send_photo
from face_detection import detect_face

# 🔔 Startup message
send_alert("🚀 SentriLock AI Started Successfully")
# cooldown memory
LAST_INTRUDER_ALERT = {}

# seconds cooldown
ALERT_COOLDOWN = 30

def scan_wifi():

    print("Scanning network for connected devices...\n")

    devices = []

    try:

        result = subprocess.check_output("arp -a", shell=True).decode()

        pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})"
        matches = re.findall(pattern, result)

        ignored_prefixes = ("01-00-5e", "ff-ff-ff")

        current_devices = set()

        print("Detected Devices:\n")

        for ip, mac in matches:

            mac_lower = mac.lower()

            if mac_lower.startswith(ignored_prefixes):
                continue

            current_devices.add(mac)

            hostname = get_hostname(ip)
            vendor = get_vendor(mac)

            # ✅ Known Device
            if mac in KNOWN_DEVICES:

                status = "Known"

                print(f"✅ Known Device: {KNOWN_DEVICES[mac]} | IP: {ip}")

                        # 🚨 Intruder Detected
            else:

                status = "Unknown"

                alert = f"⚠ Intruder detected: {mac} | IP: {ip}"

                print(alert)

                current_time = time.time()

                # check cooldown
                last_time = LAST_INTRUDER_ALERT.get(mac, 0)

                if current_time - last_time > ALERT_COOLDOWN:

                    LAST_INTRUDER_ALERT[mac] = current_time

                    intruder_alarm()  # 🔊 alarm

                    image_path = capture_intruder()  # 📸 capture

                    send_alert(alert)  # 📲 telegram alert

                    if image_path:

                        face_found = detect_face(image_path)

                        if face_found:
                            print("🧠 Face Detected")
                            send_alert("🚨 Intruder detected WITH FACE")
                        else:
                            print("❌ No Face Detected")
                            send_alert("⚠ Intruder detected (no face)")

                        send_photo(image_path)

                    log_alert(alert)

                else:
                    print(f"⏳ Cooldown active for {mac}, skipping alert/photo")
        # 🔁 New device tracking
        new_devices = check_new_devices(current_devices)

        for mac in new_devices:

            vendor = get_vendor(mac)

            print(f"🚨 New device joined network: {mac} | Vendor: {vendor}")

            log_alert(f"New device joined network: {mac} | Vendor: {vendor}")

        return devices

    except Exception as e:
        print("Error scanning network:", e)
        return []