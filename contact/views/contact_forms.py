# Importa atalhos essenciais: buscar objeto ou retornar 404, redirecionar rotas e renderizar templates HTML
from django.shortcuts import get_object_or_404, redirect, render
# Permite descobrir a URL real de uma rota a partir do "nome" que você deu a ela no arquivo urls.py
from django.urls import reverse
# Importa a classe (modelo) que representa a tabela de contatos no banco de dados
from contact.models import Contact
# Importa a classe ContactForm do arquivo 'forms.py' localizado na pasta 'contact'
from contact.forms import ContactForm


def create(request):
    """View responsável por exibir e processar a criação de um novo contato."""
    # Define dinamicamente a URL de destino para onde o formulário enviará os dados (ele mesmo)
    form_action = reverse('contact:create')
    
    # Se o usuário clicou no botão de enviar (submeteu o formulário)
    if request.method == 'POST':
        # Cria uma instância do formulário preenchida com os dados que vieram do navegador
        # e com os arquivos de upload, como fotos e documentos (request.FILES)
        form = ContactForm(request.POST, request.FILES)

        # Se o formulário for inválido, o código continua aqui e renderiza a página exibindo os erros
        context = {
            'form': form,
            'form_action': form_action,
        }

        # Se todos os campos forem preenchidos corretamente de acordo com as regras do formulário
        if form.is_valid():
            # Salva o novo contato no banco de dados
            contact = form.save()
            # REDIRECIONAMENTO CRÍTICO: Envia o usuário para a página de edição do contato criado.
            # Isso limpa a requisição POST do navegador, impedindo que o usuário crie o contato 
            # duplicado caso aperte F5 ou recarregue a página.
            return redirect('contact:update', contact_id=contact.pk)

        
        return render(request, 'contact/create.html', context)

    # Se o método for GET (usuário acabou de entrar na página), exibe o formulário totalmente limpo
    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }
    return render(request, 'contact/create.html', context)


def update(request, contact_id):
    """View responsável por buscar um contato existente, exibir seus dados e salvar alterações."""
    # Busca o contato pelo ID (pk). Se não existir ou se show=False, joga o usuário direto para a tela 404
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    
    # Define dinamicamente a URL de edição passando o ID do contato atual como argumento (ex: '/contact/update/5/')
    form_action = reverse('contact:update', args=(contact_id,))

    # Se o usuário clicou em salvar as alterações do contato
    if request.method == 'POST':
        # Preenche o formulário com os novos dados enviados pelo POST, 
        # mas vincula ao objeto 'contact' antigo para que o Django saiba que deve ATUALIZAR e não criar um novo.
        # e com os arquivos de upload, como fotos e documentos (request.FILES)
        form = ContactForm(request.POST, request.FILES, instance=contact)

        # Se a validação falhar (ex: digitou algo errado), monta o contexto com os erros para o usuário corrigir
        context = {
            'form': form,
            'form_action': form_action,
        }

        # Se os novos dados forem válidos
        if form.is_valid():
            # Atualiza o registro existente no banco de dados
            contact = form.save()
            # Redireciona para si mesmo (página de update). Isso atualiza a página de forma limpa, 
            # exibe os dados salvos e previne reenvios acidentais de dados.
            return redirect('contact:update', contact_id=contact.pk)

        
        return render(request, 'contact/create.html', context)

    # Se o método for GET (usuário acabou de entrar na página para editar), 
    # joga os dados atuais do contato buscado do banco de dados para dentro dos campos do formulário
    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }
    return render(request, 'contact/create.html', context)

# Controller/View responsável por gerenciar a exclusão segura de um contato
def delete(request, contact_id):
    # Busca o contato pelo ID (pk) se ele estiver marcado como visível (show=True).
    # Retorna um erro 404 (Página não encontrada) caso o contato não exista ou esteja oculto.
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True
    )
    
    # Captura o valor do campo oculto 'confirmation' enviado via POST pelo formulário.
    # Se o campo não for enviado (ex: primeiro clique ou acesso via GET), define 'no' como padrão.
    confirmation = request.POST.get('confirmation', 'no')

    # Se o valor capturado for 'yes', significa que o usuário confirmou a ação no segundo clique
    if confirmation == 'yes':
        # Remove o contato definitivamente do banco de dados
        contact.delete()
        # Redireciona o usuário de volta para a página inicial (lista de contatos)
        return redirect('contact:index')

    # Caso o usuário ainda não tenha confirmado ('no'), recarrega a página atual do contato
    # enviando a variável 'confirmation' para o template alternar o botão para "Confirma?"
    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
