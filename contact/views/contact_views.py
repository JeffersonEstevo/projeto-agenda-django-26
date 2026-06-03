# render é uma função auxiliar que une um template HTML com dados para o navegador
# IMPORTAÇÃO: O get_object_or_404 é um atalho (shortcut) essencial do Django.
# Sem ele, você precisaria escrever um bloco 'try/except' com a exceção 'DoesNotExist' em cada View.
# 'redirect' -> Importa a função do Django usada para redirecionar o usuário para outra URL.
# Importante para controlar o fluxo de navegação do site (ex: enviar o usuário de volta para a Home).
from django.shortcuts import render, get_object_or_404, redirect

# Por que você precisa importar 'contact.models'?
# O Django trabalha com o padrão MVT (Model-View-Template). A sua View precisa buscar 
# os dados guardados no banco de dados para poder enviá-los ao template HTML. 
# A classe 'Contact' é a representação da sua tabela do banco de dados em código Python. 
# Sem essa importação, a View não saberia onde buscar as informações dos contatos.
from contact.models import Contact

# 'Q' -> Importa o objeto de consultas (Query) do Django. 
# Ele é fundamental para realizar buscas complexas usando o operador lógico "OU" (|), 
# permitindo filtrar dados por múltiplos campos simultaneamente no banco de dados.
from django.db.models import Q

# Importa a classe Paginator do Django para gerenciar a divisão de dados em páginas
from django.core.paginator import Paginator

# Função que processa a requisição da página inicial
def index(request):
    # .filter(show=True) -> Filtra os resultados. Só traz os contatos onde 
    # o campo 'show' é Verdadeiro (True).
    # .order_by('-id')   -> Ordena os dados. O sinal de menos '-' 
    # indica ordem decrescente (do ID maior para o menor / mais recentes primeiro).
    # [10:20]            -> Faz o fatiamento (Slicing). Cria uma paginação que 
    # .order_by('-id')[10:20]
    # pula os 10 primeiros registros e pega do 11º ao 20º.
    contacts = Contact.objects \
    .filter(show=True) \
    .order_by('-id')
    
    # Cria o paginador dividindo a lista total de contatos ('contacts') em grupos de 10 por página
    paginator = Paginator(contacts, 10)

    # Recupera o número da página atual a partir dos parâmetros de URL (ex: ?page=2)
    page_number = request.GET.get("page")

    # Busca os contatos específicos da página atual e cria o objeto final usado no template
    page_obj = paginator.get_page(page_number)

    # Exibe no terminal do servidor o comando SQL puro que o ORM do Django gerou para o banco de dados.
    # Útil para debugar e entender a performance da consulta.
    # print(contacts.query)

    # Um dicionário Python que serve como "ponte" de dados.
    # A chave em string 'contacts' será o nome da variável que o seu 
    # arquivo HTML (index.html) vai ler para exibir as informações.
    context = {
        'contacts': page_obj,
        'site_title': 'Contatos - '
    }
    
    # Retorna o arquivo HTML renderizado localizado na pasta de templates
    return render(
        request,              # O objeto da requisição HTTP obrigatório
        'contact/index.html', # Caminho do arquivo HTML que será exibido
        context
    )

# Função que processa a requisição da barra de pesquisa
def search(request):
    # Obtém o termo digitado pelo usuário na barra de pesquisa (o parâmetro 'q' do formulário GET).
    # .get('q', '') -> Se 'q' não existir (busca vazia), define uma string vazia como padrão.
    # .strip()      -> Remove espaços em branco desnecessários no início e no final do termo digitado.
    search_value = request.GET.get('q', '').strip()

    # Validação de Segurança/Experiência do Usuário:
    # Se o usuário não digitou nada ou apenas espaços, ele é redirecionado de volta para a página inicial.
    # Isso evita que o banco de dados faça buscas vazias desnecessárias.
    if search_value == '':
        return redirect('contact:index')

    # Consulta ao Banco de Dados (QuerySet):
    # .filter(show=True) -> Garante que a busca só retorne contatos marcados como visíveis.
    # .filter(Q(...) | Q(...)) -> Aplica o filtro de pesquisa. O símbolo pipe '|' funciona como o "OU" (OR) do SQL.
    # __icontains        -> O 'i' significa 'case-insensitive' (ignora maiúsculas/minúsculas). 
    #                       O 'contains' busca por partes do texto (ex: "ana" encontra "Ana", "Mariana" ou "Analu").
    # .order_by('-id')   -> Ordena os resultados encontrados exibindo os mais recentes primeiro.
    contacts = Contact.objects \
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) | # Busca no primeiro nome OR
            Q(last_name__icontains=search_value)  | # Busca no sobrenome OR
            Q(phone__icontains=search_value)      | # Busca no telefone OR
            Q(email__icontains=search_value)        # Busca no e-mail
        )\
        .order_by('-id')
    
    # Cria o paginador dividindo a lista total de contatos ('contacts') em grupos de 10 por página
    paginator = Paginator(contacts, 10)

    # Recupera o número da página atual a partir dos parâmetros de URL (ex: ?page=2)
    page_number = request.GET.get("page")

    # Busca os contatos específicos da página atual e cria o objeto final usado no template
    page_obj = paginator.get_page(page_number)

    # Dicionário de contexto que serve como "ponte" para enviar as variáveis para o HTML.
    # Reaproveita a variável 'contacts' exigida pelo seu template 'index.html'.
    # Modifica o título dinâmico da página para indicar que é um resultado de busca.
    # context = {
    #     'contacts': contacts,
    #     'site_title': 'Search - '
    # }

    # ANTES: Enviada a lista completa e sem tratamento de páginas para o template
    # context = {
    #     'contacts': contacts,
    #     'site_title': 'Search - '
    # }

    # DEPOIS: Passa o objeto paginado e atualiza o título para o idioma correto
    context = {
        # Altera 'contacts' pelo 'page_obj' que contém apenas os 10 registros da página atual
        'page_obj': page_obj,
        
        # Atualiza o título da aba do navegador para português e altera o termo de busca para o geral
        'site_title': 'Contatos - ',

        # Mantém o termo pesquisado no campo de busca para o usuário ver o que digitou
        'search_value': search_value,
    }

    # Retorna o arquivo HTML reaproveitando a mesma estrutura visual da página inicial,
    # porém exibindo apenas os registros filtrados pela pesquisa.
    return render(
        request,              # O objeto da requisição HTTP obrigatório
        'contact/index.html', # Caminho do arquivo HTML reaproveitado
        context               # Dados filtrados enviados para o template
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

    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    # RELAÇÃO COM O TEMPLATE (Dicionário de Contexto):
    # Empacota o objeto do banco de dados em um dicionário. 
    # A chave dinâmica 'contact' é exatamente a variável que o seu template 'contact.html' usa para acessar os dados (ex: {{ contact.first_name }}).
    context = {
        'contact': single_contact,
        'site_title': site_title
    }

    # RENDERIZAÇÃO FINAL:
    # Junta o pedido do usuário (request), o arquivo HTML ('contact/contact.html') e os dados (context).
    # O Django processa tudo isso no servidor e devolve uma página HTML completa e customizada para o navegador.
    return render(
        request,
        'contact/contact.html',
        context
    )
