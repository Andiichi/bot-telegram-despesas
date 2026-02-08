from services.gemini_service import interpretar_despesa
from services.sheets_service import adicionar_linha
import time


# ==============================
# Memória temporária de despesas
# ==============================
DESPESAS_PENDENTES = {}


def aguardar_despesa(bot, message):
    """
    Inicia o fluxo de registro de despesa
    """
    msg = bot.send_message(
        message.chat.id,
        "💸 *Estou aguardando a despesa.*\n\n"
        "Digite a despesa em texto livre.\n\n"
        "*Exemplo:* "
        "_Pago conta da Claro hoje de valor 45 no PIX_",
        parse_mode="markdown"
    )

    bot.register_next_step_handler(msg, processar_despesa, bot)


def processar_despesa(message, bot):
    """
    Envia o texto para o Gemini e pede confirmação
    """
    chat_id = message.chat.id
    texto = message.text.strip()

    if texto.startswith('/'):
        if texto == '/voltar' or texto == '/cancelar':
            cancelar_despesa(bot, message)
            return
        else:
            bot.send_message(chat_id, "Voltando ao menu principal...Digite /start para ver as opções.")
            DESPESAS_PENDENTES.pop(chat_id, None)
            return 

    if not texto:
        bot.send_message(chat_id, "⚠️ Descrição vazia. Use /despesa novamente.")
        return

    try:
        # mostra "digitando..."
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1.5)  # sensação de processamento

        # 🔑 AQUI ESTÁ A CORREÇÃO
        despesa = interpretar_despesa(
            texto_usuario=texto,
            message_date=message.date
        )

        # Salva temporariamente
        DESPESAS_PENDENTES[chat_id] = despesa

        bot.send_message(
            chat_id,
            f"🧾 *Confirme a despesa:*\n\n"
            f"📝 *Descrição:* {despesa.get('descricao', '-')}\n"
            f"💰 *Valor:* R$ {despesa.get('valor', 0)}\n"
            f"📅 *Data:* {despesa.get('data_pagamento', '-')}\n"
            f"🗓️ *Mês:* {despesa.get('mes_pagamento', '-')}\n"
            f"🏷️ *Categoria:* {despesa.get('categoria', '-')}\n"
            f"💳 *Pagamento:* {despesa.get('meio_pagamento', '-')}\n\n"
            "👉 Digite */confirmar* para salvar ou */cancelar* para descartar.",
            parse_mode="markdown"
        )

    except Exception as e:
        print("Erro ao processar despesa:", e)
        bot.send_message(
            chat_id,
            "⚠️ Não consegui entender a despesa.\n"
            "Use /despesa e tente novamente."
        )


def confirmar_despesa(bot, message):
    chat_id = message.chat.id

    if chat_id not in DESPESAS_PENDENTES:
        bot.send_message(
            chat_id,
            "⚠️ Nenhuma despesa pendente para confirmar."
        )
        return

    despesa = DESPESAS_PENDENTES.pop(chat_id)

    adicionar_linha(despesa)

    bot.send_message(
        chat_id,
        "✅ *Despesa registrada com sucesso!* 💸\n\n"
        f"📝 *Descrição:* {despesa.get('descricao', '-')}\n"
        f"💰 *Valor:* R$ {despesa.get('valor', 0)}\n"
        f"📅 *Data:* {despesa.get('data_pagamento', '-')}\n"
        f"🗓️ *Mês:* {despesa.get('mes_pagamento', '-')}\n"
        f"🏷️ *Categoria:* {despesa.get('categoria', '-')}\n"
        f"💳 *Pagamento:* {despesa.get('meio_pagamento', '-')}\n\n"
        f"👉 Para listar despesas do mês, use /listar ou use /listar <mês>\n"
        f"👉 Lembrando que para registrar uma nova despesa use /despesa\n\n"
        f"💬 Agora você pode continuar falando com o bot abaixo.",

        parse_mode="markdown"
    )

    print("\n✅ Despesa registrada com sucesso! 💸\n")


def cancelar_despesa(bot, message):
    chat_id = message.chat.id

    if chat_id in DESPESAS_PENDENTES:
        DESPESAS_PENDENTES.pop(chat_id)

    bot.send_message(
        chat_id,
        "❌ *Despesa cancelada.*\n"
        "Use /despesa para registrar uma nova.\n"
        "Ou /start para ver opções do menu principal.",
        parse_mode="markdown"
    )
