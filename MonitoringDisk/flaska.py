from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Ativar CORS para todas as rotas

# Inicializar a lista de logs
log_content = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obter_logs', methods=['GET'])
def obter_logs():
    print("Recebida solicitação para /obter_logs\n ===")
    try:
        json_data = jsonify(log_content)
        print(json_data)  # Imprima o JSON para verificar
        return json_data
    except Exception as e:
        print(f"Erro ao converter para JSON: {str(e)}")
        return jsonify({'error': 'Erro ao obter logs'}), 500  # Retorne um erro HTTP 500

if __name__ == '__main__':
    print("Iniciando o servidor Flask...\n ===")
    app.run(debug=True, host='0.0.0.0')
