// script.js

document.addEventListener("DOMContentLoaded", function () {
    function atualizarLogs() {
        console.log('Atualizando logs...');
        fetch('/obter_logs', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            var logContainer = document.getElementById('log-container');
            logContainer.innerHTML = '';

            data.forEach(log => {
                logContainer.innerHTML += '<p>' + log + '</p>';
            });
        })
        .catch(error => console.error('Erro ao obter logs:', error));
        console.log('Endpoint.js executado com sucessoooooooooo!');

    }

    setInterval(atualizarLogs, 60000);

    atualizarLogs();  // Execute a função uma vez ao carregar a página

});
