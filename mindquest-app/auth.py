import bcrypt
import random

def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')

def verificar_senha(senha_digitada: str, hash_salvo: str) -> bool:
    senha_bytes = senha_digitada.encode('utf-8')[:72]
    hash_bytes = hash_salvo.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)

def gerar_codigo_mfa(email: str):
    codigo = f"{random.randint(100000, 999999)}"
    print(f"Código MFA para {email}: {codigo}")
    return codigo