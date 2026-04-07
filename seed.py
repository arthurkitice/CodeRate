import os
from database import SessionLocal, engine, Base
from services.user_service import UserService

# Remove o banco de dados existente
db_url = engine.url
if db_url.drivername == "sqlite":
    db_path = db_url.database
    if db_path and os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco de dados removido: {db_path}")

# Recria todas as tabelas
Base.metadata.create_all(bind=engine)
print("Banco de dados recriado com sucesso!")

db = SessionLocal()
repo = UserService()

try:
    repo.create_user(db, "Arthur", "arthur@gmail.com", "123")
    repo.create_user(db, "Maria", "maria@gmail.com", "456")
    print("Usuários criados com sucesso!")
finally:
    db.close()