import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_latest_cves():
    try:
        res = requests.get(URL, params={"resultsPerPage": 5}, timeout=5)
        data = res.json()
    except:
        return []

    result = []
    for v in data.get("vulnerabilities", []):
        cve = v["cve"]
        result.append({
            "id": cve["id"],
            "desc": cve["descriptions"][0]["value"][:100]
        })

    return result