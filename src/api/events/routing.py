from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema

router = APIRouter()


@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return {"results": [{"id": 1}, {"id": 2}, {"id": 3}], "count": 3}


@router.get("/{event_id}")
def get_events(event_id: int) -> EventSchema:
    # a single row
    return {"id": event_id}
