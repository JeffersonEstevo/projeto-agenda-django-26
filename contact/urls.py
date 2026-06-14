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
    # path('<int:contact_id>/', views.contact, name='contact'),

    # DEFINIÇÃO DA ROTA DE PESQUISA:
    # 1. 'search/'      -> Define o caminho estático da URL no navegador (ex: ://seudominio.com).
    #                      Quando o usuário enviar uma busca, os termos irão após a barra (ex: /search/?q=termo).
    # 2. views.search   -> Define que a função 'search' dentro do arquivo 'views.py' vai processar essa requisição.
    # 3. name='search'  -> Dá um apelido para a rota. Permite gerar o link dinamicamente nos formulários HTML 
    #                      usando a tag '{% url "contact:search" %}' sem precisar fixar o caminho no código.
    path('search/', views.search, name='search'),


    # contact (CRUD) - Definição das rotas para o gerenciamento completo de contatos
    # 1. Rota de Leitura (Read): Exibe os detalhes de um contato específico com base no ID
    # path('contact/<int:contact_id>/detail/', views.contact, name='contact'),
    # 2. Rota de Criação (Create): Exibe o formulário e processa o cadastro de novos contatos
    # path('contact/create/', views.contact, name='contact'),
    # 3. Rota de Atualização (Update): Exibe o formulário de edição e salva as alterações do contato
    # path('contact/<int:contact_id>/update/', views.contact, name='contact'),
    # 4. Rota de Deleção (Delete): Processa a exclusão permanente de um contato específico
    # path('contact/<int:contact_id>/delete/', views.contact, name='contact'),

    # contact (CRUD) - Definição das rotas para o gerenciamento completo de contatos
    # 1. Rota de Leitura (Read): Exibe os detalhes de um contato específico com base no ID
    path('contact/<int:contact_id>', views.contact, name='contact'),
    # 2. Rota de Criação (Create): Exibe o formulário e processa o cadastro de novos contatos
    path('contact/create/', views.create, name='create'),
    # 3. Rota de Atualização (Update): Exibe o formulário de edição e salva as alterações do contato
    path('contact/<int:contact_id>/update/', views.update, name='update'),
    # 4. Rota de Deleção (Delete): Processa a exclusão permanente de um contato específico
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'),

    # user
    path('user/create/', views.register, name='register'),
]

