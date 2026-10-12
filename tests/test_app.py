import app

def test_pagina_inicial():
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False
    cliente = app.app.test_client()
    resposta = cliente.get("/")
    assert resposta.status_code == 200

def test_login_abre():
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False
    cliente = app.app.test_client()
    resposta = cliente.get("/login")
    assert resposta.status_code == 200

def test_admin_exige_login():
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False
    cliente = app.app.test_client()
    resposta = cliente.get("/admin")
    assert resposta.status_code == 302

def test_login_com_senha_incorreta():
    import os
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False
    os.environ["ADMIN_PASSWORD"] = "senha_correta_teste"
    cliente = app.app.test_client()
    resposta = cliente.post("/login", data={"senha": "senha_errada"})
    assert resposta.status_code == 200
    assert b"Senha incorreta" in resposta.data

def test_logout_redireciona():
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False
    cliente = app.app.test_client()
    resposta = cliente.get("/logout")
    assert resposta.status_code == 302

def test_admin_cadastro_bloqueado_sem_login():
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False
    cliente = app.app.test_client()
    resposta = cliente.post("/admin/cadastrar", data={
        "titulo": "Teste",
        "categoria": "Estudos",
        "descricao": "Teste de cadastro",
        "conteudo": "Conteúdo de teste"
    })
    assert resposta.status_code == 302

def test_login_com_senha_correta():
    import os
    os.environ["ADMIN_PASSWORD"] = "senha_teste_123"
    cliente = app.app.test_client()
    resposta = cliente.post("/login", data={"senha": "senha_teste_123"})
    assert resposta.status_code == 302
    assert "/admin" in resposta.location

def test_pagina_inicial_com_pesquisa():
    cliente = app.app.test_client()
    resposta = cliente.get("/?q=Instagram")
    assert resposta.status_code == 200
    assert b"Ideias para Instagram" in resposta.data

def test_pagina_inicial_com_categoria():
    cliente = app.app.test_client()
    resposta = cliente.get("/?categoria=Estudos")
    assert resposta.status_code == 200
    assert b"Organizador de estudos" in resposta.data

def test_cadastro_sem_login_nao_cadastra():
    cliente = app.app.test_client()
    resposta = cliente.post("/admin/cadastrar", data={
        "titulo": "Teste adicional",
        "categoria": "Estudos",
        "descricao": "Teste",
        "conteudo": "Conteudo"
    })
    assert resposta.status_code == 302

def test_login_com_senha_vazia():
    cliente = app.app.test_client()
    resposta = cliente.post("/login", data={"senha": ""})
    assert resposta.status_code == 200
    assert b"Senha incorreta" in resposta.data

def test_pesquisa_sem_resultados():
    cliente = app.app.test_client()
    resposta = cliente.get("/?q=xyznaoexiste999")
    assert resposta.status_code == 200

def test_cadastro_com_login():
    import os
    os.environ["ADMIN_PASSWORD"] = "senha_teste_123"
    cliente = app.app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["autenticada"] = True

    resposta = cliente.post("/admin/cadastrar", data={
        "titulo": "Prompt de teste automatizado",
        "categoria": "Testes",
        "descricao": "Descricao de teste",
        "conteudo": "Conteudo de teste"
    })

    assert resposta.status_code == 200
    assert b"cadastrado com sucesso" in resposta.data

def test_cadastro_com_campos_vazios():
    cliente = app.app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["autenticada"] = True

    resposta = cliente.post("/admin/cadastrar", data={
        "titulo": "",
        "categoria": "",
        "descricao": "",
        "conteudo": ""
    })

    assert resposta.status_code == 400
    assert b"Todos os campos s\xc3\xa3o obrigat\xc3\xb3rios" in resposta.data

def test_criar_banco_completo(tmp_path, monkeypatch):
    import sqlite3

    banco_teste = tmp_path / "teste.db"
    monkeypatch.setattr(app, "CAMINHO_BANCO", banco_teste)

    app.criar_banco()

    conexao = sqlite3.connect(banco_teste)
    quantidade = conexao.execute(
        "SELECT COUNT(*) FROM prompts"
    ).fetchone()[0]
    conexao.close()

    assert quantidade == len(app.PROMPTS)

def test_admin_com_login():
    cliente = app.app.test_client()

    with cliente.session_transaction() as sessao:
        sessao["autenticada"] = True

    resposta = cliente.get("/admin")
    assert resposta.status_code == 200
