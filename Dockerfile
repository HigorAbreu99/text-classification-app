# --- Estágio 1: Imagem Base e Instalação de Dependências ---
# Usamos uma imagem Python "slim", que é mais leve e ideal para produção.
FROM python:3.12-slim AS base

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Atualiza o pip e instala as dependências do sistema necessárias para a biblioteca `magic`.
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*

# Copia apenas o ficheiro de requisitos primeiro.
# Isto aproveita o cache do Docker: se o requirements.txt não mudar,
# o Docker não reinstalará tudo a cada build.
COPY requirements.txt .

# Instala as dependências Python.
# O --no-cache-dir reduz o tamanho da imagem.
RUN pip install --no-cache-dir -r requirements.txt


# --- Estágio 2: Imagem Final da Aplicação ---
# Começamos de novo a partir da imagem base para manter a imagem final limpa.
FROM python:3.12-slim

WORKDIR /app

# Copia as dependências do sistema do estágio anterior.
COPY --from=base /usr/lib/x86_64-linux-gnu/libmagic.so.1 /usr/lib/x86_64-linux-gnu/
COPY --from=base /usr/share/file /usr/share/file

# Copia as dependências Python instaladas do estágio anterior.
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Agora, copia o código da sua aplicação.
COPY . .

# Expõe a porta 5000, que é a porta que o Gunicorn irá usar dentro do container.
EXPOSE 5000

# O comando que será executado quando o container iniciar.
# Inicia o servidor Gunicorn com 4 workers, ouvindo na porta 5000.
# "app:app" refere-se ao objeto `app` dentro do ficheiro `app.py`.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]