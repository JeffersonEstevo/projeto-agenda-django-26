# Importa o utilitário de paginação do Django para dividir listas longas em várias páginas
from django.core.paginator import Paginator
# Importa o objeto Q para realizar consultas complexas no banco de dados (usando operadores OU/AND)
from django.db.models import Q
# Importa atalhos essenciais: buscar objeto ou retornar 404, redirecionar rotas e renderizar templates HTML
from django.shortcuts import get_object_or_404, redirect, render

# Importa o modelo de dados 'Contact' que representa a tabela de contatos no banco de dados
from contact.models import Contact


# Define a view 'create' responsável por renderizar a página de criação de novos contatos
# Define a função da view 'create' que recebe a requisição HTTP do usuário
def create(request):
    # Armazena os dados enviados via POST (comumente usado para ativar a validação do token CSRF)
    post = request.POST 

    # Inicializa um dicionário vazio para armazenar as variáveis que serão enviadas ao HTML
    context = {

    }

    # Renderiza o template HTML e retorna a resposta formatada para o navegador do usuário
    return render(
        request,             # Passa o objeto de requisição original
        'contact/create.html', # Define o caminho do arquivo de template que será exibido
        context              # Envia o dicionário de contexto para o template
    )
