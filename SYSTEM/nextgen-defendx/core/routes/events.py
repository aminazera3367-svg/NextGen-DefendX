from fastapi import APIRouter
from models.event_model import Event
from services.pipeline import run_pipeline

router = APIRouter()

@router.post("/events")
def process_event(event: Event):
    return run_pipeline(event.dict())