from mac_vendor_lookup import MacLookup

lookup = MacLookup()

def get_vendor(mac):

    try:
        vendor = lookup.lookup(mac)
        return vendor
    except:
        return "Unknown Vendor"