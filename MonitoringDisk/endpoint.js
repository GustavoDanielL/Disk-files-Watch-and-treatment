
// script.js
document.addEventListener("DOMContentLoaded", function () {
    function atualizarLogs() {
        console.log('Atualizando logs...');
        fetch('/obter_logs', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            var logContainer = document.getElementById('log-container');
            logContainer.innerHTML = '';

            if (data.length > 0) {
                var table = document.createElement('table');
                table.className = 'log-table';

                // Cabeçalho da tabela
                var headerRow = table.insertRow(0);
                var headers = ['Arquivo', 'Colunas Vazias', 'Data e Hora', 'Quantidade de NaN'];

                for (var i = 0; i < headers.length; i++) {
                    var headerCell = headerRow.insertCell(i);
                    headerCell.textContent = headers[i];
                }

                // Adicionar linhas à tabela com os dados JSON
                for (var i = 0; i < data.length; i++) {
                    var log = data[i];
                    var row = table.insertRow(i + 1);

                    var arquivoCell = row.insertCell(0);
                    arquivoCell.textContent = log.arquivo;

                    var colunasCell = row.insertCell(1);
                    colunasCell.textContent = log.colunas_vazias.join(', ');

                    var dataHoraCell = row.insertCell(2);
                    dataHoraCell.textContent = log.data_hora;

                    var quantidadeNanCell = row.insertCell(3);
                    quantidadeNanCell.textContent = log.quantidade_nan;
                }

                logContainer.appendChild(table);
            } else {
                logContainer.textContent = 'Nenhum log disponível.';
            }
        })
        .catch(error => console.error('Erro ao obter logs:', error));
        console.log('Endpoint.js executado com sucesso!');
    }

    setInterval(atualizarLogs, 30000);

    atualizarLogs();  // Execute a função uma vez ao carregar a página
});
