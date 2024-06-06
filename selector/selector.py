from fastapi import FastAPI
from pydantic import BaseModel
import requests

DB_API_URL = ''

app = FastAPI()


class Transaction(BaseModel):
    id: int
    remetente: int
    recebedor: int
    valor: int
    status: int
    

def select_validators():
    validators = requests.get()
    validators =

@app.get("/transacao")
def validate(transaction: Transaction):
    