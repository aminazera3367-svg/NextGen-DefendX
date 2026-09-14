from collections import defaultdict
import time

store = defaultdict(list)
WINDOW = 300
MAX_EVENTS = 100

def correlate(event):
    asset = event["asset"]
    now = time.time()

    store[asset].append({"event": event["event"], "time": now})

    # cleanup old + cap size
    store[asset] = [
        e for e in store[asset]
        if now - e["time"] < WINDOW
    ][-MAX_EVENTS:]

    events = " ".join([e["event"] for e in store[asset]])

    if "login" in events and "admin" in events:
        return {
            "attack_type": "Credential Compromise",
            "stages": ["Initial Access", "Privilege Escalation"],
            "assets": [asset],
            "confidence": 0.9
        }

    return None