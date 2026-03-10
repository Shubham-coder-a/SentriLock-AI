previous_devices = set()

def check_new_devices(current_devices):

    global previous_devices

    new_devices = current_devices - previous_devices

    previous_devices = current_devices

    return new_devices