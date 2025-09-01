import os
import magic
import fitz  # PyMuPDF
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Importa as funções do nosso módulo de classificação
# (Vamos criar este arquivo a seguir)
from src.classifier_utils import load_classifier, classify_email

# Carrega as variáveis de ambiente (ex: FLASK_SECRET_KEY)
load_dotenv()

# --- CONFIGURAÇÃO INICIAL ---

# Carrega o modelo de IA UMA ÚNICA VEZ ao iniciar o app.
# Isso é crucial para o desempenho em produção.
print("A carregar o modelo de classificação... Isto pode demorar um momento.")
classifier_pipeline = load_classifier()
print("Modelo carregado com sucesso!")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'uma-chave-secreta-padrao-para-desenvolvimento')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

# Garante que a pasta de uploads exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Verifica se a extensão do ficheiro é permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    """Extrai texto de ficheiros .txt e .pdf."""
    try:
        mime_type = magic.from_file(filepath, mime=True)
        if mime_type == 'application/pdf':
            with fitz.open(filepath) as doc:
                return "".join(page.get_text() for page in doc), None
        elif mime_type.startswith('text/'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(), None
        else:
            return None, f"Tipo de ficheiro não suportado: {mime_type}"
    except Exception as e:
        return None, f"Erro ao processar o ficheiro: {str(e)}"
    finally:
        # Apaga o ficheiro após o processamento para economizar espaço
        if os.path.exists(filepath):
            os.remove(filepath)


@app.route('/', methods=['GET', 'POST'])
def pagina_inicial():
    if request.method == 'POST':
        text_content = ""
        error = None

        # Opção 1: Input de texto
        if 'text_input' in request.form and request.form['text_input'].strip():
            text_content = request.form['text_input']

        # Opção 2: Upload de ficheiro
        elif 'file' in request.files:
            file = request.files.get('file')
            if not file or file.filename == '':
                error = 'Nenhum ficheiro selecionado.'
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                text_content, error = extract_text_from_file(filepath)
            else:
                error = 'Extensão de ficheiro não permitida. Use .txt ou .pdf.'

        else:
            error = "Nenhum texto ou ficheiro enviado."

        if error:
            flash(error, 'danger')
            return redirect(url_for('pagina_inicial'))

        if not text_content or not text_content.strip():
            flash('O texto extraído está vazio.', 'warning')
            return redirect(url_for('pagina_inicial'))

        # Realiza a classificação usando o modelo já carregado
        label = classify_email(classifier_pipeline, text_content)

        # Mapeia a label para um resultado legível
        # LABEL_0 -> Produtivo, LABEL_1 -> Improdutivo
        if label == 'LABEL_0':
            result = 'Produtivo'
        else:
            result = 'Improdutivo'

        return render_template('resultado.html', result=result, text=text_content)

    return render_template('index.html')


@app.errorhandler(413)
def payload_too_large(e):
    flash('Ficheiro muito grande! O tamanho máximo permitido é de 16 MB.', 'danger')
    return redirect(url_for('pagina_inicial'))


if __name__ == '__main__':
    # host='0.0.0.0' permite que a app seja acessível na sua rede local,
    # o que é essencial para o Docker.
    app.run(host='0.0.0.0', port=5000, debug=True)

