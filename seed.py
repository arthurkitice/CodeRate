from database import SessionLocal, engine, Base
from repositories.user_repository import UserRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()
repo = UserRepository()

try:
    repo.create(db, "Arthur", "arthur@gmail.com", "123")
    repo.create(db, "Maria", "maria@gmail.com", "456")
finally:
    db.close()