import json
import re

# Updated for Hackathon Attack Prediction & Remediation requirements
EXPECTED_FIELDS = {
    "attack_summary": str,
    "attack_prediction": str,           # Added for Prediction requirement
    "remediation_console_command": str, # Added for Remediation requirement
    "risk_level": str,
    "key_indicators": list,
    "confidence": (int, float)
}

def validate_structure(data):
    """Validate that parsed JSON matches expected structure"""
    if not isinstance(data, dict):
        return False
    
    for field, expected_type in EXPECTED_FIELDS.items():
        if field not in data:
            return False
        
        if field == "risk_level":
            # Validate risk_level is one of expected values
            if data[field] not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
                return False
        elif field == "confidence":
            # Ensure confidence is 0-1
            val = data[field]
            if not isinstance(val, (int, float)) or not (0 <= val <= 1):
                return False
        elif isinstance(expected_type, tuple):
            if not isinstance(data[field], expected_type):
                return False
        else:
            if not isinstance(data[field], expected_type):
                return False
    
    return True

def extract_json_block(text):
    """Extract JSON block from text, handling nested braces"""
    # Find first opening brace
    start = text.find('{')
    if start == -1:
        return None
    
    # Track brace depth to find matching closing brace
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    
    return None

def safe_parse(response_text):
    """Parse LLM response with robust error handling"""
    
    if not response_text or not isinstance(response_text, str):
        return _default_response()
    
    # Attempt 1: Direct JSON parse
    try:
        data = json.loads(response_text)
        if validate_structure(data):
            return data
    except json.JSONDecodeError:
        pass
    
    # Attempt 2: Extract JSON block (handles "Here's the analysis: {...}")
    try:
        json_block = extract_json_block(response_text)
        if json_block:
            data = json.loads(json_block)
            if validate_structure(data):
                return data
    except json.JSONDecodeError:
        pass
    
    # Attempt 3: Clean common formatting issues
    try:
        cleaned = response_text.strip()
        
        # Remove markdown code blocks
        cleaned = re.sub(r'```json\s*', '', cleaned)
        cleaned = re.sub(r'```\s*', '', cleaned)
        
        # Remove prefixes/suffixes like "Result:" or "Done."
        cleaned = re.sub(r'^(Result|Output|Analysis|JSON):\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*(Done|End|Finished)\.?$', '', cleaned, flags=re.IGNORECASE)
        
        # Extract JSON again after cleaning
        json_block = extract_json_block(cleaned)
        if json_block:
            data = json.loads(json_block)
            if validate_structure(data):
                return data
    except (json.JSONDecodeError, AttributeError):
        pass
    
    # Attempt 4: Aggressive repair (fix quotes, etc.)
    try:
        repaired = _repair_json(response_text)
        if repaired:
            data = json.loads(repaired)
            if validate_structure(data):
                return data
    except json.JSONDecodeError:
        pass
    
    # If all parsing attempts fail, return default
    return _default_response()

def _repair_json(text):
    """Attempt to repair common JSON issues"""
    block = extract_json_block(text)
    if not block:
        return None
    
    # Fix single quotes to double quotes (carefully)
    repaired = re.sub(r"'([^']*)'", r'"\1"', block)
    
    # Ensure keys are quoted
    repaired = re.sub(r'(\w+):', r'"\1":', repaired)
    
    try:
        json.loads(repaired)
        return repaired
    except json.JSONDecodeError:
        return None

def _default_response():
    """Return default response when parsing fails - Updated for Hackathon Schema"""
    return {
        "attack_summary": "Parsing failed - manual review required",
        "attack_prediction": "Critical analysis needed; potential escalation.",
        "remediation_console_command": "Check logs and isolate affected asset.",
        "risk_level": "UNKNOWN",
        "key_indicators": ["Detection triggered"],
        "confidence": 0.0
    }