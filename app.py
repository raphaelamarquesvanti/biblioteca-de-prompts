import os
import sqlite3
from pathlib import Path
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf.csrf import CSRFProtect

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

csrf = CSRFProtect(app)

def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar_login(*args, **kwargs):
        if not session.get("autenticada"):
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return verificar_login

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_BANCO = BASE_DIR / "biblioteca.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            conteudo TEXT NOT NULL
        )
    """)

    
    if conexao.execute("SELECT COUNT(*) FROM prompts").fetchone()[0] == 0:
        conexao.executemany(
            """
            INSERT INTO prompts (titulo, categoria, descricao, conteudo)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    p["titulo"],
                    p["categoria"],
                    p["descricao"],
                    p["conteudo"],
                )
                for p in PROMPTS
            ],
        )

    conexao.commit()
    conexao.close()



PROMPTS = [
    {
        "id": 1,
        "titulo": "Ideias para Instagram",
        "categoria": "Marketing",
        "descricao": "Crie ideias de conteúdo para redes sociais.",
        "conteudo": (
            "Atue como especialista em marketing digital. "
            "Crie 5 ideias de publicações para o Instagram "
            "de uma empresa do segmento [informe o segmento], "
            "com foco em atrair clientes e gerar engajamento."
        ),
    },
    {
        "id": 2,
        "titulo": "Organizador de estudos",
        "categoria": "Estudos",
        "descricao": "Organize uma rotina de estudos.",
        "conteudo": (
            "Atue como orientador de estudos. Monte um plano "
            "semanal para estudar [disciplina], considerando "
            "[horas disponíveis] por dia e uma prova em [data]."
        ),
    },
    {
        "id": 3,
        "titulo": "Planejamento de tarefas",
        "categoria": "Produtividade",
        "descricao": "Organize tarefas e prioridades.",
        "conteudo": (
            "Atue como especialista em produtividade. "
            "Organize estas tarefas por prioridade, prazo "
            "e importância: [liste suas tarefas]."
        ),
    },
    {
        "id": 4,
        "titulo": "Currículo profissional",
        "categoria": "Carreira",
        "descricao": "Melhore sua apresentação profissional.",
        "conteudo": (
            "Atue como especialista em recrutamento. "
            "Ajude a melhorar meu currículo para a vaga "
            "[nome da vaga], considerando minhas experiências: "
            "[descreva suas experiências]."
        ),
    },
]



@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        senha = request.form.get("senha", "")

        if senha and senha == os.getenv("ADMIN_PASSWORD"):
            session["autenticada"] = True
            return redirect(url_for("admin"))

        erro = "Senha incorreta. Tente novamente."

    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin")
@login_obrigatorio
def admin():
    return render_template("admin.html")


@app.route("/admin/cadastrar", methods=["POST"])
@login_obrigatorio
def cadastrar_prompt():
    titulo = request.form.get("titulo", "").strip()
    categoria = request.form.get("categoria", "").strip()
    descricao = request.form.get("descricao", "").strip()
    conteudo = request.form.get("conteudo", "").strip()

    if not titulo or not categoria or not descricao or not conteudo:
        return "Todos os campos são obrigatórios.", 400

    conexao = conectar_banco()
    conexao.execute(
        """
        INSERT INTO prompts (titulo, categoria, descricao, conteudo)
        VALUES (?, ?, ?, ?)
        """,
        (titulo, categoria, descricao, conteudo),
    )
    conexao.commit()
    conexao.close()

    return """
    <h1>Prompt cadastrado com sucesso!</h1>
    <p>O novo prompt foi salvo na biblioteca.</p>
    <a href="/admin">Cadastrar outro prompt</a>
    <br>
    <a href="/">Voltar para a biblioteca</a>
    """


@app.route("/")
def inicio():
    busca = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()

    conexao = conectar_banco()
    resultados = [dict(p) for p in conexao.execute("SELECT * FROM prompts").fetchall()]
    conexao.close()

    if busca:
        termo = busca.casefold()
        resultados = [
            p for p in resultados
            if termo in p["titulo"].casefold()
            or termo in p["descricao"].casefold()
            or termo in p["conteudo"].casefold()
            or termo in p["categoria"].casefold()
        ]

    if categoria:
        resultados = [
            p for p in resultados
            if p["categoria"] == categoria
        ]

    conexao = conectar_banco()
    categorias = [
        linha["categoria"]
        for linha in conexao.execute(
            "SELECT DISTINCT categoria FROM prompts ORDER BY categoria"
        ).fetchall()
    ]
    conexao.close()

    return render_template(
        "index.html",
        prompts=resultados,
        categorias=categorias,
        busca=busca,
        categoria_selecionada=categoria,
    )


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)