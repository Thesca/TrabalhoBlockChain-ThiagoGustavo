import requests

DB_API_URL = 'http://nonamecoin_db:5000'

response1 = requests.post(DB_API_URL + "/transacoes/1/2/50")
response2 = requests.post(DB_API_URL + "/transacoes/3/4/1000")
response3 = requests.post(DB_API_URL + "/transacoes/5/6/5000")
response4 = requests.post(DB_API_URL + "/transacoes/7/8/10000")
response5 = requests.post(DB_API_URL + "/transacoes/8/1/99999")

print(response1.json())
print(response2.json())
print(response3.json())
print(response4.json())
print(response5.json())