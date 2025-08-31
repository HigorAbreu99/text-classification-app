import random
from pathlib import Path
from src import write_json


# --- DADOS PARA PREENCHER OS TEMPLATES (Mantidos do script original) ---

NOMES = [
    "Ana",
    "Bruno",
    "Carlos",
    "Daniela",
    "Eduardo",
    "Fernanda",
    "Gustavo",
    "Helena",
]
PROJETOS = ["Alpha", "Beta", "Gamma", "Delta", "Ômega"]
TAREFAS = [
    "relatório de vendas",
    "atualização do servidor",
    "revisão do design",
    "teste da nova feature",
]
BUGS = [
    "erro de login",
    "botão de salvar não funciona",
    "lentidão na API",
    "layout quebrado no mobile",
]
EVENTOS = ["Feliz Aniversário", "Feliz Natal", "Feliz Ano Novo", "Boas Festas"]
ASSUNTOS_ALEATORIOS = [
    "receita de bolo de cenoura",
    "melhores filmes de 2024",
    "indicação de série",
]

# --- TEMPLATES DOS E-MAILS (Mantidos do script original) ---

TEMPLATES_PRODUTIVOS = [
    lambda: f"Prezados, segue em anexo o {random.choice(TAREFAS)} referente ao projeto {random.choice(PROJETOS)}. Por favor, confirmem o recebimento. Atenciosamente, {random.choice(NOMES)}.",
    lambda: f"Olá, {random.choice(NOMES)}. Você poderia me dar um update sobre o andamento da tarefa '{random.choice(TAREFAS)}'? Precisamos finalizar até o final da semana. Obrigado!",
    lambda: f"Equipe, identifiquei um novo bug na aplicação: {random.choice(BUGS)}. A prioridade é alta. Alguém pode verificar? Att, {random.choice(NOMES)}.",
    lambda: f"Bom dia. Agendei uma reunião para amanhã às 10h para discutirmos o planejamento do projeto {random.choice(PROJETOS)}. O convite já está na agenda de vocês.",
    lambda: f"Oi, {random.choice(NOMES)}. Estou enviando os documentos necessários para a próxima fase do projeto {random.choice(PROJETOS)}. Qualquer dúvida, estou à disposição.",
]

TEMPLATES_IMPRODUTIVOS = [
    lambda: f"{random.choice(EVENTOS)} para você, {random.choice(NOMES)}! Tudo de bom!",
    lambda: f"Pessoal, quem vai participar do nosso happy hour de sexta-feira? Confirmem presença até amanhã!",
    lambda: f"Bom dia, equipe! Passando apenas para desejar uma ótima semana a todos!",
    lambda: f"Alguém aqui sabe me dizer uma boa {random.choice(ASSUNTOS_ALEATORIOS)}? Abraços, {random.choice(NOMES)}.",
    lambda: f"Olá, {random.choice(NOMES)}. Você viu aquele vídeo engraçado que está circulando na internet? Estou te mandando o link.",
]


# --- LÓGICA DE GERAÇÃO DO DATASET (Modificada para o novo formato) ---


def gerar_dataset(total_de_emails=1000):
    """
    Gera uma lista de dicionários de e-mails, cada um com 'label' (0 ou 1) e 'text'.
    """
    # Mapeamento dos tipos para os labels numéricos solicitados
    label_map = {"productive": 0, "unproductive": 1}

    dataset = []
    for _ in range(total_de_emails):
        # Decide aleatoriamente se o e-mail será produtivo ou improdutivo
        if random.choice([True, False]):
            tipo = "productive"
            texto_email = random.choice(TEMPLATES_PRODUTIVOS)()
        else:
            tipo = "unproductive"
            texto_email = random.choice(TEMPLATES_IMPRODUTIVOS)()

        # Converte o tipo de texto para o label numérico
        label_numerica = label_map[tipo]

        # Adiciona o e-mail gerado à lista no novo formato
        dataset.append({"label": label_numerica, "text": texto_email})

    return dataset


# --- EXECUÇÃO PRINCIPAL E EXPORTAÇÃO (Mantida do script original) ---

if __name__ == "__main__":
    print("Gerando o dataset de e-mails no novo formato...")

    meu_dataset = gerar_dataset(1000)

    # 2. Converta a string do caminho para um objeto Path
    caminho_diretorio = Path("data/raw")

    nome_arquivo = "dataset.json"
    # Agora o operador / funciona corretamente
    caminho_completo_arquivo = caminho_diretorio / nome_arquivo

    print(f"Salvando o arquivo em: {caminho_completo_arquivo}")

    # A chamada da sua função write_json já estava correta
    write_json(meu_dataset, caminho_completo_arquivo)
