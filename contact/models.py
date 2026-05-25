# Importa o módulo models para criar as tabelas do banco de dados como classes Python
from django.db import models
# Importa o timezone para gerenciar datas considerando o fuso horário configurado
from django.utils import timezone

# id (primary key - automático no Django)
# first_name (string) last_name (string), phone (string)
# email (email), created_date (date), description (text)
# category (foreign key), show (boolean), owner (foreign key)
# picture (imagem)

# Cada classe que herda de models.Model vira uma tabela no seu banco de dados
class Contact(models.Model):
    # ATENÇÃO: O Django cria o campo 'id' automaticamente como chave primária,
    # por isso não precisamos declarar ele aqui no código.

    # Campo de texto curto para o primeiro nome. Limite de 50 caracteres. Obrigatório.
    first_name = models.CharField(max_length=50)
    
    # Campo de texto curto para o sobrenome. Limite de 50 caracteres. Obrigatório.
    last_name = models.CharField(max_length=50)
    
    # Campo de texto curto para o telefone. Usar CharField é ideal para aceitar (xx) xxxxx-xxxx.
    phone = models.CharField(max_length=50)
    
    # Campo especializado para e-mail. Valida automaticamente se o formato possui '@' e '.com'.
    # blank=True torna o preenchimento opcional no formulário/admin.
    email = models.EmailField(max_length=254, blank=True)
    
    # Campo de data e hora. default=timezone.now registra o momento exato da criação automaticamente.
    created_date = models.DateTimeField(default=timezone.now)
    
    # Campo de texto longo (sem limite estrito de caracteres) para a descrição do contato.
    # blank=True permite salvar o contato sem nenhuma descrição.
    description = models.TextField(blank=True)

    # Método mágico do Python que define a representação em texto do objeto
    def __str__(self):
        # Retorna o primeiro nome e o sobrenome combinados como uma única string
        # ESSENCIAL: É este retorno que o Django usa para dar nome ao contato no painel administrativo!
        return f'{self.first_name} {self.last_name}'
    