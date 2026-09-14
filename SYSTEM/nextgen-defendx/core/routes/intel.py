from fastapi import APIRouter
from services.cve_service import fetch_latest_cves

router = APIRouter()

@router.get("/cves")
def get_cves():
    return fetch_latest_cves()