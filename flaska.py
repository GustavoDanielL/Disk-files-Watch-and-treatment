from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

log_content = []  # Inicializar a lista de logs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obter_logs', methods=['POST'])
def obter_logs():
    print("Recebida solicitação para /obter_logs\n ===")
    if request.method == 'POST':
        # Lógica para lidar com solicitações POST, se necessário
        pass

    # Responder com logs em formato JSON para solicitações GET
    return jsonify(log_content)

if __name__ == '__main__':
    print("Iniciando o servidor Flask...\n ===")
    app.run(debug=True, host='0.0.0.0')
