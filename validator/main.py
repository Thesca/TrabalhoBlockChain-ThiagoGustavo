import requests
from fastapi import FastAPI
from pydantic import BaseModel

DB_API_URL = 'http://nonamecoin_db:5000'

app = FastAPI()


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
    response = requests.get(f'{DB_API_URL}/cliente/{transaction.rem}')
    j = response.json()
    assert j['qtdMoedas'] >= transaction.valor
    
    return transaction.valor
    
