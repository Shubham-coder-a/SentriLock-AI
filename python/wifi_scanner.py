import subprocess
import re
from known_devices import KNOWN_DEVICES
from logger import log_alert
from vendor_lookup import get_vendor
from device_tracker import check_new_devices
from hostname_lookup import get_hostname
from alarm import intruder_alarm
from camera_capture import capture_intruder


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

            if mac in KNOWN_DEVICES:

                status = "Known"

                print(f"✅ Known Device: {KNOWN_DEVICES[mac]} | IP: {ip}")

            else:

                status = "Unknown"

                alert = f"⚠ Unknown device detected: {mac} | IP: {ip}"

                print(alert)

                intruder_alarm()

                capture_intruder()

                log_alert(alert)

            devices.append({
                "ip": ip,
                "mac": mac,
                "vendor": vendor,
                "hostname": hostname,
                "status": status
            })

        new_devices = check_new_devices(current_devices)

        for mac in new_devices:

            vendor = get_vendor(mac)

            print(f"🚨 New device joined network: {mac} | Vendor: {vendor}")

            log_alert(f"New device joined network: {mac} | Vendor: {vendor}")

        return devices

    except Exception as e:
        print("Error scanning network:", e)
        return []