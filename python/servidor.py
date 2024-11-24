import threading
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Configuração do Flask
app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['arduino']  # Nome do banco de dados

# Endpoint para registrar movimentações em uma sessão
@app.route('/<sessao>', methods=['POST'])
def postMovimentacao(sessao):
    if sessao not in ['masculina', 'feminina', 'infantil', 'esportes']:
        return jsonify({'error': f'Sessão "{sessao}" não encontrada'}), 404

    collection = db[sessao]
    dados = request.json

    if 'mov' in dados:
        # Adiciona data e hora atuais
        dados['timestamp'] = datetime.now()
        result = collection.insert_one(dados)
        return jsonify({'msg': f'Movimentação na sessão {sessao} registrada', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'error': 'Dados incompletos'}), 400

# Endpoint para listar movimentações de uma sessão
@app.route('/movimentacoes/<sessao>', methods=['GET'])
def getMovimentacoes(sessao):
    if sessao not in ['masculina', 'feminina', 'infantil', 'esportes']:
        return jsonify({'error': f'Sessão "{sessao}" não encontrada'}), 404

    collection = db[sessao]

    try:
        # Busca movimentações e ordena por timestamp (1 para ordem crescente)
        movimentacoes = collection.find().sort('timestamp', -1)
        movimentacoes_list = []

        for mov in movimentacoes:
            # Converte _id do MongoDB para string
            mov['_id'] = str(mov['_id'])
            # Formata o timestamp para string legível
            if 'timestamp' in mov:
                mov['timestamp'] = mov['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')
            movimentacoes_list.append(mov)

        return jsonify(movimentacoes_list), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar movimentações', 'details': str(e)}), 500

# Função para iniciar o servidor Flask em uma thread separada
def iniciar_flask():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

# Iniciar a API Flask em uma thread separada
thread_flask = threading.Thread(target=iniciar_flask)
thread_flask.start()
