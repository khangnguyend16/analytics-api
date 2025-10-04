import sqlmodel
from sqlmodel import SQLModel
from .config import DATABASE_URL

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

# engine là cái cầu nối tới database (do SQLAlchemy cung cấp).
# Nó biết cách gửi query tới DB (SQLite, PostgreSQL, MySQL…).
# Tất cả session/transaction sẽ dựa vào engine.

engine = sqlmodel.create_engine(DATABASE_URL)


def init_db():
    print("creating database")
    # Đọc tất cả model đã định nghĩa (class kế thừa từ SQLModel) rồi tạo bảng trong DB nếu chưa có
    SQLModel.metadata.create_all(engine)
