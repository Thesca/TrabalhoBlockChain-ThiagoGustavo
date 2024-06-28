import os
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import subprocess
import random

DB_API_URL = 'http://nonamecoin_db:5000'

app = FastAPI()


class Transaction(BaseModel):
    id: int
    remetente: int
    recebedor: int
    valor: int
    status: int
    

def select_validators():
    # validators = requests.get(os.path.join(DB_API_URL, '/validador'))
    # command = ['docker', 'build', './validator', '-t', 'nnc_validator']
    # result = subprocess.run(command, shell=True)
    
    ips = ['validator-1', 'validator-2', 'validator-3', 'validator-4',
             'validator-5', 'validator-6']
    ips = random.choices(ips, k=3)  
    for ip in ips:
        datetime = requests.get(f'{DB_API_URL}/hora')
        data = {'id': 0,'rem': 1,'reb': 2,'valor': 100,'status': 0,'datetime': 'night'}
        response = requests.post(f'http://{ip}:8000/validate', json=data)
        print(response.json())
    
    
@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}


@app.get("/transacao")
def validate():
    select_validators()