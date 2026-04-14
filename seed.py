import os
from database import get_db, engine, Base
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

user_service = UserService()
criteria_service = CriteriaService()

try:
    with get_db() as db:
        # Criação dos usuários
        user_service.create_user(db, "Arthur", "arthur@gmail.com", "123")
        user_service.create_user(db, "Maria", "maria@gmail.com", "456")
        print("Usuários criados com sucesso!")

        # --- Critérios do Arthur (user_id = 1) ---
        criteria_service.create_criteria(db, "Critério de Avaliação 1", "Descrição detalhada para o critério 1.", 1)
        criteria_service.create_criteria(db, "Critério de Avaliação 2", "Descrição detalhada para o critério 2.", 1)
        criteria_service.create_criteria(db, "Critério de Avaliação 3", "Descrição detalhada para o critério 3.", 1)
        criteria_service.create_criteria(db, "Critério de Avaliação 4", "Descrição detalhada para o critério 4.", 1)
        criteria_service.create_criteria(db, "Critério de Avaliação 5", "Descrição detalhada para o critério 5.", 1)
        criteria_service.create_criteria(db, "Critério de Avaliação 6", "Descrição detalhada para o critério 6.", 1)

        # --- Critérios da Maria (user_id = 2) ---
        criteria_service.create_criteria(db, "Critério de Avaliação 1", "Descrição detalhada para o critério 1.", 2)
        criteria_service.create_criteria(db, "Critério de Avaliação 2", "Descrição detalhada para o critério 2.", 2)
        criteria_service.create_criteria(db, "Critério de Avaliação 3", "Descrição detalhada para o critério 3.", 2)
        
        print("Critérios criados com sucesso!")
except Exception as e:
    print(f"Erro ao popular banco: {e}")