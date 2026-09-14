#!/usr/bin/env python3
"""
Test the parser with real Ollama responses
Run: python test_parser.py
"""

import requests
import json
from prompt_engine import build_prompt
from response_parser import safe_parse
from config import OLLAMA_URL, MODEL, TIMEOUT

def test_with_sample():
    """Test with a hardcoded sample response"""
    print("=" * 60)
    print("TEST 1: Sample Response")
    print("=" * 60)
    
    sample_response = """
    {
      "attack_summary": "SQL injection attempt detected",
      "risk_level": "HIGH",
      "key_indicators": ["unusual_query", "quote_markers"],
      "recommended_actions": ["block_ip", "alert_team"],
      "confidence": 0.85
    }
    """
    
    parsed = safe_parse(sample_response)
    print(f"Input: {sample_response}")
    print(f"Parsed: {json.dumps(parsed, indent=2)}")
    print()

def test_with_ollama():
    """Test with real Ollama"""
    print("=" * 60)
    print("TEST 2: Real Ollama Response")
    print("=" * 60)
    
    test_data = {
        "asset": "web_app_server",
        "stride": "Tampering",
        "mitre": "T1190 - Exploit Public-Facing Application",
        "attack_story": "Attacker sends malicious input to bypass authentication",
        "threat_score": 8.5
    }
    
    prompt = build_prompt(test_data)
    print(f"Prompt:\n{prompt}\n")
    
    try:
        print("Sending request to Ollama...")
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=TIMEOUT
        )
        
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}\n")
        
        raw_response = res.json().get("response", "")
        print(f"Raw Ollama Output:\n{raw_response}\n")
        
        parsed = safe_parse(raw_response)
        print(f"Parsed Result:\n{json.dumps(parsed, indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Ollama at", OLLAMA_URL)
        print("Make sure Ollama is running: ollama serve")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()

if __name__ == "__main__":
    test_with_sample()
    test_with_ollama()
