from app.auth import criar_hash_senha, verificar_senha
from app.upload import ficheiro_valido

def test_hash_senha_pbkdf2():
    hash_gerado = criar_hash_senha("SenhaForte123")
    assert hash_gerado != "SenhaForte123"
    assert verificar_senha(hash_gerado, "SenhaForte123") is True
    assert verificar_senha(hash_gerado, "SenhaErrada") is False

def test_validacao_upload_extensoes():
    assert ficheiro_valido("recibo.pdf", 1024) is True
    assert ficheiro_valido("script_malicioso.exe", 1024) is False
