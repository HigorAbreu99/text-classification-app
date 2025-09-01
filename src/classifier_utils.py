from transformers import pipeline

# O caminho para o seu modelo no Hugging Face Hub
CLASSIFY_MODEL_PATH = "hiigorabreu/email_classifier_trainer"

def load_classifier():
    """
    Carrega e inicializa o pipeline de classificação de texto.
    Esta função é chamada apenas uma vez para evitar recarregamentos.
    """
    try:
        # device=-1 força o uso da CPU, o que é mais compatível para deploys iniciais.
        # Se você tiver uma GPU no seu ambiente de deploy, pode remover este argumento.
        classifier = pipeline(
            task="text-classification",
            model=CLASSIFY_MODEL_PATH,
            device=-1
        )
        return classifier
    except Exception as e:
        print(f"Erro fatal ao carregar o modelo: {e}")
        return None

def classify_email(classifier_pipeline, text: str) -> str:
    """
    Recebe um pipeline já carregado e um texto, e retorna a label predita.
    """
    if not classifier_pipeline or not text:
        return "Erro"

    try:
        # Garante que o texto não seja excessivamente longo para o modelo
        result = classifier_pipeline(text, truncation=True, max_length=512)
        return result[0]['label']
    except Exception as e:
        print(f"Erro durante a classificação: {e}")
        return "Erro"

