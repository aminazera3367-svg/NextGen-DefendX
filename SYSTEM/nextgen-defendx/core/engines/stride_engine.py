def classify_stride(event: str):
    e = event.lower()
    signals = []

    if "login" in e:
        signals.append(("Spoofing", "authentication anomaly", 0.8))
    if "failed login" in e:
        signals.append(("Spoofing", "brute force", 0.9))
    if "modified" in e:
        signals.append(("Tampering", "file modification", 0.85))
    if "log deleted" in e:
        signals.append(("Repudiation", "log tampering", 0.9))
    if "data" in e:
        signals.append(("Information Disclosure", "data access", 0.85))
    if "traffic" in e:
        signals.append(("Denial of Service", "traffic spike", 0.9))
    if "admin" in e or "sudo" in e:
        signals.append(("Elevation of Privilege", "privileged execution", 0.95))

    return [
        {"type": s[0], "evidence": s[1], "confidence": s[2]}
        for s in signals
    ]