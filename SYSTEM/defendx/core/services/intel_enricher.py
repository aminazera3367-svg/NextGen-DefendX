def map_severity_to_score(severity):
    mapping = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }
    return mapping.get(severity, 0)


def enrich_with_cve(threat_data, cves):
    if not cves:
        return threat_data

    highest = max(cves, key=lambda x: map_severity_to_score(x["severity"]))

    threat_data["cve_context"] = {
        "top_cve": highest["id"],
        "severity": highest["severity"],
        "impact_score": map_severity_to_score(highest["severity"])
    }

    return threat_data