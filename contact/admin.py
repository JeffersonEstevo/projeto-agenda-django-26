from django.contrib import admin
# Importa o arquivo 'models.py' localizado dentro da pasta (app) 'contact'
# Isso dá acesso à classe 'Contact' que representa a tabela no banco de dados
from contact import models

# O decorator avisa ao Django que a classe abaixo 
# controlará o modelo 'Contact' no painel administrativo do Django
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    # Pass indica um bloco vazio por enquanto, onde entrarão as configurações visuais
    pass
