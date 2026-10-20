
from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE(), 1"))
        database_name, check = result.one()

        print(f"Connected to database: {database_name}")
        print(f"Connection test: {'PASSED' if check == 1 else 'FAILED'}")
except Exception as exc:
    print(f"Database connection failed: {exc}")
