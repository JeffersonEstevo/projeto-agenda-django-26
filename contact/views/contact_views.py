# render é uma função auxiliar que une um template HTML com dados para o navegador
from django.shortcuts import render
# Por que você precisa importar 'contact.models'?
# O Django trabalha com o padrão MVT (Model-View-Template). A sua View precisa buscar 
# os dados guardados no banco de dados para poder enviá-los ao template HTML. 
# A classe 'Contact' é a representação da sua tabela do banco de dados em código Python. 
# Sem essa importação, a View não saberia onde buscar as informações dos contatos.
from contact.models import Contact

# Função que processa a requisição da página inicial
def index(request):
    # .filter(show=True) -> Filtra os resultados. Só traz os contatos onde 
    # o campo 'show' é Verdadeiro (True).
    # .order_by('-id')   -> Ordena os dados. O sinal de menos '-' 
    # indica ordem decrescente (do ID maior para o menor / mais recentes primeiro).
    # [10:20]            -> Faz o fatiamento (Slicing). Cria uma paginação que 
    # pula os 10 primeiros registros e pega do 11º ao 20º.
    contacts = Contact.objects \
    .filter(show=True) \
    .order_by('-id')[10:20]
    

    # Exibe no terminal do servidor o comando SQL puro que o ORM do Django gerou para o banco de dados.
    # Útil para debugar e entender a performance da consulta.
    # print(contacts.query)

    # Um dicionário Python que serve como "ponte" de dados.
    # A chave em string 'contacts' será o nome da variável que o seu 
    # arquivo HTML (index.html) vai ler para exibir as informações.
    context = {
        'contacts': contacts,
    }
    
    # Retorna o arquivo HTML renderizado localizado na pasta de templates
    return render(
        request,              # O objeto da requisição HTTP obrigatório
        'contact/index.html', # Caminho do arquivo HTML que será exibido
        context
    )

