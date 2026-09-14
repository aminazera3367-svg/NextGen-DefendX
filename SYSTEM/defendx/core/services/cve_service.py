import httpx

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def extract_severity(metrics):
    try:
        # Check for V3.1 metrics first
        return metrics["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
    except:
        return "UNKNOWN"

async def fetch_latest_cves(limit=5, keyword=None, cvss_level=None):
    params = {"resultsPerPage": limit}
    
    if keyword:
        params["keywordSearch"] = keyword
    
    # This is the "Magic" line that fixes the empty []
    if cvss_level:
        params["cvssV3Severity"] = cvss_level

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.get(URL, params=params)
            data = res.json()
            
            results = []
            for v in data.get("vulnerabilities", []):
                cve = v["cve"]
                # Extract severity safely
                metrics = cve.get("metrics", {})
                severity = "UNKNOWN"
                if "cvssMetricV31" in metrics:
                    severity = metrics["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
                
                results.append({
                    "id": cve["id"],
                    "desc": cve["descriptions"][0]["value"][:120],
                    "severity": severity
                })
            return results
        except Exception as e:
            return [{"error": str(e)}]