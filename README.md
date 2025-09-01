# text-classification-app

Este projeto é uma aplicação web desenvolvida com Flask que utiliza um modelo de Machine Learning da Hugging Face para classificar textos de e-mails como "Produtivo" ou "Improdutivo". A aplicação fornece uma interface simples onde o utilizador pode digitar, colar ou fazer upload de um ficheiro (.txt ou .pdf) contendo o texto do e-mail para análise.

## Funcionalidades
Análise de Texto Direta: Cole ou digite o texto de um e-mail diretamente numa caixa de texto.

Upload de Ficheiros: Envie ficheiros .txt ou .pdf para extrair e analisar o seu conteúdo.

Feedback Visual Imediato: A página de resultados muda de cor para verde (Produtivo) ou vermelho (Improdutivo), oferecendo uma resposta clara e instantânea.

Interface Responsiva: O layout adapta-se a diferentes tamanhos de ecrã.

## Tecnologias Utilizadas
Backend: Flask

Machine Learning: Transformers (Hugging Face), PyTorch

Frontend: HTML5, CSS3, JavaScript

Manipulação de Ficheiros: PyMuPDF (para PDFs), python-magic (para verificação de tipo de ficheiro)

Ambiente: python-dotenv

## Repositório do Model treinado
https://huggingface.co/hiigorabreu/email_classifier_trainer

## Estrutura do Projeto
.
├── app.py                   # Ficheiro principal da aplicação Flask
├── train.py                 # Script para treinar o modelo de classificação
├── requirements.txt         # Lista de dependências Python
├── .env.example             # Exemplo de ficheiro para variáveis de ambiente
├── .gitignore               # Ficheiros e pastas a serem ignorados pelo Git
├── src/
│   └── classifier_utils.py  # Módulo que carrega e executa o modelo de IA
├── templates/
│   ├── index.html           # Página inicial com os formulários
│   └── resultado.html       # Página que exibe o resultado da análise
└── static/
    ├── css/style.css        # Folha de estilos
    └── js/main.js           # Scripts do lado do cliente

Configuração e Instalação Local
Siga os passos abaixo para executar o projeto na sua máquina.

1. Clonar o Repositório
git clone https://github.com/HigorAbreu99/text-classification-app.git
cd text-classification-app

2. Criar e Ativar o Ambiente Virtual
É uma boa prática isolar as dependências do projeto.

# Criar o ambiente
python3 -m venv venv

# Ativar no macOS/Linux
source venv/bin/activate

# Ativar no Windows
.\\venv\\Scripts\\activate

3. Instalar as Dependências
Instale todas as bibliotecas necessárias a partir do ficheiro requirements.txt.

pip install -r requirements.txt

4. Configurar as Variáveis de Ambiente
Crie um ficheiro chamado .env na raiz do projeto e adicione a chave secreta necessária para o Flask.

FLASK_SECRET_KEY='uma-chave-secreta-muito-forte-e-aleatoria'

5. Executar a Aplicação
Inicie o servidor de desenvolvimento do Flask.

flask run
# ou
python3 app.py

A aplicação estará disponível em http://127.0.0.1:5000 no seu navegador.

Como Utilizar
Aceda à página inicial.

Opção 1: Escreva ou cole o texto do e-mail na caixa de texto e clique em "Analisar Texto".

Opção 2: Clique em "Escolher Ficheiro", selecione um .txt ou .pdf e clique em "Analisar Ficheiro".

A página de resultados será exibida com a classificação e a cor de fundo correspondente.