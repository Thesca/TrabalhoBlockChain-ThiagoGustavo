import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import random
from datetime import datetime, timedelta
from typing import List

DB_API_URL = 'http://nonamecoin_db:5000'

app = FastAPI()

ip_map = {
    '127.0.1.1': 'validator-1',
    '127.0.1.2': 'validator-2',
    '127.0.1.3': 'validator-3',
    '127.0.1.4': 'validator-4',
    '127.0.1.5': 'validator-5',
    '127.0.1.6': 'validator-6',
}

class Transacao(BaseModel):
    id: int
    remetente: int
    recebedor: int
    valor: int
    horario: str


def select_validators() -> List[str]:
    selected_validators = []
    selected_client_ids = []
    validator_choices = []

    response = requests.get(f'{DB_API_URL}/validador')
    validators = response.json()
    
    total_stake = sum([validator['peso'] for validator in validators])
    
    # Calculate weights based on validator coins and flags
    for validator in validators:
        weight = validator['peso'] / total_stake  # Default weight
        if validator['flags'] == 1:
            weight *= 0.5  # 50% reduction for Flag=1
        elif validator['flags'] == 2:
            weight *= 0.25  # 75% reduction for Flag=2
            
        if weight > 0.2:
            weight = 0.2

        cliente = requests.get(f'{DB_API_URL}/cliente/{validator["cliente_id"]}').json()
        service_ip = ip_map[cliente['ip']]
        validator_choices.append((service_ip, weight, cliente['id']))
    
    # Sort validators by weight (descending) and select up to 3
    selections = 3 if len(validators) > 3 else len(validators)
    for _ in range(selections):
        weights = [x[1] for x in validator_choices] 
        validator = random.choices(validator_choices, weights=weights, k=1)[0]
        selected_validators.append(validator[0])
        selected_client_ids.append(validator[2])
        validator_choices.remove(validator)

    return selected_validators, selected_client_ids

def check_consensus(selected_validators: List[str], transaction: Transacao) -> bool:
    approved_count = 0
    for ip in selected_validators:
        # Assuming each validator responds with status 1 or 2 (approved or not approved)
        data = transaction.model_dump()
        response = requests.post(f'http://{ip}:8000/validate', json=data)
        status = response.json()
        if status == 1:
            approved_count += 1
        else:
            print(response.json())
    
    return approved_count > len(selected_validators) / 2

# def update_validator_flags(ip: str, is_inconsistent: bool):
#     if is_inconsistent:
#         validators[ip]['flags'] += 1
#         if validators[ip]['flags'] > 2:
#             # Remove validator from network (simulated by resetting coins)
#             validators[ip]['coins'] = 0

@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}

@app.post("/transacao")
def process_transaction(transaction: Transacao):
    try:
        selected_validators, selected_client_ids = select_validators()
    except Exception as e:
        data={
            "message": "Failed to select validators, " + str(e)
        }
        return json.dumps(data)
    
    try:        
        # Check if minimum validators are available
        if len(selected_validators) < 3:
            raise HTTPException(status_code=503, detail="Not enough validators available. Transaction pending.")
    
        # Perform transaction validation with selected validators
        if check_consensus(selected_validators, transaction):
            print('CONSENSUSSS')
            # Successful transaction logic
            # Assuming 1.0% reward for selector and 0.5% held for validator
            # Update balances, handle flags, etc.
            client_reward = int(transaction.valor * 0.005)  # 0.5% for validator
            selector_reward = int(transaction.valor * 0.010)  # 1.0% for selector
            
            selected_clients = []
            for id in selected_client_ids:
                # Successful validation logic
                selector_client = requests.get(f'{DB_API_URL}/cliente/{id}').json()
                client_coins = selector_client['qtdMoedas'] + client_reward
                selected_client = requests.put(f'{DB_API_URL}/cliente/{id}/{client_coins}').json()
                selected_clients.append(selected_client)
            
            print('\nSELECTED', selected_clients)
            print('\nREWARDS', client_reward, selector_reward)
            # Update selector's balance, assuming 1.0% reward
            selector = requests.get(f'{DB_API_URL}/seletor/1').json()
            selector_client = requests.get(f'{DB_API_URL}/cliente/{selector["cliente_id"]}').json()
            selector_coins = selected_client['qtdMoedas'] + selector_reward
            selector_client = requests.put(f'{DB_API_URL}/cliente/{selector["cliente_id"]}/{selector_coins}').json()
            
            transaction.valor -= client_reward + selector_reward
            
            data = {
                'message': 'Transaction completed',
                'validators': selected_clients,
                'selector': selector_client,
                'transaction': transaction.model_dump()
            }
            
            print('\nDATA', json.dumps(data), flush=True)
            return json.dumps(data)
        else:
            raise HTTPException(status_code=503, detail="Consensus checking failed")
    except Exception as e:
        data={
            "message": str(e)
        }
        return json.dumps(data)