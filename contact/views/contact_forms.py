# Importa o utilitário de paginação do Django para dividir listas longas em várias páginas
from django.core.paginator import Paginator
# Importa o objeto Q para realizar consultas complexas no banco de dados (usando operadores OU/AND)
from django.db.models import Q
# Importa atalhos essenciais: buscar objeto ou retornar 404, redirecionar rotas e renderizar templates HTML
from django.shortcuts import get_object_or_404, redirect, render

# Importa o modelo de dados 'Contact' que representa a tabela de contatos no banco de dados
from contact.models import Contact

# Importa tipos do Python para dicas de tipagem (não utilizados neste trecho)
from typing import Any, Dict
# Importa o módulo de formulários do Django
from django import forms
# Importa a exceção usada para sinalizar erros de validação
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):  # Declara a classe ContactForm herdando as funcionalidades de ModelForm do Django
    class Meta:  # Cria a classe interna Meta para configurar as opções do formulário
        model = Contact  # Define que o formulário será baseado no modelo de banco de dados chamado Contact
        fields = (  # Inicia a tupla que define quais campos do modelo serão usados
            'first_name',  # Inclui o campo do primeiro nome no formulário
            'last_name',  # Inclui o campo do sobrenome no formulário
            'phone',  # Inclui o campo do telefone no formulário
        )  # Fecha a tupla de especificação dos campos

    def clean(self):  # Define o método clean para realizar validações personalizadas no formulário
        cleaned_data = self.cleaned_data  # Recupera o dicionário com os dados que já foram validados individualmente

        self.add_error(  # Registra um erro de validação específico no formulário
            'first_name',  # Vincula o erro diretamente ao campo 'first_name'
            ValidationError(  # Instancia uma exceção de erro de validação do Django
                'Mensagem de erro',  # Define o texto explicativo do primeiro erro
                code='invalid'  # Define o código identificador da falha ('invalid')
            )  # Fecha a instância do primeiro ValidationError
        )  # Fecha a execução do primeiro add_error
        
        self.add_error(  # Registra um segundo erro de validação no formulário
            'first_name',  # Vincula este novo erro também ao campo 'first_name'
            ValidationError(  # Instancia uma nova exceção de erro de validação
                'Mensagem de erro 2',  # Define o texto explicativo do segundo erro
                code='invalid'  # Define o código identificador desta segunda falha
            )  # Fecha a instância do segundo ValidationError
        )  # Fecha a execução do segundo add_error

        return super().clean()  # Executa e retorna a lógica de validação padrão da classe mãe do Django

# Define a view 'create' responsável por renderizar a página de criação de novos contatos
# Define a função da view 'create' que recebe a requisição HTTP do usuário
def create(request):
    # Armazena os dados enviados via POST (comumente usado para ativar a validação do token CSRF)
    if request.method == 'POST':
        print()
        print(request.method)
        print(request.POST.get('first_name'))
        print(request.POST.get('last_name'))
        print()

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

    return render(  # Invoca novamente a função render para construir a resposta HTTP, agora com o formulário limpo
        request,  # Passa o objeto da requisição atual contendo os metadados do usuário
        'contact/create.html',  # Especifica o mesmo caminho relativo do template HTML que será exibido
        context  # Envia o dicionário de dados para dentro do HTML
    )  # Fecha a execução da segunda função render
