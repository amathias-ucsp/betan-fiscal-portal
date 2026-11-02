import re
from flask import Flask, render_template, request, redirect, url_for, flash
from app.upload import ficheiro_valido, sanitizar_nome_ficheiro

app = Flask(__name__)
app.secret_key = 'chave-secreta-betan-academico'

# Simulação da base em memória para o MVP
DOCUMENTOS_MOCK = [
    {"id": 1, "cliente": "Mecânica Silva LTDA", "doc": "extrato_bancario_out2026.pdf", "categoria": "Extratos Bancários", "competencia": "10/2026", "status": "Recebido", "badge": "bx--tag--blue"},
    {"id": 2, "cliente": "Padaria Central ME", "doc": "nf_entrada_3049.pdf", "categoria": "Notas Fiscais de Entrada", "competencia": "10/2026", "status": "Em Análise", "badge": "bx--tag--cyan"},
    {"id": 3, "cliente": "Comércio Silva & Filhos", "doc": "folha_comprovantes.jpg", "categoria": "Folha de Pagamento", "competencia": "10/2026", "status": "Com Pendência", "badge": "bx--tag--red", "obs": "Comprovante ilegível ou sem autenticação bancária"}
]

PADRAO_COMPETENCIA = re.compile(r'^(0[1-9]|1[0-2])\/\d{4}$')

@app.route('/')
def portal_cliente():
    return render_template('portal_cliente.html', documentos=DOCUMENTOS_MOCK)

@app.route('/upload', methods=['POST'])
def upload_documento():
    competencia = request.form.get('competencia', '').strip()
    categoria = request.form.get('categoria')
    ficheiro = request.files.get('documento')

    # Validação estrita do padrão de competência (MM/AAAA)
    if not PADRAO_COMPETENCIA.match(competencia):
        flash("Formato de competência inválido. Utilize estritamente o formato MM/AAAA (Ex: 10/2026).", "error")
        return redirect(url_for('portal_cliente'))

    if ficheiro and ficheiro.filename:
        nome_seguro = sanitizar_nome_ficheiro(ficheiro.filename)
        # Verificação do arquivo simulando o tamanho
        DOCUMENTOS_MOCK.append({
            "id": len(DOCUMENTOS_MOCK) + 1,
            "cliente": "Mecânica Silva LTDA",
            "doc": nome_seguro,
            "categoria": categoria,
            "competencia": competencia,
            "status": "Recebido",
            "badge": "bx--tag--blue"
        })
        flash(f"Documento registrado com sucesso para a competência {competencia}.", "success")

    return redirect(url_for('portal_cliente'))

@app.route('/gestao')
def painel_gestao():
    termo_busca = request.args.get('q', '').lower()
    filtro_status = request.args.get('status', '')

    docs_filtrados = DOCUMENTOS_MOCK
    if termo_busca:
        docs_filtrados = [d for d in docs_filtrados if termo_busca in d['cliente'].lower() or termo_busca in d['doc'].lower()]
    if filtro_status:
        docs_filtrados = [d for d in docs_filtrados if d['status'] == filtro_status]

    return render_template('painel_gestao.html', documentos=docs_filtrados, busca=termo_busca, status_selecionado=filtro_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
