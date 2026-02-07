import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

load_dotenv()  # carrega o .env

GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")

if not GOOGLE_SHEETS_CREDENTIALS:
    raise ValueError("GOOGLE_SHEETS_CREDENTIALS não encontrado no .env")

if not SPREADSHEET_NAME:
    raise ValueError("SPREADSHEET_NAME não encontrado no .env")


SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    GOOGLE_SHEETS_CREDENTIALS,
    SCOPE
)

client = gspread.authorize(creds)
spreadsheet = client.open(SPREADSHEET_NAME)
sheet = spreadsheet.get_worksheet(0)


def adicionar_linha(despesa):
    """
    Ordem das colunas:
    Mês | Descrição | Categoria | Data do pagamento | Valor | Meio de pagamento
    """
    linha = [
        despesa.get("mes_pagamento").capitalize(),
        despesa.get("descricao").capitalize(),
        despesa.get("categoria").capitalize(),
        despesa.get("data_pagamento"),
        despesa.get("valor"),
        despesa.get("meio_pagamento").capitalize(),
    ]

    # aqui você usa gspread / API para inserir a linha
    # print("Inserindo no Sheets:", linha)

    sheet.append_row(linha, value_input_option="USER_ENTERED")

def ler_ultimas_despesas(quantidade=10):
    """
    Retorna as últimas 'quantidade' linhas da planilha.
    Supondo que a primeira linha seja o cabeçalho.
    """
    try:
        # Pega todos os registros como lista de dicionários
        registros = sheet.get_all_records()
        
        # Se estiver vazio, retorna lista vazia
        if not registros:
            return []

        # Retorna os últimos X registros (invertido para o mais recente aparecer primeiro)
        return registros[-quantidade:]
    except Exception as e:
        print(f"Erro ao ler planilha: {e}")
        return []