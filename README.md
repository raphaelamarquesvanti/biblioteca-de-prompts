# 📚 Biblioteca de Prompts

Uma aplicação web para pesquisar, consultar e copiar prompts de inteligência artificial, organizados por categorias. O projeto também possui uma área administrativa para cadastrar novos prompts.

O objetivo é facilitar o acesso a prompts úteis, especialmente para estudantes, criadores de conteúdo e pessoas que estão começando a utilizar ferramentas de inteligência artificial.

---

## 🖥️ Demonstração da aplicação

### Tela principal — Biblioteca de Prompts

![Tela do site de prompt](Tela%20do%20site%20de%20prompt.png)

### Filtro por categoria — Marketing

![Filtro de Marketing](Filto%20Marketing.png)



## ✨ Funcionalidades

- **Pesquisa de prompts:** encontre prompts por meio de uma busca.
- **Filtro por categoria:** organize e localize prompts por assunto.
- **Visualização:** consulte o conteúdo dos prompts disponíveis.
- **Cópia de prompts:** facilite o uso do conteúdo em outras ferramentas.
- **Área administrativa:** acesse uma área restrita para cadastrar prompts.
- **Autenticação:** proteja a administração por meio de login.
- **Banco de dados local:** armazene os prompts utilizando SQLite.

## 🛠️ Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- Flask-WTF, para proteção contra requisições CSRF
- python-dotenv, para carregar configurações de variáveis de ambiente
- Git e GitHub, para versionamento do código

## 📋 Pré-requisitos

Antes de começar, instale:

1. **Python:** https://www.python.org/downloads/
2. **Git:** https://git-scm.com/downloads
3. Um editor de código, como o Visual Studio Code ou PyCharm.

No Windows, durante a instalação do Python, marque a opção de adicionar o Python ao PATH, se ela estiver disponível.

Para conferir se o Python e o Git estão instalados, execute no terminal:

```bash
python --version
git --version
```

Se o comando `python` não funcionar no Windows, tente `py --version`.

## 🚀 Como instalar e executar

### 1. Baixe o projeto

Abra o terminal e execute:

```bash
git clone https://github.com/raphaelamarquesvanti/biblioteca-de-prompts.git
```

Entre na pasta do projeto:

```bash
cd biblioteca-de-prompts
```

### 2. Crie um ambiente virtual

O ambiente virtual mantém as dependências do projeto separadas de outros projetos Python.

**Windows — PowerShell:**

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, você pode abrir o terminal CMD e executar:

```cmd
.venv\Scripts\activate.bat
```

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quando o ambiente estiver ativo, normalmente aparecerá `(.venv)` no início da linha do terminal.

### 3. Instale as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install Flask Flask-WTF python-dotenv
```

### 4. Configure as variáveis de ambiente

Na pasta principal do projeto, crie um arquivo chamado `.env`.

Adicione o seguinte conteúdo:

```dotenv
SECRET_KEY=coloque_uma_chave_secreta_aqui
ADMIN_PASSWORD=defina_uma_senha_para_administracao
```

Substitua os valores de exemplo por uma chave secreta aleatória e uma senha administrativa própria.

**Importante:** não compartilhe sua senha nem envie o arquivo `.env` para o GitHub. O arquivo está listado no `.gitignore` para evitar o versionamento acidental dessas configurações.

### 5. Execute a aplicação

Com as dependências instaladas e o arquivo `.env` configurado, execute:

```bash
python app.py
```

O terminal deverá informar o endereço local da aplicação. Abra esse endereço no navegador — normalmente:

http://127.0.0.1:5000

Mantenha o terminal aberto enquanto estiver utilizando a aplicação. Para interromper a execução, pressione `Ctrl + C`.

## 🔐 Acesso administrativo

A área administrativa permite cadastrar novos prompts.

1. Abra a aplicação no navegador.
2. Acesse `/login` no endereço local, por exemplo: `http://127.0.0.1:5000/login`.
3. Informe a senha definida em `ADMIN_PASSWORD` no arquivo `.env`.
4. Após a autenticação, acesse a área administrativa para cadastrar prompts.

Não publique suas credenciais. Esta versão é um MVP acadêmico e deve passar por uma revisão adicional de segurança antes de ser disponibilizada publicamente.

## 🗂️ Estrutura do projeto

```text
biblioteca-de-prompts/
├── static/
│   └── style.css
├── templates/
│   ├── admin.html
│   ├── index.html
│   └── login.html
├── app.py
├── .env
├── .gitignore
├── biblioteca.db
└── README.md
```

- `app.py`: aplicação Flask e rotas.
- `templates/`: páginas HTML.
- `static/style.css`: estilos da interface.
- `.env`: configurações e credenciais locais.
- `biblioteca.db`: banco de dados SQLite criado ou utilizado pela aplicação.
- `.gitignore`: arquivos e pastas que não devem ser enviados ao GitHub.
- `README.md`: documentação do projeto.

O arquivo `.env`, o ambiente virtual `.venv` e o banco de dados local não devem ser compartilhados como parte do repositório público. A estrutura acima representa os arquivos utilizados localmente; alguns deles são criados ou configurados durante a instalação.

## 🧰 Solução de problemas

**Erro ao executar `python`:**

Verifique se o Python está instalado. No Windows, tente `py --version` e use `py` no lugar de `python` nos comandos de instalação, se necessário.

**Erro de módulo não encontrado:**

Confirme se o ambiente virtual está ativado e execute novamente:

```bash
python -m pip install Flask Flask-WTF python-dotenv
```

**Erro relacionado à `SECRET_KEY`:**

Confira se o arquivo `.env` existe na pasta principal do projeto e se contém as variáveis exigidas pela aplicação.

**A senha administrativa não funciona:**

Confira o valor de `ADMIN_PASSWORD` no arquivo `.env` e reinicie a aplicação depois de alterar as configurações.

**A aplicação não abre no navegador:**

Verifique se `python app.py` continua em execução e se o endereço informado no terminal está correto.

## 🤝 Contribuições

Contribuições são bem-vindas!

1. Faça um fork do repositório.
2. Crie uma branch para sua alteração.
3. Implemente e teste a mudança.
4. Registre suas alterações com commits claros.
5. Abra um Pull Request explicando o que foi modificado.

Exemplos de mensagens de commit:

```text
feat: adiciona nova funcionalidade
fix: corrige erro na pesquisa
docs: atualiza documentação
test: adiciona testes automatizados
```

## 📌 Status do projeto

Projeto acadêmico em desenvolvimento, com foco na implementação de um MVP de biblioteca de prompts.

## 📄 Licença

Nenhuma licença foi definida neste momento. Consulte o responsável pelo repositório antes de reutilizar ou redistribuir o código.
