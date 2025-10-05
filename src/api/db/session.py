import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL, DB_TIMEZONE
import timescaledb
import os
from pathlib import Path

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")


# Detect if we're running inside Docker
# Docker containers have /.dockerenv file or have "docker" in cgroup
def is_running_in_docker():
    return Path("/.dockerenv").exists() or os.getenv("DOCKER_CONTAINER") == "true"


# Replace db_service with localhost ONLY when running locally (outside Docker)
if is_running_in_docker():
    # Running in Docker - use db_service as is
    database_url = DATABASE_URL
else:
    # Running locally (Jupyter/uvicorn) - replace db_service with localhost
    database_url = DATABASE_URL.replace("db_service", "localhost")

print(f"🔍 Connecting to: {database_url}")

# engine là cái cầu nối tới database (do SQLAlchemy cung cấp).
# Nó biết cách gửi query tới DB (SQLite, PostgreSQL, MySQL…).
# Tất cả session/transaction sẽ dựa vào engine.
# Tạo kết nối (engine) tới cơ sở dữ liệu TimescaleDB, đặt múi giờ mặc định cho các trường time
engine = timescaledb.create_engine(database_url, timezone=DB_TIMEZONE)


def init_db():
    print("creating database")
    # Đọc tất cả model đã định nghĩa (class kế thừa từ SQLModel) rồi tạo bảng trong DB nếu chưa có
    SQLModel.metadata.create_all(engine)
    print("creating hypertables")
    timescaledb.metadata.create_all(engine)


# Session: là phiên làm việc với database, nơi ta có thể:
# Thêm, xoá, sửa, truy vấn dữ liệu.
# Sau khi làm xong thì phải đóng session để giải phóng tài nguyên


def get_session():
    with Session(engine) as session:
        yield session  # Tạm dừng hàm tại đây, trả session cho bên ngoài dùng


# Khi khối with kết thúc, session tự động đóng lại
