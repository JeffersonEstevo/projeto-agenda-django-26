from django.contrib import admin
# Importa o arquivo 'models.py' localizado dentro da pasta (app) 'contact'
# Isso dá acesso à classe 'Contact' que representa a tabela no banco de dados
from contact import models

# O decorator avisa ao Django que a classe abaixo 
# controlará o modelo 'Contact' no painel administrativo do Django
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    # Define as colunas que aparecem na tabela de listagem no painel administrativo
    list_display = 'id', 'first_name', 'last_name', 'phone',
    # Define a ordenação padrão dos itens (o sinal de menos indica ordem decrescente)
    ordering = '-id'
    # Cria uma barra lateral para filtrar os registros por data
    # list_filter = 'created_date',
    # Adiciona uma barra de pesquisa para buscar por termos nesses campos específicos
    search_fields = 'id', 'first_name', 'last_name',
    # Ativa a paginação, exibindo no máximo 10 registros por página.
    list_per_page = 10
    # Define o limite máximo de itens exibidos se o usuário clicar em "Mostrar tudo" (evita travar o banco)
    list_max_show_all = 200
    # Permite editar estes campos diretamente na tabela de listagem, sem abrir o registro
    list_editable = 'first_name', 'last_name',
    # Transforma estes campos em links clicáveis para abrir o formulário de edição completa
    list_display_links = 'id', 'phone'
