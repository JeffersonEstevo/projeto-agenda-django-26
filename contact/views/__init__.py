# O '.' indica uma importação relativa. Significa: "procure o módulo 'contact_views' 
# dentro deste mesmo pacote/pasta em que o arquivo __init__.py está localizado".
from .contact_views import *
from .contact_forms import *

# 1. Por que importar assim?
# Isso cria um pacote de views. Em vez de ter um único arquivo 'views.py' com milhares 
# de linhas, você divide suas lógicas em arquivos menores e mais fáceis de manter.

# 2. O que o '*' faz?
# O asterisco importa TUDO o que é público (todas as funções e classes definidas em 
# 'contact_views.py'). Isso significa que, ao importar o pacote inteiro no seu 'urls.py', 
# as views estarão acessíveis diretamente, como se estivessem no arquivo original.

# 3. Qual o efeito prático no 'urls.py'?
# Quando você for configurar suas rotas (URLs), você poderá fazer algo como:
# from . import views
# path('contato/', views.NomeDaSuaView.as_view(), name='contato')
# O Django enxerga a pasta 'views' como se fosse um único arquivo por causa deste __init__.py.
