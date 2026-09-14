import sys
import os
import requests
import json
import asyncio
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# --- 1. PATH CONFIGURATION (Fixes ModuleNotFoundError: No module named 'core') ---
# This looks one level up from the /ai folder to find the /core folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# --- 2. LOCAL IMPORTS ---
from prompt_engine import build_prompt
from response_parser import safe_parse
from config import OLLAMA_URL, MODEL, TIMEOUT
from core.services.cve_service import fetch_latest_cves

# --- 3. APP INITIALIZATION ---
app = FastAPI(title="NextGen DefendX - Unified AI Brain")

# --- 4. CORS MIDDLEWARE (Fixes Dashboard.html connection) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM1_URL = "http://127.0.0.1:8000"

# --- 5. ROUTES ---

@app.get("/health")
def health_check():
    return {"status": "online", "system1_target": SYSTEM1_URL}

@app.post("/analyze_full")
async def analyze_full(asset: str, event_text: str):
    """
    MASTER PIPELINE:
    1. Detection (System 1 .exe)
    2. Intelligence (System 2 CVEs)
    3. Prediction & Remediation (System 3 GenAI)
    """
    
    # STEP A: Get Detection from System 1 (.exe)
    try:
        s1_res = requests.post(
            f"{SYSTEM1_URL}/events", 
            json={"asset": asset, "event": event_text}, 
            timeout=5
        )
        detection_data = s1_res.json()
    except Exception as e:
        detection_data = {"error": "System 1 (.exe) is offline", "details": str(e)}

    # STEP B: Get Intel from System 2 (CVEs)
    try:
        # Asset name (e.g., 'apache') acts as the search keyword
        cve_intel = await fetch_latest_cves(limit=3, keyword=asset)
    except Exception:
        cve_intel = []

    # STEP C: Combine Context
    combined_context = {
        "asset": asset,
        "stride": detection_data.get("stride", "Unknown"),
        "mitre": detection_data.get("mitre", "Unknown"),
        "attack_story": detection_data.get("attack_story", "Unknown"),
        "threat_score": detection_data.get("threat_score", 0),
        "vulnerabilities": cve_intel
    }

    # STEP D: Call GenAI (Ollama/Llama3) with Retry Logic
    prompt = build_prompt(combined_context)
    
    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.0}
            },
            timeout=TIMEOUT
        )
        res.raise_for_status()
        raw_ai_text = res.json().get("response", "")
        
        # Parse text into structured JSON for the Dashboard
        parsed_report = safe_parse(raw_ai_text)
        
        return {
            "status": "success",
            "prediction_report": parsed_report,
            "debug_context": combined_context
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"AI Engine Error: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)