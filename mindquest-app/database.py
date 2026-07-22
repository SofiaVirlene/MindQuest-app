from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Formato: postgresql://usuario:senha@localhost:5432/nome_do_banco
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:22122000@localhost:5432/mindquest_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency de sessão do banco para as rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()