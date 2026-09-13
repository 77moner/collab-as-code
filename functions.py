def is_online(device):
    # Placeholder function to check if a device is online
    return device["connected"]

devices = [
    {"name": "Board A", "connected": True},
    {"name": "Board B", "connected": False},
]

for d in devices:
    status = "ONLINE" if is_online(d) else "OFFLINE"
    print(f"{d['name']}: {status}")