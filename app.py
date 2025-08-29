# Adicione redirect, url_for e session aos seus imports
from flask import Flask, request, render_template, redirect, url_for, session
import magic
import fitz
import os # Necessário para a secret_key

app = Flask(__name__)

# IMPORTANTE: Para usar a 'session', o Flask exige uma "chave secreta" (secret_key).
# Para desenvolvimento, podemos usar uma chave aleatória como esta.
app.secret_key = os.urandom(24)

# A rota principal agora se chama 'pagina_inicial' para clareza
@app.route('/', methods=['GET', 'POST'])
def pagina_inicial():
    # A lógica de POST foi movida daqui para ser mais limpa
    if request.method == 'POST':
        conteudo_extraido = None
        erro = None
        
        # Lógica para ARQUIVO
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            MIME_TYPES_PERMITIDOS = ['application/pdf']
            chunk = file.stream.read(2048)
            file.stream.seek(0)
            mime_type_real = magic.from_buffer(chunk, mime=True)

            if mime_type_real.startswith('text/') or mime_type_real in MIME_TYPES_PERMITIDOS:
                try:
                    if mime_type_real == 'application/pdf':
                        file_bytes = file.stream.read()
                        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                            conteudo_extraido = "".join(page.get_text() for page in doc)
                    else:
                        conteudo_extraido = file.read().decode('utf-8', errors='ignore')
                except Exception as e:
                    erro = f"Erro ao processar o conteúdo do arquivo: {e}"
            else:
                erro = f"Formato de arquivo não suportado ({mime_type_real})."
        
        # Lógica para TEXTO
        elif 'text_input' in request.form and request.form['text_input'].strip() != '':
            conteudo_extraido = request.form['text_input']
        
        # Armazena os resultados na SESSÃO
        if erro:
            session['erro'] = erro
        elif conteudo_extraido:
            # Simula o processamento (contagem de caracteres)
            resultado_processamento = f"O texto contém {len(conteudo_extraido)} caracteres."
            session['texto_original'] = conteudo_extraido
            session['resultado'] = resultado_processamento
        
        # Redireciona para a página de resultados
        return redirect(url_for('exibir_resultado'))

    # Se a requisição for GET, apenas mostra a página inicial de upload
    return render_template('index.html')

# Nova rota APENAS para exibir os resultados
@app.route('/resultado')
def exibir_resultado():
    # Pega os dados da sessão (e os remove para não aparecerem novamente se a página for recarregada)
    erro = session.pop('erro', None)
    texto_original = session.pop('texto_original', None)
    resultado = session.pop('resultado', None)
    
    # Renderiza o novo template 'resultado.html' com os dados
    return render_template('resultado.html', erro=erro, texto_original=texto_original, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)