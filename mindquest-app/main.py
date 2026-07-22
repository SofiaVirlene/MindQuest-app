import random
import time
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Usuario
from auth import gerar_hash_senha, verificar_senha

# Cria as tabelas automaticamente no PostgreSQL na inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MindQuest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memória temporária apenas para códigos MFA ativos (expiram em 60s)
mfa_codigos = {}

# --- Schemas de Entrada (Pydantic) ---
class CadastroRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class MFARequest(BaseModel):
    email: EmailStr
    codigo: str

class RecuperarSenhaRequest(BaseModel):
    email: EmailStr

class RedefinirSenhaRequest(BaseModel):
    email: EmailStr
    nova_senha: str


# --- Endpoints da API ---

@app.post("/cadastrar", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: CadastroRequest, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {"message": "Usuário cadastrado com sucesso!", "usuario_id": novo_usuario.id}


@app.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    # Gerar código MFA simulado de 6 dígitos
    codigo = f"{random.randint(100000, 999999)}"
    mfa_codigos[dados.email] = {
        "codigo": codigo,
        "expira_em": time.time() + 60
    }
    
    print("\n" + "="*50)
    print(f"🔒 [MFA GERADO] Código para {dados.email}: {codigo} (Válido por 60s)")
    print("="*50 + "\n")
    
    return {"message": "Credenciais válidas. Autenticação MFA requerida."}


@app.post("/verificar-mfa")
def verificar_mfa(dados: MFARequest, db: Session = Depends(get_db)):
    registro = mfa_codigos.get(dados.email)
    
    if not registro:
        raise HTTPException(status_code=400, detail="Nenhum código gerado para este e-mail.")
    
    if time.time() > registro["expira_em"]:
        del mfa_codigos[dados.email]
        raise HTTPException(status_code=400, detail="O código expira! Solicite um novo.")
        
    if registro["codigo"] != dados.codigo:
        raise HTTPException(status_code=400, detail="Código incorreto.")
    
    del mfa_codigos[dados.email]
    
    # Busca dados atualizados do banco para retornar ao perfil
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    
    return {
        "status": "sucesso",
        "usuario": usuario.nome,
        "xp": usuario.xp,
        "nivel": usuario.nivel
    }


@app.post("/recuperar-senha")
def recuperar_senha(dados: RecuperarSenhaRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="E-mail não cadastrado.")
    
    print("\n" + "="*50)
    print(f"📧 [EMAIL SIMULADO] Link de redefinição para: {dados.email}")
    print("="*50 + "\n")
    return {"message": "Link de recuperação gerado."}


@app.post("/redefinir-senha")
def redefinir_senha(dados: RedefinirSenhaRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="E-mail não encontrado.")
    
    usuario.senha_hash = gerar_hash_senha(dados.nova_senha)
    db.commit()
    
    print("\n" + "="*50)
    print(f"✅ [SENHA ATUALIZADA] Nova senha hash gerada para {dados.email}")
    print("="*50 + "\n")
    return {"message": "Senha atualizada com sucesso no banco de dados."}