from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import SQLModel, Field
import sqlmodel
from datetime import datetime, timezone


def get_utc_now():
    # Lấy thời điểm hiện tại (bây giờ) theo múi giờ UTC (Universal Time Coordinated)
    # Đảm bảo object datetime có thông tin timezone đi kèm (tzinfo=UTC).
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime = Field(
        # Tự động gọi hàm khi tạo bản ghi mới
        default_factory=get_utc_now,
        # Khi tạo bảng trong DB (SQLAlchemy layer), cột này là kiểu TIMESTAMP WITH TIME ZONE — nghĩa là lưu cả thông tin múi giờ
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int
