# path é a função padrão do Django usada para mapear uma URL para uma view
from django.urls import path
# Importa o arquivo views.py do próprio aplicativo contact para usar as funções
from contact import views 

# Define o namespace deste app para evitar conflitos de nomes em projetos grandes
app_name = 'contact'

# Lista de rotas específicas para as páginas do aplicativo de contatos
urlpatterns = [
    # Mapeia a raiz do app ('') para a função 'index' dentro de views.py
    # O 'name=index' serve para criar links dinâmicos no HTML usando {% url 'contact:index' %}
    path('', views.index, name='index'),

    # DEFINIÇÃO DA ROTA DINÂMICA:
    # 1. '<int:contact_id>/' -> Captura o valor digitado na URL (ex: /5/) e garante que ele seja um número inteiro (int).
    #                           O Django salva esse número em uma variável chamada 'contact_id'.
    # 2. views.contact       -> Define qual função do arquivo 'views.py' vai processar essa requisição.
    # 3. name='contact'      -> Dá um apelido para a rota. Permite chamar esta URL no template sem escrever o caminho fixo.
    path('<int:contact_id>/', views.contact, name='contact'),
]
