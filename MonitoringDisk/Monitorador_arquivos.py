import os
import sys
import json
import numpy as np
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time
import subprocess
from flask import app  # Importa a aplicação Flask


log_content = []

class ArquivoHandler(FileSystemEventHandler):
    def __init__(self, log_content):
        super().__init__()
        self.log_content = log_content

    def processar_arquivo(self, caminho_arquivo):
        print("═︎═︎")
        print(f'Arquivo criado/modificado: {caminho_arquivo}')
        print("═︎═︎")
        formato_data = "%Y%m%d"

        try:
            #================ Obtendo o nome base do arquivo e a data ================
            nome_base_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
            data_str = nome_base_arquivo[-8:]

            #================ Tentar converter a string de data para o formato esperado ================
            try:
                data = datetime.strptime(data_str, formato_data).strftime(formato_data)
            except ValueError:
                # Tratar o erro quando a conversão falhar
                print(f"Não foi possível extrair a data do arquivo {caminho_arquivo}. Usando data padrão.")
                print("═︎═︎")
                data = "data_padrao"

            #================ Verificar tamanho do arquivo ================
            tamanho_arquivo = os.path.getsize(caminho_arquivo) / (1024 * 1024)  # tamanho em MB
            #================ Tentar processar o arquivo ================
            df = pd.read_csv(caminho_arquivo) if caminho_arquivo.endswith('.csv') else pd.read_excel(caminho_arquivo, engine='openpyxl')
            colunas_vazias = df.columns[df.isnull().all()].tolist()
            quantidade_nan = df.isnull().sum().sum()
            print("\n ☠︎ Verificação Pandas rodou\n")

            #================ Carregar logs existentes ou criar uma lista vazia se o arquivo não existir ================
            try:
                with open('logs.json', 'r') as json_file:
                    logs_existentes = json.load(json_file)
            except FileNotFoundError:
                logs_existentes = []

            #================ Adicionar logs a uma lista ================
            log = {
                'arquivo': caminho_arquivo,
                'colunas_vazias': colunas_vazias,
                'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'quantidade_nan': quantidade_nan,
                'tamanho_mb': tamanho_arquivo,
            }
            
            #================ TRAZER LOGS EXISTENTES, CONVERSÃO E ADIÇÃO DE LOGS ================
            logs_existentes.append(log)
            # # Converter valores não serializáveis para tipos nativos Python
            logs_existentes = self.converter_para_tipo_nativo(logs_existentes)
            # # # Adicionar o novo log aos logs existentes
            # self.log_content.append(log)
            
            #================ Salvar a lista em um arquivo JSON ================
            with open('logs.json', 'w') as json_file:
                #json.dump(self.log_content, json_file, indent=2)
                json.dump(logs_existentes, json_file, indent=2)
                print("═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎\n")
                print(" ➙︎ Log adicionado à lista com sucesso!\n")
                print("═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎═︎")
                
        except Exception as e:
            # Lidar com exceções, registrar em log e continuar
            print("\nErro durante o processamento do arquivo na try 1:", str(e))
            print("\n")
            pass  # Ignorar o bloco de código em caso de exceção
        
#================ fUNÇÃO PARA CONVERTER VALORES NAO SERIALIZÁVEIS PARA NATIVOS PYTHON ================  

    def converter_para_tipo_nativo(self, obj):
        """
        Função recursiva para converter valores não serializáveis para tipos nativos Python.
        """
        if isinstance(obj, (np.generic, np.int64, np.float64)):
            return obj.item()
        elif isinstance(obj, list):
            return [self.converter_para_tipo_nativo(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.converter_para_tipo_nativo(value) for key, value in obj.items()}
        else:
            return obj
        
#================ fUNÇÕES PARA MODIFICAÇÕES E CRIAÇÕES NO DIRETÓRIO (MOSTRARÃO APENAS NO CONSOLE) ================ 
   
    def on_created(self, event):
        print("\n======================")
        print(f'Evento criado:\n{event.src_path}\n====================== ')
        if event.is_directory:
            return
        self.processar_arquivo(event.src_path)

    def on_modified(self, event):
        print("\n======================")
        print(f'Evento modificado:\n{event.src_path}\n====================== ')
        if event.is_directory:
            return
        self.processar_arquivo(event.src_path)
        
#================ CONFIGURAÇÕES ================

diretorio_rede = 'X:\\ARQUIVOS\\3810-GTSS\\'
caminho_logs = 'C:\\Users\\gustavo.costa\\Desktop\\MonitoringDisk\\'  
      
# Verificar e criar diretório de logs se não existir
if not os.path.exists(caminho_logs):
    os.makedirs(caminho_logs)

# Configurar o observador e o manipulador de eventos
log_content = []                     
event_handler = ArquivoHandler(log_content)
observer = Observer()


observer.schedule(event_handler, path=diretorio_rede, recursive=True)

#================ INICIANDO OBSERVADOR ================

if __name__ == '__main__':
    try:
        # ================ Iniciar o observador ================
        observer.start()
        print(" \n========================================================\n")
        print(" ♦♦♦ Observador Rodando ♦♦♦")
        print(" \n========================================================\n")
        # Iniciar o servidor Flask em um processo separado usando subprocess
        flask_command = [sys.executable, os.path.join(os.path.dirname(__file__), 'flaska.py')]
        flask_process = subprocess.Popen(flask_command, cwd=os.path.dirname(os.path.abspath(__file__)))
        # Mantenha o script em execução para continuar monitorando
        while True:
            time.sleep(1)  

    except KeyboardInterrupt:
        #================ Encerrar o observador e o servidor Flask ao interromper o script ================
        observer.stop()
        flask_process.terminate()

    # Aguardar a conclusão do observador e do servidor Flask
    observer.join()
    flask_process.wait() #http://10.0.162.63:5000/