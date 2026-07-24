from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional

import database
import auth

app = FastAPI(title="MindQuest API")

# Configuração do CORS para permitir que o front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ESQUEMAS PYDANTIC (DTOs) ---

class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: str
    instituicao: Optional[str] = None
    matricula: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class LoginMFA(BaseModel):
    email: EmailStr
    codigo: str

class EsqueciSenhaRequest(BaseModel):
    email: EmailStr

class RedefinirSenhaRequest(BaseModel):
    email: EmailStr
    codigo: str
    nova_senha: str


# --- ENDPOINTS DA API ---

@app.post("/api/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCadastro):
    conn = database.get_connection()
    cursor = conn.cursor()

    # 1. Verifica se e-mail já existe
    cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (usuario.email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=400, 
            detail="Este e-mail já está cadastrado no MindQuest."
        )

    # 2. Criptografa a senha
    senha_criptografada = auth.gerar_hash_senha(usuario.senha)

    # 3. Insere o novo usuário no PostgreSQL
    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha_hash, perfil, instituicao, matricula)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        usuario.nome,
        usuario.email,
        senha_criptografada,
        usuario.perfil,
        usuario.instituicao,
        usuario.matricula
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Cadastro realizado com sucesso! Faça login para continuar."}


@app.post("/api/login")
def login_primeiro_fator(dados: UsuarioLogin):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = %s;", (dados.email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario or not auth.verificar_senha(dados.senha, usuario["senha_hash"]):
        raise HTTPException(
            status_code=401, 
            detail="E-mail ou senha incorretos."
        )

    # Gera código MFA
    codigo_mfa = auth.gerar_codigo_mfa(dados.email)

    print("\n" + "="*50)
    print(f"🔑 [MFA - 60s] Código para {dados.email}: {codigo_mfa}")
    print("="*50 + "\n")

    return {"message": "Senha correta. Código de verificação enviado."}


@app.post("/api/login/mfa")
def login_segundo_fator(dados: LoginMFA):
    valido = auth.validar_codigo_mfa(dados.email, dados.codigo)
    
    if not valido:
        raise HTTPException(
            status_code=400, 
            detail="Código de verificação inválido ou expirado (limite de 60s). Tente novamente."
        )

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, perfil FROM usuarios WHERE email = %s;", (dados.email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        "message": "Autenticação concluída com sucesso!",
        "usuario": {
            "nome": usuario["nome"],
            "email": usuario["email"],
            "perfil": usuario["perfil"]
        }
    }


@app.post("/api/esqueci-senha")
def solicitar_recuperacao(dados: EsqueciSenhaRequest):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (dados.email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario:
        raise HTTPException(status_code=404, detail="E-mail não encontrado no sistema.")

    codigo_rec = auth.gerar_codigo_recuperacao(dados.email)

    print("\n" + "="*50)
    print(f"📩 [RECUPERAÇÃO DE SENHA] Código para {dados.email}: {codigo_rec}")
    print("="*50 + "\n")

    return {"message": "Código de recuperação gerado. Verifique o terminal Python."}


@app.post("/api/redefinir-senha")
def redefinir_senha(dados: RedefinirSenhaRequest):
    if not auth.validar_codigo_recuperacao(dados.email, dados.codigo):
        raise HTTPException(status_code=400, detail="Código de recuperação inválido ou expirado.")

    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (dados.email,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="E-mail não encontrado.")

    nova_hash = auth.gerar_hash_senha(dados.nova_senha)

    cursor.execute("UPDATE usuarios SET senha_hash = %s WHERE email = %s;", (nova_hash, dados.email))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Senha redefinida com sucesso! Você já pode realizar o login."}