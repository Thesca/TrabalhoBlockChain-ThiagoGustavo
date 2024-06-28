from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
  
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Cliente(db.Model):
    __tablename__ = "cliente_table"
    
    id: int
    nome: str
    senha: int
    qtdMoedas: int
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoedas = db.Column(db.Integer, unique=False, nullable=False)

@dataclass
class Validador(db.Model):
    __tablename__ = "validador_table"
    __allow_unmapped__ = True
    
    id: int
    cliente_id: int
    peso: int
    flags: int
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(20), db.ForeignKey(Cliente.id), unique=False)
    peso = db.Column(db.Integer, nullable=False)
    flags = db.Column(db.Integer, nullable=False)

@dataclass
class Seletor(db.Model):
    id: int
    nome: str
    ip: str
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)

@dataclass    
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    status: int
    
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)


#@app.before_first_request
#def create_tables():
#    db.create_all()

@app.route("/")
def index():
    return render_template('api.html')

@app.route('/cliente', methods = ['GET'])
def ListarCliente():
    if(request.method == 'GET'):
        clientes = Cliente.query.all()
        return jsonify(clientes)  

@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoedas>', methods = ['POST'])
def InserirCliente(nome, senha, qtdMoedas):
    if request.method=='POST' and nome != '' and senha != '' and qtdMoedas != '':
        objeto = Cliente(nome=nome, senha=senha, qtdMoedas=qtdMoedas)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods = ['GET'])
def UmCliente(id):
    if(request.method == 'GET'):
        objeto = Cliente.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>/<int:qtdMoedas>', methods=["POST"])
def EditarCliente(id, qtdMoedas):
    if request.method=='POST':
        try:
            varId = id
            varqtdMoedas = qtdMoedas
            cliente = Cliente.query.filter_by(id=id).first()
            db.session.commit()
            cliente.qtdMoedas = qtdMoedas
            db.session.commit()
            return jsonify(cliente)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods = ['DELETE'])
def ApagarCliente(id):
    if(request.method == 'DELETE'):
        objeto = Cliente.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Cliente Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador', methods = ['GET'])
def ListarValidador():
    if(request.method == 'GET'):
        validadores = Validador.query.all()
        return jsonify(validadores)  

@app.route('/validador/<int:cliente_id>', methods = ['POST'])
def InserirValidador(cliente_id, senha, qtdMoedas):
    if request.method=='POST' and cliente_id != '':
        objeto = Validador(cliente_id=cliente_id, flags=0)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>', methods = ['GET'])
def UmValidador(id):
    if(request.method == 'GET'):
        objeto = Validador.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>/<int:qtdMoedas>', methods=["POST"])
def EditarValidador(id, qtdMoedas):
    if request.method=='POST':
        try:
            varId = id
            varqtdMoedas = qtdMoedas
            validador = Validador.query.filter_by(id=id).first()
            db.session.commit()
            validador.qtdMoedas = qtdMoedas
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>', methods = ['DELETE'])
def ApagarValidador(id):
    if(request.method == 'DELETE'):
        objeto = Validador.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Validador Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])



@app.route('/seletor', methods = ['GET'])
def ListarSeletor():
    if(request.method == 'GET'):
        produtos = Seletor.query.all()
        return jsonify(produtos)  

@app.route('/seletor/<string:nome>/<string:ip>', methods = ['POST'])
def InserirSeletor(nome, ip):
    if request.method=='POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>', methods = ['GET'])
def UmSeletor(id):
    if(request.method == 'GET'):
        produto = Seletor.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>/<string:nome>/<string:ip>', methods=["POST"])
def EditarSeletor(id, nome, ip):
    if request.method=='POST':
        try:
            varNome = nome
            varIp = ip
            validador = Seletor.query.filter_by(id=id).first()
            db.session.commit()
            validador.nome = varNome
            validador.ip = varIp
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>', methods = ['DELETE'])
def ApagarSeletor(id):
    if(request.method == 'DELETE'):
        objeto = Seletor.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Validador Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/hora', methods = ['GET'])
def horario():
    if(request.method == 'GET'):
        objeto = datetime.now()
        return jsonify(objeto)
		
@app.route('/transacoes', methods = ['GET'])
def ListarTransacoes():
    if(request.method == 'GET'):
        transacoes = Transacao.query.all()
        return jsonify(transacoes)
    
    
@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods = ['POST'])
def CriaTransacao(rem, reb, valor):
    if request.method=='POST':
        objeto = Transacao(remetente=rem, recebedor=reb,valor=valor,status=0,horario=datetime.now())
        db.session.add(objeto)
        db.session.commit()
		
        seletores = Seletor.query.all()
        for i in seletores:
            url = seletores[i].ip + '/transacao'
            request.post(url, data=jsonify(objeto))
		
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacoes/<int:id>', methods = ['GET'])
def UmaTransacao(id):
    if(request.method == 'GET'):
        objeto = Transacao.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transactions/<int:id>/<int:status>', methods=["POST"])
def EditaTransacao(id, status):
    if request.method=='POST':
        try:
            objeto = Transacao.query.filter_by(id=id).first()
            db.session.commit()
            objeto.id = id
            objeto.status = status
            db.session.commit()
            return jsonify(objeto)
        except Exception as e:
            data={
                "message": "transação não atualizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
    
app.run(host='0.0.0.0', debug=True)