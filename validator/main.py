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
    
    
@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}


@app.post("/validate")
def validate(transaction: Transaction):
    print(transaction.valor)
    return transaction.valor
    
