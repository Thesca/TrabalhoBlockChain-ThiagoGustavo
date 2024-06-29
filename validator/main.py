import requests
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

DB_API_URL = 'http://nonamecoin_db:5000'

app = FastAPI()

# Dicionario para guardar transações por minuto por remetente
TRANSACTION_COUNTS = {}
COUNTER_LIMIT = 100

class Transacao(BaseModel):
    id : int
    rem : int
    reb : int
    valor: int
    status : int
    datetime: str
    #Flags do seletor
    #Receber da request de validacao
    
    
@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}


@app.post("/validate")
def validate(transaction: Transacao):
    # Checar se o rem tem credito o suficiente
    response = requests.get(f'{DB_API_URL}/cliente/{transaction.rem}')
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch sender details")
    sender_info = response.json()
    if sender_info['qtdMoedas'] < transaction.valor:
        transaction.status = 2  # Não aprovado (não tem credito)
        return transaction

    # Ver se o tempo da transação é válido
    current_time = requests.get(f'{DB_API_URL}/hora').json()
    current_time = datetime.strptime(transaction.datetime, '%a, %d %b %Y %H:%M:%S %Z')
    transaction_time = datetime.strptime(transaction.datetime, '%a, %d %b %Y %H:%M:%S %Z')
    if transaction_time > current_time or \
       transaction_time <= current_time - timedelta(minutes=1):
        transaction.status = 2  # Não aprovado (tempo inválido)
        return transaction

    # Ver o contador de transações por minuto do remetente
    transactions_count = requests.get(f'{DB_API_URL}/transacoes/{transaction.rem}')
    
    if transaction.rem in TRANSACTION_COUNTS:
        if len(TRANSACTION_COUNTS[transaction.rem]) >= COUNTER_LIMIT:
            transaction.status = 2  # Não aprovado (excedeu a quantidade de transações)
            return transaction
    else:
        TRANSACTION_COUNTS[transaction.rem] = []

    TRANSACTION_COUNTS[transaction.rem].append(transaction_time)
    
    # Retorna a chave do seletor
    transaction.status = 1  # Aprovado
    return transaction
    
