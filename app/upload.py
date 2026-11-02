import os
from werkzeug.utils import secure_filename

EXTENSOES_PERMITIDAS = {'pdf', 'png', 'jpg', 'jpeg'}
TAMANHO_MAXIMO_BYTES = 10 * 1024 * 1024  # 10 MB

def ficheiro_valido(nome_ficheiro: str, tamanho: int) -> bool:
    if not nome_ficheiro or '.' not in nome_ficheiro:
        return False
    extensao = nome_ficheiro.rsplit('.', 1)[1].lower()
    return extensao in EXTENSOES_PERMITIDAS and 0 < tamanho <= TAMANHO_MAXIMO_BYTES

def sanitizar_nome_ficheiro(nome_original: str) -> str:
    """Higieniza o nome do arquivo para mitigar path traversal e caracteres nocivos."""
    return secure_filename(nome_original)
