// Seleciona os elementos comuns
const resultadoContainer = document.getElementById("resultado-container");

// --- Lógica para o formulário de UPLOAD DE ARQUIVO ---
const fileInput = document.getElementById("file-input");
const uploadForm = document.getElementById("upload-form");

if (fileInput && uploadForm) {
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            resultadoContainer.innerHTML =
                "<h2>Processando arquivo, por favor aguarde...</h2>";
            uploadForm.submit();
        }
    });
}

// --- Lógica para o formulário de ENVIO DE TEXTO ---
const textForm = document.getElementById("text-form");

if (textForm) {
    // Escuta o evento 'submit', que é disparado quando o botão é clicado
    textForm.addEventListener("submit", function () {
        // Mostra a mensagem de processamento antes de a página recarregar
        resultadoContainer.innerHTML =
            "<h2>Processando texto, por favor aguarde...</h2>";
    });
}

// --- LÓGICA PARA MOSTRAR O NOME DO ARQUIVO SELECIONADO ---
const fileInputForName = document.getElementById("file-input");
const fileNameDisplay = document.getElementById("file-name");

if (fileInputForName && fileNameDisplay) {
    // Escuta o evento 'change' do input de arquivo (que ainda funciona, mesmo escondido)
    fileInputForName.addEventListener("change", function () {
        // Se um ou mais arquivos foram selecionados...
        if (fileInputForName.files.length > 0) {
            // ...mostra o nome do primeiro arquivo no nosso <span>
            fileNameDisplay.textContent = fileInputForName.files[0].name;
        } else {
            // Se o usuário cancelar, volta ao texto original
            fileNameDisplay.textContent = "Nenhum arquivo selecionado";
        }
    });
}

// --- LÓGICA PARA O BOTÃO LIMPAR ---
const clearButton = document.getElementById("clear-button");
const textInput = document.getElementById("text-input");

// Verifica se ambos os elementos existem na página antes de adicionar o listener
if (clearButton && textInput) {
    // Adiciona um "escutador de eventos" que espera pelo clique no botão
    clearButton.addEventListener("click", function () {
        // Define o valor da caixa de texto como uma string vazia
        textInput.value = "";
    });
}
