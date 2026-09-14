from pydantic import BaseModel

class Event(BaseModel):
    asset: str
    event: str