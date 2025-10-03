from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema, EventCreateSchema, EventUpdateSchema

router = APIRouter()


# Get data here
# List view
# GET /api/events
@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return {"results": [{"id": 1}, {"id": 2}, {"id": 3}], "count": 3}


# Send data here
# create view
# POST /api/events/
@router.post("/")
def create_event(payload: EventCreateSchema) -> EventSchema:
    # a bunch of items in a table
    print(payload.page)
    data = payload.model_dump()  # payload -> dict (pydantic)
    return {"id": 123, **data}  # unpack data


# GET /api/events/12
@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    # a single row
    return {"id": event_id}


# Update this data
# PUT /api/events/12
@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventSchema:
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
