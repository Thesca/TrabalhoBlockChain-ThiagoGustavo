import requests
from fastapi import FastAPI, HTTPException, Query   
from fastapi import FastAPI, HTTPException, Query   
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from datetime import datetime, timedelta
from typing import Optional

DB_API_URL = 'http://nonamecoin_db:5000'
TRANSACTIONS_LIMIT = 60
TRANSACTIONS_LIMIT = 60

app = FastAPI()

# Dicionario para guardar transações por minuto por remetente
transaction_counts = {}
transaction_counts = {}

class Transacao(BaseModel):
    id: int
    remetente: int
    recebedor: int
    valor: int
    horario: str
    #Flags do seletor
    #Receber da request de validacao
    
    
@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}

@app.post("/validate")
def validate(transaction: Transacao):
    status = 0
    # Checar se o rem tem credito o suficiente
    response = requests.get(f'{DB_API_URL}/cliente/{transaction.remetente}')
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch sender details")
    
    sender_info = response.json()
    if sender_info is None:
        raise HTTPException(status_code=400, detail="Sender not registered as client")
    
    if sender_info['qtdMoedas'] < transaction.valor:
        status = 2  # Não aprovado (não tem credito)
        return transaction

    # Ver se o tempo da transação é válido
    current_time = requests.get(f'{DB_API_URL}/hora').json()
    current_time = datetime.strptime(transaction.horario, '%a, %d %b %Y %H:%M:%S %Z')
    transaction_time = datetime.strptime(transaction.horario, '%a, %d %b %Y %H:%M:%S %Z')
    if transaction_time > current_time or \
       transaction_time <= current_time - timedelta(minutes=1):
        status = 2  # Não aprovado (tempo inválido)
        return transaction

    # Ver o contador de transações por minuto do remetente
    transactions = requests.get(f'{DB_API_URL}/transacoes/{transaction.remetente}').json()
    
    if transactions:
        if len(transactions) >= TRANSACTIONS_LIMIT:
                status = 2  # Não aprovado (excedeu a quantidade de transações)
                return transaction

    # Retorna a chave do seletor
    status = 1  # Aprovado
    return status
    
