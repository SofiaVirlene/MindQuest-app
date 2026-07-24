from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    
    # Perfil e Identificação
    perfil = Column(String(50), nullable=False, default="autodidata")
    instituicao = Column(String(100), nullable=True)
    matricula = Column(String(50), nullable=True)
    
    # Camada de Gamificação (MindQuest)
    xp = Column(Integer, default=0)
    nivel = Column(Integer, default=1)
    
    criado_em = Column(DateTime, default=datetime.utcnow)