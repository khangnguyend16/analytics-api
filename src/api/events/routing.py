import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api.db.session import get_session
from .models import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now,
)

router = APIRouter()
from api.db.config import DATABASE_URL


# Get data here
# List view
# GET /api/events
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # a bunch of items in a table
    query = select(EventModel).order_by(EventModel.updated_at.desc()).limit(10)
    results = session.exec(query).all()  # .all() trả về list các EventModel object.
    return {"results": results, "count": len(results)}


# Send data here
# create view
# POST /api/events/
@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)):
    # Depends là hàm (hoặc lớp) được FastAPI dùng để tự động gọi một hàm khác

    # chuyển payload từ pydantic model -> dict (chỉ cần thiết khi muốn chỉnh sửa dữ liệu trước khi tạo model)
    data = payload.model_dump()

    # tạo ra một instance hợp lệ của EventModel từ dict data
    obj = EventModel.model_validate(data)

    # Nói với SQLAlchemy “Hãy thêm object này vào danh sách chờ ghi vào DB"
    session.add(obj)

    # Ghi thay đổi vào database thật (Tức là thực hiện câu SQL INSERT INTO eventmodel (...) VALUES (...)).
    session.commit()

    # Sau khi commit, Postgres sẽ tạo id tự động (primary key).
    # session.refresh(obj) sẽ lấy lại dữ liệu mới từ DB và gán vào object obj.
    # Vì vậy, sau dòng này obj.id sẽ có giá trị (ví dụ 1).
    session.refresh(obj)

    return obj


# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


# Update this data
# PUT /api/events/12
@router.put("/{event_id}", response_model=EventModel)
def update_event(
    event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)
):
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")

    data = payload.model_dump()  # payload -> dict (pydantic)
    for key, value in data.items():
        if key == "id":
            continue
        setattr(obj, key, value)
    obj.updated_at = get_utc_now()

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# # Delete this data
# # DELETE /api/events/12
@router.delete("/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(obj)
    session.commit()
    return {"ok": True}
