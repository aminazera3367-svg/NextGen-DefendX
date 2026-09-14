from fastapi import APIRouter, Query
from core.services.cve_service import fetch_latest_cves

router = APIRouter()

# --- 1. Main CVE Route (Already working in your screenshot) ---
@router.get("/cves")
async def get_cves(
    limit: int = Query(5, ge=1, le=100, description="How many CVEs to return"),
    keyword: str = Query(None, description="Search term (e.g., 'apache', 'windows')")
):
    """Fetches latest vulnerabilities based on limit and keyword."""
    return await fetch_latest_cves(limit=limit, keyword=keyword)


# --- 2. Critical CVE Route (Adding parameters here now) ---
@router.get("/cves/critical")
async def get_critical_cves(limit: int = Query(10, ge=1, le=50)):
    # Now we ask the API for ONLY criticals, so you won't get []
    return await fetch_latest_cves(limit=limit, cvss_level="CRITICAL")