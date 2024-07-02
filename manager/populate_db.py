import requests

DB_API_URL = 'http://nonamecoin_db:5000'

# Insert validators: nome / senha / qtdMoedas / ip
requests.post(DB_API_URL + '/cliente/joao/1234/3000/127.0.1.1') # id 1
requests.post(DB_API_URL + '/cliente/maria/abc/6000/127.0.1.2') # id 2
requests.post(DB_API_URL + '/cliente/carlos/1234abc/9000/127.0.1.3') # id 3
requests.post(DB_API_URL + '/cliente/fernanda/1234/15000/127.0.1.4') # id 4
requests.post(DB_API_URL + '/cliente/jose/abc/9000/127.0.1.5') # id 5
requests.post(DB_API_URL + '/cliente/henrique/1234abc/0/127.0.1.6') # id 6
requests.post(DB_API_URL + '/cliente/joaquina/1234abc/26000/127.0.1.7') # id 7
requests.post(DB_API_URL + '/cliente/alberto/1234abc/0/127.0.1.8') # id 8

# Register clients as validators: cliente_id / peso
requests.post(DB_API_URL + '/validador/1/100')
requests.post(DB_API_URL + '/validador/2/200')
requests.post(DB_API_URL + '/validador/3/30')
requests.post(DB_API_URL + '/validador/4/1000')
requests.post(DB_API_URL + '/validador/5/20')
requests.post(DB_API_URL + '/validador/6/0')

# Register selector: cliente_id
requests.post(DB_API_URL + '/seletor/7')