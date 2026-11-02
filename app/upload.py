import re
from werkzeug.utils import secure_filename

EXTENSOES_PERMITIDAS = {'pdf', 'png', 'jpg', 'jpeg'}
TAMANHO_MAXIMO = 10 * 1024 * 1024  # 10 MB

def ficheiro_valido(nome_ficheiro: str, tamanho: int) -> bool:
    if not nome_ficheiro or '.' not in nome_ficheiro:
        return False
    if tamanho <= 0 or tamanho > TAMANHO_MAXIMO:
        return False
    extensao = nome_ficheiro.rsplit('.', 1)[1].lower()
    return extensao in EXTENSOES_PERMITIDAS

def sanitizar_nome_ficheiro(nome_ficheiro: str) -> str:
    # Remove eventuais caminhos transversais e caracteres especiais
    nome_seguro = secure_filename(nome_ficheiro)
    # Se o nome original continha path traversal (ex: etc/passwd) ou espaços
    nome_seguro = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', nome_seguro)
    return nome_seguro
