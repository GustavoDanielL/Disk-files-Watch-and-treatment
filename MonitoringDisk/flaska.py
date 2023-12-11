from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Ativar CORS para todas as rotas

#================ Inicializar a lista de logs a partir do arquivo JSON ================
log_content = []

@app.route('/')
def index():
    return render_template('index.html', logs=log_content)

@app.route('/obter_logs', methods=['GET'])
def obter_logs():
    print("Recebida solicitação para /obter_logs\n ===")
    
    #================ Ler logs do arquivo JSON ================
    with open('logs.json', 'r') as json_file:
        logs_from_file = json.load(json_file)
    
    #================ Responder com logs em formato JSON para solicitações GET ================
    return jsonify(logs_from_file)

if __name__ == '__main__':
    print("Iniciando o servidor Flask...")
    app.run(debug=True, host='0.0.0.0')
    # Adicione um pequeno atraso antes de iniciar o observador

