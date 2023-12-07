import os
import sys
import json
# Obtenha o diretório do script atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Adicione o diretório ao sys.path
sys.path.append(diretorio_atual)
import numpy as np
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time
import subprocess
from flask import app  # Importa a aplicação Flask



# Configurações
diretorio_rede = 'X:\\ARQUIVOS\\3810-GTSS\\'
caminho_logs = 'C:\\Users\\gustavo.costa\\Desktop\\Verificador'
limite_tamanho_arquivo_kb = 10000  # 10MB

nomes_base_arquivos = ['tHourlyUsage-v2', 'gTerminalData-v2', 'gDailyStats-v2', 'sHourlyUsageByCarrierVNO',
                       'sPerformanceDownload', 'sPerformanceLatency', 'sPerformanceUpload', 'beam_fullness_by_hour',
                       'Speedtestresultsbyvno', 't_CUST_Active_Accounts']


# Verificar e criar diretório de logs se não existir
if not os.path.exists(caminho_logs):
    os.makedirs(caminho_logs)

def obter_requisito_tamanho(nome_base_arquivo, data):
    # Defina requisitos de tamanho com base no nome_base_arquivo
    requisitos = {
        'tHourlyUsage-v2':{'tamanho':50000, 'formato_data': "%Y%m%d",},   
        'gTerminalData-v2':{'tamanho': 55000, 'formato_data': "%Y%m%d",}, 
        'gDailyStats-v2':{'tamanho':5500, 'formato_data': "%Y%m%d",},  
        'sHourlyUsageByCarrierVNO':{'tamanho':900, 'formato_data': "%Y%m%d",}, 
        'sPerformanceDownload':{'tamanho': 5000, 'formato_data': "%Y%m%d",},
        'sPerformanceLatency':{'tamanho':15000, 'formato_data': "%Y%m%d",}, 
        'sPerformanceUpload':{'tamanho':5000, 'formato_data': "%Y%m%d",}, 
        'beam_fullness_by_hour':{'tamanho':90, 'formato_data': "%Y%m%d",}, 
        'Speedtestresultsbyvno':{'tamanho':4000, 'formato_data': "%Y%m%d",}, 
        't_CUST_Active_Accounts':{'tamanho':6000, 'formato_data': "%Y%m%d",}
    }

    requisito = requisitos.get(nome_base_arquivo)
    if requisito:
        return requisito['tamanho'], requisito.get('formato_data', "%Y%m%d")
    else:
        return None, "%Y%m%d"  # Valor padrão para formato_data
log_content = []
class ArquivoHandler(FileSystemEventHandler):
    def __init__(self, log_content):
        super().__init__()
        self.log_content = log_content

    def processar_arquivo(self, caminho_arquivo):
        print(f'Arquivo criado/modificado: {caminho_arquivo}\n ===')
        formato_data = "%Y%m%d"

        try:
            # Obtendo o nome base do arquivo e a data
            nome_base_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
            data_str = nome_base_arquivo[-8:]

            # Tentar converter a string de data para o formato esperado
            try:
                data = datetime.strptime(data_str, formato_data).strftime(formato_data)
            except ValueError:
                # Tratar o erro quando a conversão falhar
                print(f"Não foi possível extrair a data do arquivo {caminho_arquivo}. Usando data padrão.")
                data = "data_padrao"

            # Tentar processar o arquivo
            df = pd.read_csv(caminho_arquivo) if caminho_arquivo.endswith('.csv') else pd.read_excel(caminho_arquivo, engine='openpyxl')
            colunas_vazias = df.columns[df.isnull().all()].tolist()
            quantidade_nan = df.isnull().sum().sum()
            print("try 1 rodou")

            # Adicionar logs a uma lista
            log = {
                'arquivo': caminho_arquivo,
                'colunas_vazias': colunas_vazias,
                'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'quantidade_nan': quantidade_nan,
            }

            self.log_content.append(log)
            print("Log adicionado à lista com sucesso!")

            # Salvar a lista em um arquivo JSON
            with open('logs.json', 'w') as json_file:
                json.dump(self.log_content, json_file)

            # Restante do código...
        except Exception as e:
            # Lidar com exceções, registrar em log e continuar
            print("Erro durante o processamento do arquivo na try 1:", str(e))
            pass  # Ignorar o bloco de código em caso de exceção
        
    def on_created(self, event):
        print(f'Evento criado: {event.src_path}')
        if event.is_directory:
            return
        self.processar_arquivo(event.src_path)

    def on_modified(self, event):
        print(f'Evento modificado: {event.src_path}')
        if event.is_directory:
            return
        self.processar_arquivo(event.src_path)

# Configurar o observador e o manipulador de eventos
log_content = []
event_handler = ArquivoHandler(log_content)
observer = Observer()

observer.schedule(event_handler, path=diretorio_rede, recursive=True)

if __name__ == '__main__':
    try:
        # Iniciar o observador
        observer.start()
        print("rodou")
        # Iniciar o servidor Flask em um processo separado usando subprocess
        flask_command = [sys.executable, os.path.join(os.path.dirname(__file__), 'flaska.py')]
        print("rodou")
        flask_process = subprocess.Popen(flask_command, cwd=os.path.dirname(os.path.abspath(__file__)))
        print("rodou")
        # Mantenha o script em execução para continuar monitorando
        while True:
            time.sleep(1)  # Adiciona um pequeno atraso para reduzir o uso da CPU

    except KeyboardInterrupt:
        # Encerrar o observador e o servidor Flask ao interromper o script
        observer.stop()
        flask_process.terminate()

    # Aguardar a conclusão do observador e do servidor Flask
    observer.join()
    flask_process.wait() #http://10.0.162.63:5000/