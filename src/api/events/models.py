from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import SQLModel, Field
import sqlmodel
from datetime import datetime, timezone
from timescaledb import TimescaleModel


def get_utc_now():
    # Lấy thời điểm hiện tại (bây giờ) theo múi giờ UTC (Universal Time Coordinated)
    # Đảm bảo object datetime có thông tin timezone đi kèm (tzinfo=UTC).
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


# page visits at any given time


class EventModel(TimescaleModel, table=True):
    # REQUIRED field - must be provided
    page: str
    # The URL/path of the page being viewed (e.g., "/home", "/products/123")

    # OPTIONAL fields - have default values
    user_agent: Optional[str] = Field(default="", index=True)
    # Browser info (e.g., "Mozilla/5.0 Chrome/91.0...")
    # index=True means database will create an index for faster queries

    ip_address: Optional[str] = Field(default="", index=True)
    # User's IP address (e.g., "192.168.1.1")
    # Indexed for analytics queries

    referrer: Optional[str] = Field(default="", index=True)
    # Where the user came from (e.g., "https://google.com")
    # Useful for tracking traffic sources

    session_id: Optional[str] = Field(index=True)
    # Unique identifier to track user session
    # No default value, so it's None if not provided

    duration: Optional[int] = Field(default=0)
    # How long user stayed on page (in seconds or milliseconds)
    # Defaults to 0 if not tracked

    # configuration
    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True)  # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)


# class EventUpdateSchema(SQLModel):
#     description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int
