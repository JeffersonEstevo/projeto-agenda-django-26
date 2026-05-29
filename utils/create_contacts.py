import os  # Permite interagir com as variáveis de ambiente do sistema operacional
import sys  # Permite modificar caminhos do sistema para o Python encontrar módulos
from datetime import datetime  # Importa a classe para manipulação de datas e horários
from pathlib import Path  # Facilita a manipulação de caminhos de arquivos e pastas
from random import choice  # Função para escolher um item aleatório de uma lista

import django  # Importa o core do framework Django
from django.conf import settings  # Importa as configurações do projeto Django

# Descobre a pasta raiz do projeto Django subindo dois níveis a partir deste arquivo
DJANGO_BASE_DIR = Path(__file__).parent.parent
# Define a constante com a quantidade de contatos fictícios que serão criados
NUMBER_OF_OBJECTS = 1000

# Adiciona a raiz do projeto ao caminho de busca do Python para permitir os imports do Django
sys.path.append(str(DJANGO_BASE_DIR))
# Informa ao Django qual arquivo de configurações (settings.py) ele deve usar
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
# Desativa o fuso horário automático para evitar conflitos de timezone no script de seed
settings.USE_TZ = False

# Inicializa o Django carregando os modelos e as configurações do projeto
django.setup()

# Garante que o bloco abaixo só execute se este script for rodado diretamente no terminal
if __name__ == '__main__':
    import faker  # Importa a biblioteca Faker para geração de dados falsos e realistas

    # Importa os modelos de Categoria e Contato do aplicativo 'contact'
    from contact.models import Category, Contact

    # Apaga TODOS os contatos existentes no banco de dados para evitar duplicidade
    Contact.objects.all().delete()
    # Apaga TODAS as categorias existentes no banco de dados
    Category.objects.all().delete()

    # Inicializa o gerador de dados falsos configurado para o português do Brasil
    fake = faker.Faker('pt_BR')
    # Lista com os nomes das categorias que serão criadas no sistema
    categories = ['Amigos', 'Família', 'Conhecidos']

    # Cria uma lista de objetos 'Category' na memória (sem salvar no banco ainda) usando list comprehension
    django_categories = [Category(name=name) for name in categories]

    # Percorre a lista de categorias criadas na memória
    for category in django_categories:
        category.save()  # Salva cada categoria efetivamente no banco de dados

    # Cria uma lista vazia para acumular os objetos de contato que serão gerados
    django_contacts = []

    # Executa um laço de repetição 1.000 vezes (definido em NUMBER_OF_OBJECTS)
    for _ in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()  # Gera um perfil completo falso (nome, e-mail, etc.)
        email = profile['mail']  # Extrai o e-mail falso do perfil gerado
        # Divide o nome completo em primeiro nome e sobrenome usando o primeiro espaço encontrado
        first_name, last_name = profile['name'].split(' ', 1)
        phone = fake.phone_number()  # Gera um número de telefone brasileiro falso
        # Gera uma data de criação aleatória dentro do ano corrente
        created_date: datetime = fake.date_this_year()
        description = fake.text(max_nb_chars=100)  # Gera um texto descritivo de até 100 caracteres
        category = choice(django_categories)  # Escolhe aleatoriamente uma das 3 categorias salvas

        # Cria o objeto Contact na memória e o adiciona na lista 'django_contacts'
        django_contacts.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                created_date=created_date,
                description=description,
                category=category,
            )
        )

    # Verifica se a lista de contatos gerados na memória não está vazia
    if len(django_contacts) > 0:
        # Insere todos os 1.000 contatos de uma única vez no banco de dados (otimiza muito o desempenho)
        Contact.objects.bulk_create(django_contacts)
        