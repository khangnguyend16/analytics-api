import os
from fastapi import APIRouter
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema

router = APIRouter()
from api.db.config import DATABASE_URL


# Get data here
# List view
# GET /api/events
@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    return {"results": [{"id": 1}, {"id": 2}, {"id": 3}], "count": 3}


# Send data here
# create view
# POST /api/events/
@router.post("/")
def create_event(payload: EventCreateSchema) -> EventModel:
    # a bunch of items in a table
    print(payload.page)
    data = payload.model_dump()  # payload -> dict (pydantic)
    return {"id": 123, **data}  # unpack data


# GET /api/events/12
@router.get("/{event_id}")
def get_event(event_id: int) -> EventModel:
    # a single row
    return {"id": event_id}


# Update this data
# PUT /api/events/12
@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    # a single row
    print(payload.description)
    data = payload.model_dump()  # payload -> dict (pydantic)
    return {"id": event_id, **data}  # # unpack data


# # Delete this data
# # PUT /api/events/12
# @router.put("/{event_id}")
# def update_event(event_id: int, payload: dict = {}) -> EventSchema:
#     # a single row
#     return {"id": event_id}
