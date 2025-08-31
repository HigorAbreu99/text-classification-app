import transformers

classify_model_path = "hiigorabreu/email_classifier_trainer"
response_model_path = "pierreguillou/gpt2-small-portuguese"

# TODO: achar uma forma de melhorar as respostas
def respond_email(text, classification):
    tokenizer = transformers.AutoTokenizer.from_pretrained(response_model_path)
    model = transformers.AutoModelWithLMHead.from_pretrained(response_model_path)
    tokenizer.model_max_length=1024 
    model.eval()
    question = ""
    
    if classification == "LABEL_0":
        question = f"""
        Gere uma resposta de até 500 caracteres para o e-mail abaixo, que foi classificado como produtivo. A resposta deve levar em conta os dados informados.

        ### Email:
        {text}

        ### Resposta:"
        """
    elif classification == "LABEL_1":
        question = f"""
        Gere uma resposta automática de até 256 caracteres e breve para o e-mail abaixo, que foi classificado como improdutivo. A resposta deve ser educada mas genérica, informando que a mensagem foi recebida.

        ### Email:
        {text}

        ### Resposta:"
        """
    else:
        raise ValueError(
        "Label inválido"
    )
    
    inputs = tokenizer(question, return_tensors="pt")

    result = []
    
    sample_outputs = model.generate(inputs.input_ids,
                                pad_token_id=50256,
                                do_sample=True, 
                                max_length=512,
                                top_k=40,
                                num_return_sequences=1
    )
    
    # Itere sobre as saídas do modelo
    for sample_output in sample_outputs:
        # Decodifique a saída para obter o texto puro e adicione à lista
        raw_text = tokenizer.decode(sample_output.tolist())
        result.append(raw_text)
        
    return result

def classify_email(text):
    pipelineClassify = transformers.pipeline(task="text-classification", model=classify_model_path)
    resultado_classificacao = pipelineClassify(text)
    
    return resultado_classificacao


