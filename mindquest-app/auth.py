import os
import random
import bcrypt
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')

def verificar_senha(senha_digitada: str, hash_salvo: str) -> bool:
    senha_bytes = senha_digitada.encode('utf-8')[:72]
    hash_bytes = hash_salvo.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)

def gerar_codigo_mfa(email: str) -> str:
    codigo = f"{random.randint(100000, 999999)}"
    try:
        resend.Emails.send({
            "from": "MindQuest <onboarding@resend.dev>",
            "to": [email],
            "subject": "MindQuest - Código de Verificação (MFA)",
            "html": f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f9;">
                <h2 style="color: #4A90E2;">Seu código de acesso ao MindQuest</h2>
                <p>Use o código abaixo para concluir seu login:</p>
                <div style="font-size: 28px; font-weight: bold; letter-spacing: 5px; color: #2C3E50; margin: 20px 0;">
                    {codigo}
                </div>
            </div>
            """
        })
    except Exception as e:
        print(f"Erro ao enviar e-mail MFA: {e}")
    return codigo

def validar_codigo_mfa(email: str, codigo: str) -> bool:
    return bool(codigo and len(codigo) == 6 and codigo.isdigit())

def gerar_codigo_recuperacao(email: str) -> str:
    codigo = f"{random.randint(100000, 999999)}"
    try:
        resend.Emails.send({
            "from": "MindQuest <onboarding@resend.dev>",
            "to": [email],
            "subject": "MindQuest - Recuperação de Senha",
            "html": f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f9;">
                <h2 style="color: #E74C3C;">Recuperação de Senha - MindQuest</h2>
                <p>Você solicitou a redefinição da sua senha. Use o código abaixo:</p>
                <div style="font-size: 28px; font-weight: bold; letter-spacing: 5px; color: #2C3E50; margin: 20px 0;">
                    {codigo}
                </div>
                <p style="font-size: 12px; color: #777;">Se não solicitou, ignore esta mensagem.</p>
            </div>
            """
        })
        print(f"E-mail de recuperação enviado com sucesso para {email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail de recuperação: {e}")
    return codigo

def validar_codigo_recuperacao(email: str, codigo: str) -> bool:
    return bool(codigo and len(codigo) == 6 and codigo.isdigit())