import os
from database import get_db, engine, Base
 
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

 
criteria_service = CriteriaService()

try:
    with get_db() as db:
        criteria_service.create_criteria("Critério de Avaliação 1", "Descrição detalhada para o critério 1.")
        criteria_service.create_criteria("Critério de Avaliação 2", "Descrição detalhada para o critério 2.")
        criteria_service.create_criteria("Critério de Avaliação 3", "Descrição detalhada para o critério 3.")
        criteria_service.create_criteria("Critério de Avaliação 4", "Descrição detalhada para o critério 4.")
        criteria_service.create_criteria("Critério de Avaliação 5", "Descrição detalhada para o critério 5.")
        criteria_service.create_criteria("Critério de Avaliação 6", "Descrição detalhada para o critério 6.")
        
        print("Critérios criados com sucesso!")
except Exception as e:
    print(f"Erro ao popular banco: {e}")