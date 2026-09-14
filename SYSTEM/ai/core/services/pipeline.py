from engines.stride_engine import classify_stride
from engines.mitre_engine import map_to_mitre, enrich
from engines.correlation_engine import correlate
from engines.scoring_engine import score
from engines.graph_engine import build_graph

import requests


def run_pipeline(event):
    # 1. STRIDE classification
    stride = classify_stride(event["event"])

    # 2. MITRE mapping
    mitre_ids = map_to_mitre(stride)
    mitre = enrich(mitre_ids)

    # 3. Correlation
    correlation = correlate(event)

    # 4. 🔗 System 2 (CVE fetch via HTTP)
    try:
        res = requests.get("http://127.0.0.1:8001/cves", timeout=3)
        cves = res.json()
    except:
        cves = []

    # 5. Scoring
    threat_score = score(stride, mitre)

    # (Optional small boost if CVEs exist)
    if cves:
        threat_score += 2

    # 6. Graph generation
    graph = build_graph(correlation)

    # 7. Final output
    return {
        "asset": event["asset"],
        "stride": stride,
        "mitre": mitre,
        "attack_story": correlation,
        "threat_score": threat_score,
        "graph": graph,
        "cves": cves
    }