import requests
from fastapi import FastAPI, HTTPException, Query   
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

DB_API_URL = 'http://nonamecoin_db:5000'

app = FastAPI()

# Dicionario para guardar transações por minuto por remetente
transaction_counts = {}

class Transacao(BaseModel):
    id: int
    rem: int
    reb: int
    valor: int
    status: int
    datetime: str
    seletor_key: str  # Assumindo que essa é a chave unica do seletor

@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}

@app.post("/validate")
def validate(transaction: Transacao, tempo_recusa: Optional[int] = Query(60))  :
    # Checar se o rem tem credito o suficiente
    response = requests.get(f'{DB_API_URL}/cliente/{transaction.rem}')
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch sender details")
    sender_info = response.json()
    if sender_info['qtdMoedas'] < transaction.valor:
        transaction.status = 2  # Não aprovado (não tem credito)
        return transaction

    # Ver se o tempo da transação é válido
    current_time = requests.get('localhost:5000/hora')
    transaction_time = datetime.strptime(transaction.datetime, '%Y-%m-%d %H:%M:%S')
    if transaction_time > current_time or \
       transaction_time <= current_time - timedelta(minutes=1):
        transaction.status = 2  # Não aprovado (tempo inválido)
        return transaction

    # Ver o contador de transações por minuto do remetente
    if transaction.rem in transaction_counts:
        if len(transaction_counts[transaction.rem]) >= tempo_recusa:
            transaction.status = 2  # Não aprovado (excedeu a quantidade de transações)
            return transaction
    else:
        transaction_counts[transaction.rem] = []

    transaction_counts[transaction.rem].append(transaction_time)
    
    # Retorna a chave do seletor
    transaction.status = 1  # Aprovado
    return transaction
