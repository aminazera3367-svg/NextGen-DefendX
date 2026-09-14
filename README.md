# NextGen DefendX

**A unified, AI-assisted SOC (Security Operations Center) engine** that takes in raw security events and turns them into a scored, explained, and visualized threat picture — built for Idea 2.0, Hackathon 2026.

## What it does

When a security event comes in, DefendX runs it through a pipeline:

1. **STRIDE Classification** — categorizes the event (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
2. **MITRE ATT&CK Mapping** — maps the STRIDE category to relevant MITRE technique IDs and enriches them with technique details
3. **Correlation** — links the event to related activity to build an "attack story" instead of an isolated alert
4. **Live CVE Enrichment** — fetches current CVE data and factors it into the threat assessment
5. **Scoring** — produces a single threat score from the STRIDE + MITRE analysis (boosted when relevant CVEs are found)
6. **Graph Generation** — builds a visual attack graph from the correlated events

The result is served through a FastAPI backend (`/events`, `/cves` endpoints) and rendered on a web dashboard for analysts.

## Architecture

\```
Event → STRIDE Engine → MITRE Engine → Correlation Engine
                                              ↓
                                        CVE Service (live fetch)
                                              ↓
                                        Scoring Engine
                                              ↓
                                        Graph Engine → Dashboard
\```

## Tech stack

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: HTML/Tailwind dashboard (`dashboard.html`)
- **Packaging**: PyInstaller (for the standalone `run_core` executable)

## Running it

\```
cd "SYSTEM/nextgen-defendx"
pip install fastapi uvicorn requests
uvicorn core.main:app --reload
\```

Open `SYSTEM/dashboard.html` in a browser to view the SOC dashboard.

## Team

Team Cognita — Idea 2.0, Hackathon 2026
