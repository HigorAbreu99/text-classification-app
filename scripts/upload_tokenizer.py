# upload_tokenizer.py
from transformers import AutoTokenizer
from huggingface_hub import login

# Faça o login no Hugging Face (vai pedir seu token)
login()

# O nome do modelo base que você usou para treinar
base_model = "neuralmind/bert-base-portuguese-cased"

# O nome do seu repositório no Hub
repo_id = "hiigorabreu/email_classifier_trainer"

print(f"Carregando o tokenizador de '{base_model}'...")
tokenizer = AutoTokenizer.from_pretrained(base_model)

print(f"Enviando o tokenizador para '{repo_id}'...")
# Isso vai adicionar os arquivos do tokenizador ao seu repositório existente
tokenizer.push_to_hub(repo_id)

print("Tokenizador enviado com sucesso!")