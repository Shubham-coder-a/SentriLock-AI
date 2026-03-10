import subprocess
import re
from known_devices import KNOWN_DEVICES
from logger import log_alert
from vendor_lookup import get_vendor
from device_tracker import check_new_devices
from hostname_lookup import get_hostname

def scan_wifi():

    print("Scanning network for connected devices...\n")

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

                print(f"✅ Known Device: {KNOWN_DEVICES[mac]} | IP: {ip} | Host: {hostname}")

            else:

                alert = f"⚠ Unknown device detected: {mac} | Vendor: {vendor} | IP: {ip} | Host: {hostname}"

                print(alert)

                log_alert(alert)

        new_devices = check_new_devices(current_devices)

        for mac in new_devices:

            vendor = get_vendor(mac)

            print(f"🚨 New device joined network: {mac} | Vendor: {vendor}")

            log_alert(f"New device joined network: {mac} | Vendor: {vendor}")

        return list(current_devices)

    except Exception as e:
        print("Error scanning network:", e)
        return []