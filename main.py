import telebot
from handlers.despesa_handler import registrar_handlers_despesa
from services.gemini_service import chatbot_livre
from handlers.despesa_registrar_handler import DESPESAS_PENDENTES
import os
from dotenv import load_dotenv

load_dotenv()  # carrega o .env
TOKEN_BOT = os.getenv("TOKEN_BOT")

if not TOKEN_BOT:
    raise ValueError("TOKEN_BOT não encontrado no .env")


bot = telebot.TeleBot(TOKEN_BOT)

print("🤖 Bot ativo e aguardando mensagens...")


@bot.message_handler(commands=['start', 'help', 'ajuda'])
def enviar_ajuda(message):
    msg = bot.send_message(
        message.chat.id,
        """
🤖 *Olá! Eu sou a AndyBot, seu assistente virtual.*

Aqui estão os comandos que você pode usar:

📌 *Comandos de Registro de Despesa na Planilha:*
/despesa - Inicia o registro de uma nova despesa.
/listar - Mostra as últimas 10 despesas da planilha.
/extrato - Outro nome para listar(Opcional) 


💡 *Conversa Livre:*
Basta digitar qualquer mensagem para conversar comigo sobre suas finanças!
    """,
        parse_mode="markdown"
    )
  
# ... comandos despesa ...
registrar_handlers_despesa(bot)

# Aqui conectamos as pontas sem criar importação circular no Service
chatbot_livre(bot, DESPESAS_PENDENTES)

bot.infinity_polling()









# import telebot
# from telebot import types

# from config import TOKEN
# from handlers.despesa_handler


# bot = telebot.TeleBot(TOKEN)


# print("🤖 Bot ativo e aguardando mensagens...")


# @bot.message_handler(commands=['start'])
# def start_help(msg:telebot.types.Message):
#     bot.send_message(msg.chat.id, "Olá! 👋 \nEu sou o bot Andy 🤖 ")
    
# #     markup=types.InlineKeyboardMarkup()

# #     botao_sobre = types.InlineKeyboardButton("Sobre", callback_data="botao_sobre")
# #     botao_ajuda = types.InlineKeyboardButton("Ajuda", callback_data="botao_ajuda")

# #     markup.add(botao_sobre, botao_ajuda)
# #     bot.send_message(msg.chat.id, "\nComo posso ajudar você hoje?", reply_markup=markup)

# # @bot.callback_query_handler(func=lambda call: True)
# # def callback_query(call:types.CallbackQuery):
# #     match call.data:
# #         case "botao_sobre":
# #             bot.answer_callback_query(call.id, "Você clicou no botão Sobre!")
# #             bot.send_message(call.message.chat.id, "AndyBot é um bot desenvolvido para ajudar você com diversas tarefas. 🚀")
# #         case "botao_ajuda":
# #             bot.answer_callback_query(call.id, "Você clicou no botão Ajuda!")
# #             bot.send_message(call.message.chat.id, "Se precisar de ajuda, envie suas dúvidas ou perguntas aqui. Estou aqui para ajudar! 🆘")

# markup=types.KeyboardMarkup()

#     botao_sobre = types.InlineKeyboardButton("Sobre", callback_data="botao_sobre")
#     botao_ajuda = types.InlineKeyboardButton("Ajuda", callback_data="botao_ajuda")

#     markup.add(botao_sobre, botao_ajuda)
#     bot.send_message(msg.chat.id, "\nComo posso ajudar você hoje?", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call:types.CallbackQuery):
#     match call.data:
#         case "botao_sobre":
#             bot.answer_callback_query(call.id, "Você clicou no botão Sobre!")
#             bot.send_message(call.message.chat.id, "AndyBot é um bot desenvolvido para ajudar você com diversas tarefas. 🚀")
#         case "botao_ajuda":
#             bot.answer_callback_query(call.id, "Você clicou no botão Ajuda!")
#             bot.send_message(call.message.chat.id, "Se precisar de ajuda, envie suas dúvidas ou perguntas aqui. Estou aqui para ajudar! 🆘")


# bot.infinity_polling()
    