def score(stride, mitre, criticality=5):
    score = 0

    for s in stride:
        score += 2 if s["type"] == "Elevation of Privilege" else 1

    for m in mitre:
        score += 2 if m["tactic"] == "Exfiltration" else 1

    score += criticality * 0.2

    return round(score, 2)