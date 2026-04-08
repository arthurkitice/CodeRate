import os
from database import SessionLocal, engine, Base
from services.user_service import UserService
from services.criteria_service import CriteriaService

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
user_service = UserService()
criteria_service = CriteriaService()


try:
    user_service.create_user(db, "Arthur", "arthur@gmail.com", "123")
    user_service.create_user(db, "Maria", "maria@gmail.com", "456")
    print("Usuários criados com sucesso!")

    criteria_service.create_criteria(db, "Critério de Avaliação 1", "Descrição detalhada do primeiro critério de avaliação.", 1)
    criteria_service.create_criteria(db, "Critério de Avaliação 2", "Descrição detalhada do segundo critério de avaliação.", 1)
    criteria_service.create_criteria(db, "Critério de Avaliação 3", "Descrição detalhada do terceiro critério de avaliação.", 2)
    print("Critérios criados com sucesso!")
finally:
    db.close()