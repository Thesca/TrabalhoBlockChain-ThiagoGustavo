import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import random
from datetime import datetime, timedelta
from typing import List

DB_API_URL = 'http://nonamecoin_db:5000'

app = FastAPI()

# Dicionario de exemplo dos validadores
validators = {
    'validator-1': {'coins': 1000, 'flags': 0, 'hold_count': 0},
    'validator-2': {'coins': 800, 'flags': 0, 'hold_count': 0},
    'validator-3': {'coins': 1200, 'flags': 0, 'hold_count': 0},
    'validator-4': {'coins': 600, 'flags': 0, 'hold_count': 0},
    'validator-5': {'coins': 1500, 'flags': 0, 'hold_count': 0},
    'validator-6': {'coins': 900, 'flags': 0, 'hold_count': 0},
}

class Transaction(BaseModel):
    id: int
    remetente: int
    recebedor: int
    valor: int
    status: int

from typing import List, Dict

def select_validators(transaction: Transaction, validators: Dict[str, Dict[str, int]]) -> List[str]:
    selected_validators = []
    validator_choices = []

    # Calculate chance based on validator coins and flags
    for ip, info in validators.items():
        if info['coins'] >= transaction.valor:
            chance = 1.0  # Default chance

            # Adjust chance based on flags
            if info['flags'] == 1:
                chance *= 0.5  # 50% reduction for Flag=1
            elif info['flags'] == 2:
                chance *= 0.25  # 75% reduction for Flag=2
            
            # Ensure chance is between 0% and 20%
            chance = max(0.0, min(chance, 0.2))

            validator_choices.append((ip, chance))
    
    # Sort validators by chance (descending) and select up to 3
    sorted_validators = sorted(validator_choices, key=lambda x: x[1], reverse=True)[:3]
    selected_validators = [ip for ip, chance in sorted_validators]

    return selected_validators


def check_consensus(selected_validators: List[str]) -> bool:
    approved_count = 0
    for ip in selected_validators:
        # Assuming each validator responds with status 1 or 2 (approved or not approved)
        response = requests.get(f'http://{ip}:8000/validate')
        status = response.json().get('status', 0)
        if status == 1:
            approved_count += 1
    
    return approved_count > len(selected_validators) / 2

def update_validator_flags(ip: str, is_inconsistent: bool):
    if is_inconsistent:
        validators[ip]['flags'] += 1
        if validators[ip]['flags'] > 2:
            # Remove validator from network (simulated by resetting coins)
            validators[ip]['coins'] = 0

def handle_hold(ip: str):
    validators[ip]['hold_count'] = 5

@app.get("/healthcheck")
def healthcheck():
    return {"message": "Service is running"}

@app.post("/transacao")
def process_transaction(transaction: Transaction):
    selected_validators = select_validators(transaction)
    
    # Check if minimum validators are available
    if len(selected_validators) < 3:
        raise HTTPException(status_code=503, detail="Not enough validators available. Transaction pending.")
    
    # Perform transaction validation with selected validators
    if check_consensus(selected_validators):
        # Successful transaction logic
        # Assuming 1.0% reward for selector and 0.5% held for validator
        # Update balances, handle flags, etc.
        for ip in selected_validators:
            response = requests.post(f'http://{ip}:8000/validate', json=transaction.model_dump())
            validator_response = response.json()
            if validator_response['status'] == 1:
                # Successful validation logic
                validators[ip]['coins'] += transaction.valor * 0.005  # 0.5% for validator
                # Handle transaction counts for flags
                # Update selector's balance, assuming 1.0% reward
                selector_reward = transaction.valor * 0.010  # 1.0% for selector
                # Update selector's balance, assuming 1.0% reward
