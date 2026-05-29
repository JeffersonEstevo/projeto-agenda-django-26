# Importa o módulo models para criar as tabelas do banco de dados como classes Python
from django.db import models
# Importa o timezone para gerenciar datas considerando o fuso horário configurado
from django.utils import timezone

# Importa o modelo padrão de Usuário do Django. Para usar owner
from django.contrib.auth.models import User

# id (primary key - automático no Django)
# first_name (string) last_name (string), phone (string)
# email (email), created_date (date), description (text)
# category (foreign key), show (boolean), owner (foreign key), picture (imagem)

# Depois 
# owner (foreign key)

# Classe que representa a tabela de Categorias (ex: Amigos, Família, Trabalho).
# Ela existe para que os contatos possam ser organizados em grupos dinâmicos.
class Category(models.Model):
    # A class Meta define os metadados (configurações de comportamento do modelo)
    # --- ORDENAÇÃO DE DADOS ---
    # Ordena as consultas do mais novo para o mais antigo (o '-' indica ordem decrescente)
    #ordering = ['-created_at']

    # --- BANCO DE DADOS ---
    # Altera o nome físico da tabela gerada no banco de dados SQL
    #db_table = 'tb_sistema_categorias'

    # --- REGRAS E VALIDAÇÕES ---
    # Bloqueia o banco: impede duas categorias com o mesmo 'slug' para o mesmo 'user'
    #unique_together = [['slug', 'user']]

    # --- REAPROVEITAMENTO (Descomente se for usar como modelo base) ---
    # abstract = True # Se for True, não cria tabela própria, serve apenas para herança
    class Meta:
        # --- EXIBIÇÃO NO DJANGO ADMIN ---
        # Define o nome amigável no singular para a interface do painel administrativo
        verbose_name = 'Category'
        # Define o nome amigável no plural (evita que o Django escreva 'Categorys')
        verbose_name_plural = 'Categories'

    # Campo de texto curto para o nome da categoria. Limite de 50 caracteres.
    # Cada linha criada nesta tabela representará uma categoria única no sistema.
    name = models.CharField(max_length=50)

    # Método que define como a categoria será exibida como texto no Admin do Django.
    # Sem isso, o Django exibiria "Category object (1)" em vez do nome real (ex: "Amigos").
    def __str__(self) -> str:
        return self.name


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

    # Campo booleano para controlar a exibição do contato. 
    # default=True faz com que novos contatos fiquem visíveis por padrão.
    show = models.BooleanField(default=True)

    # Campo especializado para upload de imagens (fotos, capturas de tela, etc.).
    # blank=True torna o preenchimento opcional, permitindo salvar o contato sem foto.
    # upload_to define o caminho de organização baseado na data atual do upload.
    # POR QUE USAR: O Django usará a pasta raiz de mídias (MEDIA_ROOT) combinada com 
    # este parâmetro. Isso significa que as imagens físicas serão salvas automaticamente 
    # na pasta 'media/pictures/ANO/MES/' (ex: media/pictures/2026/05/foto.jpg), evitando 
    # que milhares de arquivos fiquem jogados em uma única pasta e causem lentidão no servidor.
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    # RELACIONAMENTO (Chave Estrangeira / Foreign Key):
    # Vincula este contato a uma categoria específica da tabela Category.
    #
    # COMO FUNCIONA A RELAÇÃO (Muitos-para-Um / Many-to-One):
    # - Muitos contatos podem pertencer a uma mesma categoria (ex: 10 contatos na categoria "Trabalho").
    # - Cada contato individual só pode ter uma única categoria vinculada a ele por vez.
    #
    # EXPLICAÇÃO DOS PARÂMETROS:
    # - Category: Indica o modelo com o qual este contato está se relacionando.
    # - on_delete=models.SET_NULL: Se a categoria vinculada for apagada do banco de dados,
    #   o Django NÃO apagará o contato. Em vez disso, ele apenas limpará o campo deixando-o vazio.
    # - on_delete=models.CASCADE: Comportamento de exclusão em cascata. Se uma categoria for 
    #   apagada do banco de dados (ex: deletar a categoria "Trabalho"), o Django vai APAGAR 
    #   automaticamente todos os contatos que estavam vinculados a ela.
    # - blank=True: Torna o preenchimento opcional em formulários e no painel administrativo.
    # - null=True: Permite que a coluna aceite valores nulos (NULL) no banco de dados. 
    #   Isso é obrigatório para que o 'SET_NULL' funcione, permitindo contatos sem nenhuma categoria.
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    owner = models.ForeignKey(
        # Vincula o contato ao modelo de Usuário padrão do Django
        User,
        
        # Se o Usuário dono for deletado, o Django NÃO apaga o contato.
        # Em vez disso, ele limpa o campo mudando o valor para NULL no banco de dados.
        on_delete=models.SET_NULL,
        
        # Permite que o campo fique vazio em formulários do Django (como no Admin)
        blank=True, 
        
        # Permite que o campo grave o valor NULL (vazio) diretamente no banco de dados
        null=True
    )


    # Método mágico do Python que define a representação em texto do objeto
    def __str__(self):
        # Retorna o primeiro nome e o sobrenome combinados como uma única string
        # ESSENCIAL: É este retorno que o Django usa para dar nome ao contato no painel administrativo!
        return f'{self.first_name} {self.last_name}'
    