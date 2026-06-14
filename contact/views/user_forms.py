# Importa a função do Django usada para renderizar páginas HTML enviando dados do back-end
from django.shortcuts import render

# Importa o formulário de registro personalizado que criamos anteriormente
from contact.forms import RegisterForm


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
