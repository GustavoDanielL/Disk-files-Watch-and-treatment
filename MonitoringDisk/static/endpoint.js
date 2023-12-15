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

            data.forEach(log => {
                logContainer.innerHTML += '<p style="color: blue;">=================================================================</p>';
                logContainer.innerHTML += '<p>Arquivo: ' + log.arquivo + '</p>';
                logContainer.innerHTML += '<p>Colunas vazias: ' + log.colunas_vazias.join(', ') + '</p>';
                logContainer.innerHTML += '<p><strong>Data e Hora:</strong> ' + log.data_hora + '</p>';
                logContainer.innerHTML += '<p>Tamanho (MB): ' + log.tamanho_mb.toFixed(2) + '</p>';  // Ajuste para exibir com duas casas decimais
                logContainer.innerHTML += '<p>Quantidade de NaN: ' + log.quantidade_nan + '</p>';
                logContainer.innerHTML += '<p>DataFrame Vazio? ' + log.is_dataframe_empty + '</p>';
                logContainer.innerHTML += '<br>';  // Adiciona uma quebra de linha entre os logs
            });
        })
        .catch(error => console.error('Erro ao obter logs:', error));
        console.log('Endpoint.js executado com sucesso!');
    }

    setInterval(atualizarLogs, 120000);
    atualizarLogs();  // Execute a função uma vez ao carregar a página
});