import threading
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Configuração do Flask
app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['arduino']  # Nome do banco de dados

@app.route('/masculina', methods=['POST'])
def postMasculinaMov():
    collection = db['masculina']
    dados = request.json
    if 'mov' in dados:
        # Adiciona a data e hora atuais
        dados['timestamp'] = datetime.now()  # Use datetime.now() para horário local se preferir
        result = collection.insert_one(dados)
        return jsonify({'msg': 'Movimentação na sessão masculina registrada', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'error': 'Dados incompletos'}), 400

@app.route('/movimentacoes/masculina', methods=['GET'])
def getMasculinaMov():
    collection = db['masculina']
    movimentacoes = collection.find()  # Busca todas as movimentações
    movimentacoes_list = []
    
    for mov in movimentacoes:
        # Convertendo _id do MongoDB para string
        mov['_id'] = str(mov['_id'])
        movimentacoes_list.append(mov)
    
    return jsonify(movimentacoes_list), 200

@app.route('/feminina', methods=['POST'])
def postFemininaMov():
    collection = db['feminina']
    dados = request.json
    if 'mov' in dados:
        # Adiciona a data e hora atuais
        dados['timestamp'] = datetime.now()  # Use datetime.now() para horário local se preferir
        result = collection.insert_one(dados)
        return jsonify({'msg': 'Movimentação na sessão feminina registrada', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'error': 'Dados incompletos'}), 400
    
@app.route('/movimentacoes/feminina', methods=['GET'])
def getFemininaMov():
    collection = db['feminina']
    movimentacoes = collection.find()  # Busca todas as movimentações
    movimentacoes_list = []
    
    for mov in movimentacoes:
        # Convertendo _id do MongoDB para string
        mov['_id'] = str(mov['_id'])
        movimentacoes_list.append(mov)


# Função para iniciar o servidor Flask em uma thread separada
def iniciar_flask():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)


# Iniciar a API Flask em uma thread separada
thread_flask = threading.Thread(target=iniciar_flask)
thread_flask.start()
