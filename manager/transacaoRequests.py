import requests

response1 = requests.post("localhost:5000/transacoes/1/2/10")
response2 = requests.post("localhost:5000/transacoes/3/4/50")
response3 = requests.post("localhost:5000/transacoes/5/6/100")
response4 = requests.post("localhost:5000/transacoes/7/8/10000")
response5 = requests.post("localhost:5000/transacoes/8/1/99999")

print(response1.json())
print(response2.json())
print(response3.json())
print(response4.json())
print(response5.json())