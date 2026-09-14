from fastapi import FastAPI
from routes.events import router as events_router
from routes.intel import router as intel_router

app = FastAPI(title="NextGen DefendX Core")

app.include_router(events_router)
app.include_router(intel_router)