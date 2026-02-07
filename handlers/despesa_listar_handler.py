from services.sheets_service import ler_ultimas_despesas 
import unicodedata


MESES = {
    "janeiro": "Janeiro",
    "fevereiro": "Fevereiro",
    "marco": "Março",
    "abril": "Abril",
    "maio": "Maio",
    "junho": "Junho",
    "julho": "Julho",
    "agosto": "Agosto",
    "setembro": "Setembro",
    "outubro": "Outubro",
    "novembro": "Novembro",
    "dezembro": "Dezembro",
}


def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def converter_valor(valor):
    if isinstance(valor, (int, float)):
        return float(valor)

    if isinstance(valor, str):
        valor = (
            valor.replace("R$", "")
                 .replace(" ", "")
                 .replace(".", "")
                 .replace(",", ".")
        )
        try:
            return float(valor)
        except ValueError:
            return 0.0

    return 0.0


def listar_despesas(bot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🔍 Buscando despesas registradas...")

    try:
        despesas = ler_ultimas_despesas(quantidade=50)

        if not despesas:
            bot.send_message(chat_id, "📭 Nenhuma despesa encontrada.")
            return

        # 🔎 Extrai o mês do comando: /listar janeiro
        partes = message.text.split(maxsplit=1)
        mes_filtro = None

        if len(partes) > 1:
            mes_digitado = normalizar(partes[1])
            mes_filtro = MESES.get(mes_digitado)

        # Se não informou mês, usa o mês da despesa mais recente
        if not mes_filtro:
            mes_filtro = (
                despesas[0].get("Mês")
                or despesas[0].get("mes_pagamento")
            )

        despesas_filtradas = [
            d for d in despesas
            if (d.get("Mês") or d.get("mes_pagamento")) == mes_filtro
        ]

        if not despesas_filtradas:
            bot.send_message(
                chat_id,
                f"📭 Nenhuma despesa encontrada para *{mes_filtro}*.",
                parse_mode="markdown"
            )
            return

        resposta = (
            f"📊 *Despesas registradas — {mes_filtro}*\n"
            f"────────────────────\n\n"
        )

        total_mes = 0.0

        for d in despesas_filtradas:
            data = d.get("Data do pagamento") or d.get("data_pagamento") or "-"
            descricao = d.get("Descrição") or d.get("descricao") or "Sem descrição"
            categoria = d.get("Categoria") or d.get("categoria") or "-"
            valor_raw = d.get("Valor") or d.get("valor") or 0
            meio = d.get("Meio de pagamento") or d.get("meio_pagamento") or "-"

            valor = converter_valor(valor_raw)
            total_mes += valor

            resposta += (
                f"📅 `{data}`  •  💳 *{meio.capitalize()}*\n"
                f"📝 *{descricao}*\n"
                f"🏷️ {categoria}   |   💰 *R$ {valor:.2f}*\n"
                f"────────────────────\n"
            )

        resposta += (
            f"\n💰 *Total de {mes_filtro}:* "
            f"*R$ {total_mes:.2f}*\n"
        )

        bot.send_message(chat_id, resposta, parse_mode="markdown")
        bot.send_message(
            chat_id,
            f"Pode inserir novas despesas usando o comando `/despesa`.\n"
            f"📌 Use `/listar <mês>` para filtrar por mês específico. Ex: `/listar fevereiro`"
        )
    except Exception as e:
        print(f"Erro ao listar despesas: {e}")
        bot.send_message(
            chat_id,
            "⚠️ Ocorreu um erro ao buscar as despesas. Tente novamente."
        )
