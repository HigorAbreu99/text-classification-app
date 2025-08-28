from flask import Flask, request, render_template
import magic  # Para identificar o tipo de arquivo pelo conteúdo
import fitz   # PyMuPDF, para extrair texto de PDFs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def processar_entrada():
    resultado = None
    if request.method == 'POST':
        # Verifica se um arquivo foi enviado
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']

            # --- VERIFICAÇÃO DE CONTEÚDO (Magic Numbers) ---
            
            # 1. Define os MIME types que vamos aceitar.
            # Adicionamos 'application/pdf' à nossa lógica.
            MIME_TYPES_PERMITIDOS = ['application/pdf']

            # 2. Lê os primeiros 2KB do arquivo para análise.
            # Isso é suficiente para o python-magic identificar o tipo.
            chunk = file.stream.read(2048)
            
            # 3. CRUCIAL: Retorna o "ponteiro" do arquivo para o início!
            # Se não fizermos isso, a leitura posterior (para extrair o texto) começará do byte 2049.
            file.stream.seek(0)
            
            # 4. Pede ao magic para identificar o tipo real do arquivo a partir dos bytes lidos.
            mime_type_real = magic.from_buffer(chunk, mime=True)

            # 5. Verifica se o tipo real está na nossa lista de permissões OU se é um tipo de texto genérico.
            if mime_type_real.startswith('text/') or mime_type_real in MIME_TYPES_PERMITIDOS:
                
                try:
                    conteudo_extraido = ""
                    # --- LÓGICA DE EXTRAÇÃO DE TEXTO ---
                    # Se for PDF, usa o PyMuPDF para extrair o texto
                    if mime_type_real == 'application/pdf':
                        with fitz.open(stream=file.stream, filetype="pdf") as doc:
                            for page in doc:
                                conteudo_extraido += page.get_text()
                    
                    # Se for texto simples, apenas decodifica
                    else:
                        conteudo_extraido = file.read().decode('utf-8', errors='ignore')

                    # Agora processa o 'conteudo_extraido'
                    num_caracteres = len(conteudo_extraido)
                    resultado = f"Arquivo '{file.filename}' (tipo: {mime_type_real}) processado. Ele contém {num_caracteres} caracteres."

                except Exception as e:
                    resultado = f"Erro ao processar o conteúdo do arquivo: {e}"
            else:
                # Se o tipo não for permitido, rejeita o arquivo.
                resultado = f"ERRO: O conteúdo do arquivo foi identificado como '{mime_type_real}', que não é permitido. Apenas arquivos de texto e PDF são aceitos."

        # (A lógica para entrada de texto manual continua a mesma)
        elif 'text_input' in request.form and request.form['text_input'].strip() != '':
            texto = request.form['text_input']
            num_caracteres = len(texto)
            resultado = f"Texto processado. Ele contém {num_caracteres} caracteres."

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)