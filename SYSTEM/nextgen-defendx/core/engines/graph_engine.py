def build_graph(correlation):
    if not correlation:
        return None

    assets = correlation.get("assets", [])

    nodes = [{"id": a} for a in assets]
    edges = []

    for i in range(len(assets) - 1):
        edges.append({
            "source": assets[i],
            "target": assets[i+1],
            "label": correlation["attack_type"]
        })

    return {"nodes": nodes, "edges": edges}