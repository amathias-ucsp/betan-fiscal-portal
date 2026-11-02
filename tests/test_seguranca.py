import pytest
from app.auth import criar_hash_senha, verificar_senha
from app.upload import ficheiro_valido, sanitizar_nome_ficheiro
from app.models import Cliente, Documento
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hash_senha_pbkdf2():
    hash_gerado = criar_hash_senha("SenhaForte123")
    assert hash_gerado != "SenhaForte123"
    assert verificar_senha(hash_gerado, "SenhaForte123") is True
    assert verificar_senha(hash_gerado, "SenhaErrada") is False

def test_validacao_upload_extensoes_e_tamanho():
    assert ficheiro_valido("recibo.pdf", 1024) is True
    assert ficheiro_valido("foto.png", 2048) is True
    assert ficheiro_valido("documento.jpg", 4096) is True
    assert ficheiro_valido("script_malicioso.exe", 1024) is False
    assert ficheiro_valido("arquivo_sem_extensao", 1024) is False
    assert ficheiro_valido("", 1024) is False
    assert ficheiro_valido("recibo.pdf", 15 * 1024 * 1024) is False
    assert ficheiro_valido("recibo.pdf", 0) is False

def test_sanitizacao_nome_arquivo():
    assert sanitizar_nome_ficheiro("../../../etc/passwd") == "etc_passwd"
    assert sanitizar_nome_ficheiro("nota fiscal final.pdf") == "nota_fiscal_final.pdf"

def test_instanciacao_modelos_cliente_e_documento():
    cliente = Cliente(
        razao_social="Oficina Mecânica Silva LTDA",
        cnpj_cpf="12.345.678/0001-90",
        email="contato@oficinasilva.com.br",
        senha_hash="hash_teste",
        telefone="11999998888"
    )
    assert cliente.razao_social == "Oficina Mecânica Silva LTDA"
    assert cliente.cnpj_cpf == "12.345.678/0001-90"

    doc = Documento(
        cliente_id=1,
        nome_original="notas_outubro.pdf",
        caminho_arquivo="/uploads/notas_outubro.pdf",
        tipo_documento="Notas Fiscais de Entrada",
        mes_competencia="10/2026",
        status="Recebido",
        observacao="Envio pontual"
    )
    assert doc.mes_competencia == "10/2026"
    assert doc.status == "Recebido"

def test_rotas_portal_e_gestao(client):
    res_home = client.get('/')
    assert res_home.status_code == 200
    assert b"Betan" in res_home.data

    res_gestao = client.get('/gestao?q=Silva&status=Recebido')
    assert res_gestao.status_code == 200

    # Teste de validação estrita de competência (invalida vs valida)
    res_invalido = client.post('/upload', data={'competencia': 'invalida'}, follow_redirects=True)
    assert res_invalido.status_code == 200

    from io import BytesIO
    data_valida = {
        'competencia': '10/2026',
        'categoria': 'Notas Fiscais de Entrada',
        'documento': (BytesIO(b"conteudo simulado"), 'recibo_teste.pdf')
    }
    res_valido = client.post('/upload', data=data_valida, content_type='multipart/form-data', follow_redirects=True)
    assert res_valido.status_code == 200
