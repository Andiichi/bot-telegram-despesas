# 🤖 Bot Telegram com Gemini AI

Este projeto é um **bot do Telegram em Python** integrado à **API Gemini (Google AI)** para interpretar mensagens de inserção de despesas cotidiana e responder de forma inteligente.

---

## 🚀 Funcionalidades

* Integração com o Telegram Bot API
* Respostas inteligentes usando **Gemini AI** livre
* Adição de despesas por texto livre
* Listagem geral ou por mês especifico 

---

## 🛠️ Tecnologias utilizadas

* **Python 3.10+**
* **Telegram Bot API**
* **Google Gemini API**
* **API Google Sheets**
* `python-dotenv`
* Ambiente virtual `venv`

---

## 🧪 Ambiente virtual (venv)

### Criar a venv

```bash
python -m venv venv
```

### Ativar a venv

**Linux / Mac / WSL**

```bash
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate
```

---

## 📦 Instalação das dependências

Com a venv ativa:

```bash
pip install -r requirements.txt
```

---

## ▶️ Executar o bot

Com a venv ativa e o `.env` configurado:

```bash
python main.py
```

Se tudo estiver correto, você verá algo como:

```
🤖 Bot ativo e aguardando mensagens...
```

---

## ☁️ Deploy (opcional)

O bot pode ser hospedado em plataformas como:

* Render
* Railway
* VPS (Ubuntu)
* PythonAnywhere

Em produção, configure as **variáveis de ambiente direto na plataforma** (não use `.env`).

*OBS: Projeto feito deploy no Render*


---

## ⚠️ Boas práticas

* Nunca suba tokens ou chaves no GitHub
* Sempre use `.env` para dados sensíveis
* Mantenha o `requirements.txt` atualizado
* Ignore `venv/` e `.env` no `.gitignore`

---

## 🧠 Próximos passos (sugestões)

* Adicionar histórico de conversas
* Fazer a inclusão por transcrição de audios
* Controle de usuários
* Limite de requisições
* Possibilidade de realizar exclusão de despesa inserida no mês

---

✨ Projeto simples, seguro e pronto para evoluir.
