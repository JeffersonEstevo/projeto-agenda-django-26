# render é uma função auxiliar que une um template HTML com dados para o navegador
from django.shortcuts import render

# Função que processa a requisição da página inicial
def index(request):
    # Retorna o arquivo HTML renderizado localizado na pasta de templates
    return render(
        request,             # O objeto da requisição HTTP obrigatório
        'contact/index.html', # Caminho do arquivo HTML que será exibido
    )