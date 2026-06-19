# Importa a função do Django usada para renderizar páginas HTML enviando dados do back-end
# Importa a função utilitária do Django usada para redirecionar o usuário para outra URL ou página do site
from django.shortcuts import render, redirect

# Importa o formulário de registro personalizado que criamos anteriormente.
# Importa a classe do formulário 'RegisterUpdateForm' que está localizada dentro 
# do arquivo 'forms.py', o qual pertence ao app (aplicativo) chamado 'contact'.
from contact.forms import RegisterForm, RegisterUpdateForm

# Importa o framework de mensagens do Django para enviar notificações temporárias (ex: alertas de sucesso ou erro) ao usuário
# Importa os módulos de autenticação (login/logout) e o sistema de alertas/mensagens do Django
from django.contrib import messages, auth

# Importa o formulário padrão do Django para validação de usuário e senha
from django.contrib.auth.forms import AuthenticationForm 


# Define a função da view que vai gerenciar a página de cadastro do usuário
def register(request):
    # Cria uma instância limpa (vazia) do formulário para exibição inicial na página
    form = RegisterForm()

    # Verifica se o usuário enviou o formulário clicando no botão (método HTTP POST)
    if request.method == 'POST':
        # Recria o formulário, mas agora preenchido com os dados enviados pelo usuário
        form = RegisterForm(request.POST)

        # Executa as validações de segurança e regras dos campos (ex: senhas iguais)
        if form.is_valid():
            # Salva o novo usuário de forma segura no banco de dados se tudo estiver correto
            form.save()

            # Envia um alerta de sucesso temporário (flash message) para o usuário com o texto 'Usuário registrado'
            messages.success(request, 'Usuário registrado')

            # Interrompe a execução atual e redireciona o navegador do usuário para a página de login do app 'contact'
            # Redireciona imediatamente o navegador do usuário para a página de login
            return redirect('contact:login') 

    # Retorna a resposta HTTP renderizando o arquivo HTML na tela do navegador
    return render(
        # Passa o objeto do request para que o Django gerencie a sessão do usuário
        request,
        # Define o caminho do template HTML que será exibido (o seu arquivo register.html)
        'contact/register.html',
        # Envia a variável do formulário (com ou sem erros) para ser usada no HTML
        {
            'form': form
        }
    )

def user_update(request):
# Define uma função de View chamada 'user_update' que recebe o objeto 'request' da requisição HTTP.

    form = RegisterUpdateForm(instance=request.user)
    # Cria uma instância do formulário pré-preenchida com os dados atuais do usuário logado (GET padrão).

    if request.method != 'POST':
    # Verifica se o método de envio da requisição NÃO é do tipo POST (ou seja, se o usuário está apenas acessando a página).
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form
            }
        )
        # Renderiza a página HTML do formulário vazio/preenchido e encerra a execução deste bloco se não for POST.

    form = RegisterUpdateForm(data=request.POST, instance=request.user)
    # Recria o formulário, mas agora injetando os dados que o usuário preencheu no HTML (request.POST) e mantendo a referência do usuário atual.

    if not form.is_valid():
    # Executa todos os métodos de validação (clean, clean_email, etc.) e verifica se o formulário contém algum erro.
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form
            }
        )
        # Se houver erros, recarrega a mesma página HTML exibindo os alertas de validação para o usuário.

    form.save()
    # Executa o método save() customizado do formulário, criptografando a senha (se alterada) e salvando as modificações no banco de dados.
    
    return redirect('contact:user_update')
    # Redireciona o navegador de volta para a mesma página de atualização (evitando o reenvio de dados caso o usuário atualize a página).

# Define a função que controla a lógica da página de login, recebendo os dados da requisição HTTP
def login_view(request): 
    # Cria uma instância vazia do formulário de login para ser exibida quando a página carregar (GET)
    form = AuthenticationForm(request) 
    # Verifica se o usuário submeteu o formulário (clicou no botão para enviar os dados)
    if request.method == 'POST': 
        # Recria o formulário, mas agora preenchido com os dados (usuário/senha) enviados pelo POST
        form = AuthenticationForm(request, data=request.POST) 
        # Verifica se os campos foram preenchidos corretamente e se o usuário e senha existem/estão corretos
        if form.is_valid(): 
            # Recupera o objeto do usuário autenticado a partir dos dados validados do formulário
            user = form.get_user() 
            # Cria formalmente a sessão do usuário no navegador, conectando-o ao sistema
            auth.login(request, user) 
            # Salva uma mensagem temporária de sucesso para ser exibida na próxima página
            messages.success(request, 'Logado com sucesso!') 
            # Redireciona o usuário logado para a página inicial (index) do app contact
            return redirect('contact:index') 
        # Se o formulário for inválido (senha errada, etc), cria uma mensagem de erro
        messages.error(request, 'Login inválido') 

    return render( # Executado se a requisição for GET (página abrindo) ou se o POST falhar (erros no formulário)
        request, # Passa o objeto da requisição obrigatório para a renderização
        'contact/login.html', # Indica qual arquivo HTML (template) deve ser desenhado na tela do usuário
        {
            'form': form # Envia o formulário (com erros ou vazio) para dentro do HTML através do contexto
        }
    )

# Define a função responsável por desconectar o usuário do sistema
def logout_view(request):
    # Encerra a sessão do usuário atual, limpando os dados de autenticação do navegador 
    auth.logout(request) 
    # Redireciona o usuário de volta para a página de login após ele sair do sistema
    return redirect('contact:login') 
