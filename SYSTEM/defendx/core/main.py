from fastapi import FastAPI
from core.routes import intel

app = FastAPI(title="NextGen DefendX")

app.include_router(intel.router, tags=["Threat Intelligence"])

@app.get("/")
async def root(name: str = "User"): # Adding 'name' here makes a parameter box appear
    return {
        "message": f"Hello {name}, System 2 Intelligence Engine is Online",
        "instructions": "Go to /docs to interact with the API"
    }