import json
from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import pytz

load_dotenv()  # carrega o .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrado no .env")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"

# --- FUNÇÕES DE APOIO ---

def limpar_json(texto: str) -> str:
    return texto.replace("```json", "").replace("```", "").strip()

def formatar_data_telegram(timestamp: int) -> str:
    """
    Converte timestamp do Telegram (UTC) para DD/MM/AAAA no fuso do Brasil
    """
    dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    brasil = pytz.timezone("America/Sao_Paulo")
    dt_br = dt_utc.astimezone(brasil)
    return dt_br.strftime("%d/%m/%Y")

def interpretar_despesa(texto_usuario: str, message_date: int) -> dict:
    with open("prompts/despesa_prompt.txt", "r", encoding="utf-8") as f:
        prompt_base = f.read()

    data_mensagem = formatar_data_telegram(message_date)

    prompt_final = f"""
CONTEXTO FIXO:
DATA_DA_MENSAGEM: {data_mensagem}

DESPESA:
"{texto_usuario}"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt_base, prompt_final]
    )

    texto_resposta = limpar_json(response.text)

    try:
        return json.loads(texto_resposta)
    except json.JSONDecodeError as e:
        raise ValueError("Resposta da IA não é um JSON válido") from e

def responder_pergunta(texto_usuario: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=texto_usuario
    )
    return response.text.strip()

# --- HANDLER DO CHAT ---

def chatbot_livre(bot, memoria_despesas):
    @bot.message_handler(func=lambda m: True)
    def chat_livre(message):
        chat_id = message.chat.id

        # Se o ID estiver na memória passada, o chatbot livre ignora
        if chat_id in memoria_despesas:
            return

        resposta = responder_pergunta(message.text)
        bot.send_message(chat_id, resposta)
