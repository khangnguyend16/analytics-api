import sqlmodel
from sqlmodel import SQLModel, Session
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


# Session: là phiên làm việc với database, nơi ta có thể:
# Thêm, xoá, sửa, truy vấn dữ liệu.
# Sau khi làm xong thì phải đóng session để giải phóng tài nguyên


def get_session():
    with Session(engine) as session:
        yield session  # Tạm dừng hàm tại đây, trả session cho bên ngoài dùng


# Khi khối with kết thúc, session tự động đóng lại
