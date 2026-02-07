# 1. Renomeamos a função importada usando 'as' para evitar o conflito de nomes
from services.gemini_service import responder_pergunta as gemini_api_call

def responder_pergunta(texto):
    prompt = f"""
Você é Alec, um assistente pessoal da Andrezza. Você está aqui para ajudar a responder perguntas gerais e fornecer informações úteis.
Está atualmente no chat privado telegram como bot.

Responda de forma clara, curta e prática.
Não registre despesas.
Não gere JSON.
Não invente dados financeiros.

Pergunta do usuário:
{texto}
"""
    try:
        # 2. Chamamos a função com o apelido, não a função local
        response = gemini_api_call(prompt)
        return response.strip()
    except Exception as e:
        # Tratamento básico para evitar que o bot caia se a API der erro 503 de novo
        return "Desculpe, estou com dificuldade para conectar ao meu cérebro agora. Tente novamente em alguns segundos."