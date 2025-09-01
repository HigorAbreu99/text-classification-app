document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const clearButton = document.getElementById('clear-button');
    const textInput = document.getElementById('text-input');
    const form = document.querySelector('form');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Mostra o nome do ficheiro selecionado
    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
            } else {
                fileNameDisplay.textContent = 'Nenhum ficheiro selecionado';
            }
        });
    }

    // Limpa a caixa de texto
    if (clearButton && textInput) {
        clearButton.addEventListener('click', function() {
            textInput.value = '';
        });
    }

    // Mostra "A carregar..." ao submeter o formulário
    if (form && loadingIndicator) {
        form.addEventListener('submit', function() {
            loadingIndicator.style.display = 'block';
        });
    }
});
