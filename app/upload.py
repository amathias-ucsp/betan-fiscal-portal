import os
from werkzeug.utils import secure_filename

EXTENSOES_PERMITIDAS = {'pdf', 'png', 'jpg', 'jpeg'}
TAMANHO_MAXIMO_BYTES = 10 * 1024 * 1024  # 10 MB

def ficheiro_valido(nome_ficheiro: str, tamanho: int) -> bool:
    if '.' not in nome_ficheiro:
        return False
    extensao = nome_ficheiro.rsplit('.', 1)[1].lower()
    return extensao in EXTENSOES_PERMITIDAS and tamanho <= TAMANHO_MAXIMO_BYTES
