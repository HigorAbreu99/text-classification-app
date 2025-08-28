// Seleciona os elementos comuns
const resultadoContainer = document.getElementById('resultado-container');

// --- Lógica para o formulário de UPLOAD DE ARQUIVO ---
const fileInput = document.getElementById('file-input');
const uploadForm = document.getElementById('upload-form');

if (fileInput && uploadForm) {
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            resultadoContainer.innerHTML = '<h2>Processando arquivo, por favor aguarde...</h2>';
            uploadForm.submit();
        }
    });
}


// --- Lógica para o formulário de ENVIO DE TEXTO ---
const textForm = document.getElementById('text-form');

if (textForm) {
    // Escuta o evento 'submit', que é disparado quando o botão é clicado
    textForm.addEventListener('submit', function() {
        // Mostra a mensagem de processamento antes de a página recarregar
        resultadoContainer.innerHTML = '<h2>Processando texto, por favor aguarde...</h2>';
    });
}