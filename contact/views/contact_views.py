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
    # Faz uma consulta (Query) no banco de dados. 
    # O método '.all()' busca TODOS os registros cadastrados na tabela de Contatos
    # e armazena o resultado (um QuerySet) na variável 'contacts'.
    contacts = Contact.objects.all()
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