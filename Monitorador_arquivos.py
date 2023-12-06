import os
import sys

# Obtenha o diretório do script atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Adicione o diretório ao sys.path
sys.path.append(diretorio_atual)

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

formato_data = "%Y%m%d"
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

class ArquivoHandler(FileSystemEventHandler):
    def processar_arquivo(self, caminho_arquivo):
        # if caminho_arquivo in self.arquivos_processados:
        #     return
        # self.arquivos_processados.add(caminho_arquivo)
        print(f'Arquivo criado/modificado: {caminho_arquivo}\n ===')

        try:
            # Obtendo o nome base do arquivo e a data
            nome_base_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
            data = datetime.strptime(nome_base_arquivo[-8:], formato_data).strftime(formato_data)

            # Tentar processar o arquivo
            df = pd.read_csv(caminho_arquivo) if caminho_arquivo.endswith('.csv') else pd.read_excel(caminho_arquivo, engine='openpyxl')
            colunas_vazias = df.columns[df.isnull().all()].tolist()
            quantidade_nan = df.isnull().sum().sum()

            with open(os.path.join(caminho_logs, 'log.html'), 'a') as log_file:
                log_file.write(f'\n<p style="color: blue;">=================================================================</p>\n')
                log_file.write(f'<p>Arquivo: {caminho_arquivo}</p>\n')
                log_file.write(f'<p>Colunas vazias: {colunas_vazias}</p>\n')
                log_file.write(f'<p><strong>Data e Hora:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>\n')
                log_file.write(f'<p>Quantidade de NaN: {quantidade_nan}</p>\n\n')
                

            # Verificar tamanho do arquivo
            try:
                tamanho_minimo, formato_data = obter_requisito_tamanho(nome_base_arquivo, data)
            except TypeError:
                # Tratar o erro quando tamanho_minimo não é definido corretamente
                tamanho_minimo = float('1000000000000000')  # Definir um valor grande para indicar "infinito"

            tamanho_arquivo = os.path.getsize(caminho_arquivo) / 1024  # tamanho em KB

            with open(os.path.join(caminho_logs, 'log.html'), 'a') as log_file:
                if tamanho_arquivo > tamanho_minimo:
                    log_file.write(f'<p style="color: green;">O arquivo {caminho_arquivo} é maior que {tamanho_minimo}KB - Excedeu o limite de tamanho. com o tamanho de {tamanho_arquivo}</p>\n')
                    log_file.write(f'\n<p style="color: blue;">=================================================================</p>\n\n')
                elif tamanho_arquivo < tamanho_minimo:
                    log_file.write(f'\n<p style="color: red;">###############%%%%%%%%%%%%%%%%%%%%%##############################</p>\n\n')
                    log_file.write(f'<p style="color: red;">O arquivo {caminho_arquivo} é menor que {tamanho_minimo}KB - Não atingiu a expectativa de tamanho. com o tamanho de {tamanho_arquivo}</p>\n')
                    log_file.write(f'\n<p style="color: red;">###############%%%%%%%%%%%%%%%%%%%%%##############################</p>\n\n')
                elif colunas_vazias:
                    log_file.write(f'<p style="color: red;">#############################################################\n') 
                    log_file.write(f'<p style="color: red;">O arquivo {caminho_arquivo} veio com 1 ou mais COLUNAS VAZIAS\n')
                    log_file.write(f'<p>Colunas vazias: {colunas_vazias}</p>\n')
                    log_file.write(f'<p style="color: red;">#############################################################\n')    
        except Exception as e:
            # Lidar com exceções, registrar em log e continuar

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
observer = Observer()
event_handler = ArquivoHandler()
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