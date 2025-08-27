# Instale o Flask primeiro: pip install Flask
from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)
# Define a pasta onde os arquivos serão salvos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Garante que a pasta exista
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML básico para a página de upload em uma string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Classificador de Emails</title>
</head>
<body>
    <h1>Faça o upload do seu arquivo</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Processar">
    </form>
    {% if resultado %}
        <h2>Resultado do Processamento:</h2>
        <p>{{ resultado }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    resultado = None
    if request.method == 'POST':
        # Verifica se um arquivo foi enviado na requisição
        if 'file' not in request.files:
            return redirect(request.url) # Recarrega a página se nenhum arquivo for enviado
        
        file = request.files['file']
        
        # Se o usuário não selecionar um arquivo, o navegador envia um campo vazio
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Salva o arquivo na pasta 'uploads'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # --- AQUI VOCÊ COLOCA A LÓGICA DE PROCESSAMENTO ---
            # Exemplo simples: contar o número de linhas do arquivo
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    num_linhas = sum(1 for line in f)
                resultado = f"O arquivo '{file.filename}' foi processado com sucesso e contém {num_linhas} linhas."
            except Exception as e:
                resultado = f"Erro ao processar o arquivo: {e}"
            # ----------------------------------------------------

    # Renderiza o template HTML passando o resultado (se houver)
    return render_template_string(HTML_TEMPLATE, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True) # debug=True é ótimo para desenvolvimento