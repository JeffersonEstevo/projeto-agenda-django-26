# Importa o utilitário de paginação do Django para dividir listas longas em várias páginas
from django.core.paginator import Paginator
# Importa o objeto Q para realizar consultas complexas no banco de dados (usando operadores OU/AND)
from django.db.models import Q
# Importa atalhos essenciais: buscar objeto ou retornar 404, redirecionar rotas e renderizar templates HTML
from django.shortcuts import get_object_or_404, redirect, render

# Importa o modelo de dados 'Contact' que representa a tabela de contatos no banco de dados
from contact.models import Contact


# Define a view 'create' responsável por renderizar a página de criação de novos contatos
def create(request):
    # Inicializa o dicionário de contexto que enviará dados e variáveis para o template HTML
    context = {

    }

    # Renderiza e retorna o arquivo HTML 'create.html', passando os dados do contexto
    return render(
        request,
        'contact/create.html',
        context
    )
