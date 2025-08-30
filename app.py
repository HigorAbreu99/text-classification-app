# Adicione redirect, url_for e session aos seus imports
from flask import Flask, request, render_template, redirect, url_for, session
import magic
import fitz
import os # Necessário para a secret_key
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Define o tamanho máximo do payload (upload) em 15 MB
# O cálculo é: 15 * 1024 (KB) * 1024 (MB)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
# -------------------------

# IMPORTANTE: Para usar a 'session', o Flask exige uma "chave secreta" (secret_key).
# Para desenvolvimento, podemos usar uma chave aleatória como esta.
#app.secret_key = os.urandom(24)

# 3. Carregue as chaves do ambiente usando os.getenv()
app.secret_key = os.getenv('FLASK_SECRET_KEY')
ANALYSIS_API_KEY = os.getenv('GEMINI_API_KEY')

# Verificação para garantir que as chaves foram carregadas
if not app.secret_key or not ANALYSIS_API_KEY:
    raise ValueError("Chaves secretas não encontradas no ambiente. Verifique seu arquivo .env")

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

            # --- INÍCIO DA INTEGRAÇÃO COM A API EXTERNA ---
            # try:
            #     api_url = "https://api.exemplo.com/analise_sentimento"
                
            #     # 1. Defina os seus headers em um dicionário.
            #     headers = {
            #         'Content-Type': 'application/json',
            #         'Accept': 'application/json',
            #         'X-API-Key': 'SUA_CHAVE_SECRETA_DA_API_AQUI',
            #         'User-Agent': 'MeuAppDeClassificacao/1.0'
            #     }

            #     # Dados a serem enviados no corpo (body) da requisição POST
            #     payload = {
            #         'texto': conteudo_extraido
            #     }

            #     # 2. Adicione o argumento 'headers=headers' à sua chamada POST.
            #     response = requests.post(api_url, json=payload, headers=headers, timeout=10)

            #     response.raise_for_status()

            #     dados_api = response.json()
            #     sentimento = dados_api.get('sentimento', 'desconhecido')
            #     score = dados_api.get('score', 0)

            #     resultado_processamento = f"Sentimento detectado: {sentimento} (Confiança: {score:.2f})."
            #     session['texto_original'] = conteudo_extraido
            #     session['resultado'] = resultado_processamento

            # except requests.exceptions.RequestException as e:
            #    session['erro'] = f"Erro ao contatar o serviço de análise: {e}"
            # --- FIM DA INTEGRAÇÃO ---
        
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

# --- MANIPULADOR DE ERRO PERSONALIZADO PARA ARQUIVOS GRANDES ---
@app.errorhandler(413)
def payload_too_large(e):
    # Reutilizamos nosso template de resultado para mostrar o erro
    erro_msg = f"Arquivo muito grande! O tamanho máximo permitido é de 15 MB."
    return render_template('resultado.html', erro=erro_msg), 413
# -------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)