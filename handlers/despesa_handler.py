from handlers.despesa_registrar_handler import (
    aguardar_despesa,
    confirmar_despesa,
    cancelar_despesa
)
from handlers.despesa_listar_handler import listar_despesas

def registrar_handlers_despesa(bot):

    @bot.message_handler(commands=['despesa'])
    def cmd_registrar_despesa(message):
        aguardar_despesa(bot, message)

    @bot.message_handler(commands=['confirmar'])
    def cmd_confirmar(message):
        confirmar_despesa(bot, message)

    @bot.message_handler(commands=['cancelar'])
    def cmd_cancelar(message):
        cancelar_despesa(bot, message)

    @bot.message_handler(commands=['listar', 'extrato'])
    def cmd_listar(message):
        listar_despesas(bot, message)
