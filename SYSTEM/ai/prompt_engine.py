def build_prompt(data):
    """
    Tailored for Hackathon: Attack Prediction & Remediation.
    """
    asset = data.get("asset", "unknown")
    event = data.get("raw_event", "unknown")
    detection = data.get("detection", {})
    cves = data.get("vulnerabilities", [])

    return f"""You are an Advanced Predictive Cybersecurity AI. 
Analyze the data from System 1 (Real-time Detection) and System 2 (Threat Intel).

CURRENT INCIDENT:
- Asset: {asset}
- Event: {event}
- System 1 Detection: {detection}
- System 2 CVE Intel: {cves}

CRITICAL REQUIREMENTS:
1. attack_summary: Clear explanation of the current threat.
2. attack_prediction: Based on the behavior and CVEs, what is the attacker's NEXT likely step?
3. remediation_console_command: Provide a specific Windows PowerShell or Linux Bash command to stop this.
4. risk_level: Exactly one of: LOW, MEDIUM, HIGH, CRITICAL.
5. confidence: A number between 0 and 1.

Respond ONLY with a valid JSON object. No conversational text.

JSON Schema:
{{
  "attack_summary": "string",
  "attack_prediction": "string",
  "remediation_console_command": "string",
  "risk_level": "string",
  "key_indicators": ["string"],
  "confidence": 0.95
}}

Response:"""