# render é uma função auxiliar que une um template HTML com dados para o navegador
# IMPORTAÇÃO: O get_object_or_404 é um atalho (shortcut) essencial do Django.
# Sem ele, você precisaria escrever um bloco 'try/except' com a exceção 'DoesNotExist' em cada View.
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
# Por que você precisa importar 'contact.models'?
# O Django trabalha com o padrão MVT (Model-View-Template). A sua View precisa buscar 
# os dados guardados no banco de dados para poder enviá-los ao template HTML. 
# A classe 'Contact' é a representação da sua tabela do banco de dados em código Python. 
# Sem essa importação, a View não saberia onde buscar as informações dos contatos.
from contact.models import Contact

# Função que processa a requisição da página inicial
def index(request):
    # .filter(show=True) -> Filtra os resultados. Só traz os contatos onde 
    # o campo 'show' é Verdadeiro (True).
    # .order_by('-id')   -> Ordena os dados. O sinal de menos '-' 
    # indica ordem decrescente (do ID maior para o menor / mais recentes primeiro).
    # [10:20]            -> Faz o fatiamento (Slicing). Cria uma paginação que 
    # pula os 10 primeiros registros e pega do 11º ao 20º.
    contacts = Contact.objects \
    .filter(show=True) \
    .order_by('-id')[10:20]
    

    # Exibe no terminal do servidor o comando SQL puro que o ORM do Django gerou para o banco de dados.
    # Útil para debugar e entender a performance da consulta.
    # print(contacts.query)

    # Um dicionário Python que serve como "ponte" de dados.
    # A chave em string 'contacts' será o nome da variável que o seu 
    # arquivo HTML (index.html) vai ler para exibir as informações.
    context = {
        'contacts': contacts,
    }
    
    # Retorna o arquivo HTML renderizado localizado na pasta de templates
    return render(
        request,              # O objeto da requisição HTTP obrigatório
        'contact/index.html', # Caminho do arquivo HTML que será exibido
        context
    )

def contact(request, contact_id):
    # RELAÇÃO COM A URL: O parâmetro 'contact_id' vem diretamente da rota definida no arquivo 'urls.py'
    # (ex: path('<int:contact_id>/', views.contact, name='contact')). O Django captura o número da URL e joga aqui.

    # ESTA LINHA FOI SUBSTITUÍDA:
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    # O método acima retornaria 'None' se o contato não existisse, o que poderia gerar erros na renderização do template.

    # NOVA ABORDAGEM COM SEGURANÇA:
    # Busca no banco de dados o contato que possui a Chave Primária (pk) igual ao 'contact_id' recebido.
    # Adiciona a regra 'show=True', garantindo que contatos ocultos não sejam exibidos.
    # Se o contato não for encontrado ou estiver oculto, o Django interrompe a execução e retorna um erro 404 (Página não encontrada).
    single_contact = get_object_or_404(
        Contact, pk=contact_id, show=True
    )

    # RELAÇÃO COM O TEMPLATE (Dicionário de Contexto):
    # Empacota o objeto do banco de dados em um dicionário. 
    # A chave dinâmica 'contact' é exatamente a variável que o seu template 'contact.html' usa para acessar os dados (ex: {{ contact.first_name }}).
    context = {
        'contact': single_contact,
    }

    # RENDERIZAÇÃO FINAL:
    # Junta o pedido do usuário (request), o arquivo HTML ('contact/contact.html') e os dados (context).
    # O Django processa tudo isso no servidor e devolve uma página HTML completa e customizada para o navegador.
    return render(
        request,
        'contact/contact.html',
        context
    )
