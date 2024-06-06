from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Transaction(BaseModel):
    id : int
    rem : int
    reb : int
    valor: int
    status : int
    datetime: str
    #Flags do seletor
    #Receber da request de validacao
    
    
@app.get("/validate")
def validate(transaction: Transaction):
    print(transaction.stake)