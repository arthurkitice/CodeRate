from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager  # ← ADICIONE ESTA LINHA

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ← ADICIONE ESTA FUNÇÃO ABAIXO
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db  # ← Aqui a sessão é "emprestada" pro código que chamou
        db.commit()  # ← Se chegou aqui, deu tudo certo = COMMIT
    except Exception:
        db.rollback()  # ← Se deu erro, desfaz tudo = ROLLBACK
        raise  # ← Re-lança a exceção pra quem chamou tratar
    finally:
        db.close()  # ← SEMPRE fecha a conexão, erro ou não