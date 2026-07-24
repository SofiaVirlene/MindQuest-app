import bcrypt

def gerar_hash_senha(senha: str) -> str:
    # Trunca a senha em 72 bytes por segurança antes de gerar o hash
    senha_bytes = senha.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')

def verificar_senha(senha_digitada: str, hash_salvo: str) -> bool:
    senha_bytes = senha_digitada.encode('utf-8')[:72]
    hash_bytes = hash_salvo.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)