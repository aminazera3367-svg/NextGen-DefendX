import sys
import json
import os

# Pointing to data folder relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MITRE_PATH = os.path.join(BASE_DIR, "data", "mitre.json")

with open(MITRE_PATH) as f:
    MITRE_DB = json.load(f)

BEHAVIOR_MAP = {
    "authentication anomaly": ["T1078"],
    "privileged execution": ["T1068"],
    "file modification": ["T1565"],
    "log tampering": ["T1070"],
    "data access": ["T1005"],
    "traffic spike": ["T1499"],
    "brute force": ["T1110"]
}

def map_to_mitre(stride):
    techniques = []
    for s in stride:
        techniques.extend(BEHAVIOR_MAP.get(s["evidence"], []))
    return list(set(techniques))

def enrich(techniques):
    return [
        {
            "id": t,
            "name": MITRE_DB[t]["name"],
            "tactic": MITRE_DB[t]["tactic"]
        }
        for t in techniques if t in MITRE_DB
    ]