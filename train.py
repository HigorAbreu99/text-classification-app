# train.py
from huggingface_hub import login

# Agrupe as importações da mesma biblioteca para maior clareza
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,  # <-- CORREÇÃO: Trainer foi adicionado aqui
)
from datasets import Dataset
import numpy as np
import evaluate
from src import read_json


def tokenize(examples):
    return tokenizer(
        examples["text"], padding="max_length", truncation=True, max_length=512
    )


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    # convert the logits to their predicted class
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


login()

baseModel = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(baseModel)
metric = evaluate.load("accuracy")

# --- PASSO 1: CARREGAR O DATASET LOCAL ---

caminho_dataset = "data/raw/dataset.json"
print(f"Carregando dataset de '{caminho_dataset}' com a função read_json...")

dados_em_lista = read_json(caminho_dataset)

if dados_em_lista:
    dataset = Dataset.from_list(dados_em_lista)
else:
    print("Falha ao carregar o dataset. Encerrando o script.")
    exit()

print("Dataset carregado e convertido com sucesso!")
print(dataset)

# dataset = dataset.map(tokenize, batched=True)
train_test_split = dataset.train_test_split(test_size=0.2)

dataset = train_test_split.map(tokenize, batched=True)

small_train = dataset["train"].shuffle(seed=42).select(range(800))
small_eval = dataset["test"].shuffle(seed=42).select(range(200))

model = AutoModelForSequenceClassification.from_pretrained(baseModel, num_labels=2)

training_args = TrainingArguments(
    output_dir="email_classifier_trainer",
    eval_strategy="epoch",
    push_to_hub=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
)

trainer.train()

trainer.push_to_hub()
