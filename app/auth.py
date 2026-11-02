from werkzeug.security import generate_password_hash, check_password_hash

def criar_hash_senha(senha_pura: str) -> str:
    return generate_password_hash(senha_pura, method='pbkdf2:sha256')

def verificar_senha(senha_hash: str, senha_pura: str) -> bool:
    return check_password_hash(senha_hash, senha_pura)
