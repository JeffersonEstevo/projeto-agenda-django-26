# Importa atalhos essenciais: buscar objeto ou retornar 404, redirecionar rotas e renderizar templates HTML
# Importa a função redirect para redirecionar o usuário para outra página
from django.shortcuts import render, redirect

# Importa a classe ContactForm do arquivo 'forms.py' localizado na pasta 'contact'.
# Esse formulário geralmente gerencia os campos e a validação de uma página de contato.
from contact.forms import ContactForm

# Define a view 'create' responsável por renderizar a página de criação de novos contatos
# Define a função da view 'create' que recebe a requisição HTTP do usuário
def create(request):
    # Armazena os dados enviados via POST (comumente usado para ativar a validação do token CSRF)
    if request.method == 'POST':
        # Cria uma instância do formulário preenchida com os dados enviados pelo usuário
        form = ContactForm(request.POST)

        context = {  # Cria um dicionário chamado context para estruturar os dados que o template vai usar
            'form': ContactForm(request.POST)  # Cria o formulário e o preenche com os dados enviados pelo usuário via POST
        }  # Fecha a definição do dicionário context

        return render(  # Invoca a função render para construir e retornar a resposta HTTP com a página HTML processada
                request,  # Passa o objeto da requisição atual contendo os dados do navegador e do usuário
                'contact/create.html',  # Especifica o caminho relativo do template HTML que será renderizado na tela
                context  # Envia o dicionário de dados para que suas variáveis sejam usadas dentro do HTML
            )  # Fecha a execução da primeira função render

    context = {  # Cria ou sobrescreve o dicionário chamado context para estruturar os dados do template
        'form': ContactForm()  # Instancia uma versão nova, limpa e completamente vazia do formulário
    }  # Fecha a definição deste novo dicionário context

    # Verifica se todos os dados enviados são válidos e seguem as regras do formulário
    if form.is_valid():
        # Salva os dados validados no banco de dados (cria ou atualiza o registro)
        form.save()
        
        # Redireciona o navegador do usuário para a URL correspondente à rota 'contact:create'
        return redirect('contact:create')

    return render(  # Invoca novamente a função render para construir a resposta HTTP, agora com o formulário limpo
        request,  # Passa o objeto da requisição atual contendo os metadados do usuário
        'contact/create.html',  # Especifica o mesmo caminho relativo do template HTML que será exibido
        context  # Envia o dicionário de dados para dentro do HTML
    )  # Fecha a execução da segunda função render
