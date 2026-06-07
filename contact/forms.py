# Importa o módulo de formulários do Django
from django import forms
# Importa a exceção usada para sinalizar erros de validação
from django.core.exceptions import ValidationError

# Importa o módulo 'models' que está na mesma pasta deste arquivo.
# Geralmente usado no Django ou FastAPI para acessar as tabelas do banco de dados.
from . import models

class ContactForm(forms.ModelForm):  # Declara a classe ContactForm herdando as funcionalidades de ModelForm do Django
    # Cria o campo 'first_name' manualmente como um texto obrigatório
    first_name = forms.CharField(
        # Define o elemento HTML do campo (uma caixa de texto simples)
        widget=forms.TextInput(
            # Adiciona atributos direto na tag HTML do campo
            attrs={
                # Define as classes CSS para estilizar o campo na tela
                'class': 'classe-a classe-b',
                # Coloca o texto de dica que some ao digitar
                'placeholder': 'Aqui veio do init',
            }
        ),
        # Altera o texto da etiqueta (label) que fica ao lado ou acima do campo
        label='Primeiro Nome',
        # Adiciona uma pequena frase de instrução logo abaixo do campo
        help_text='Texto de ajuda para seu usuário',
    )

    # Método construtor que roda toda vez que o formulário é criado na memória
    def __init__(self, *args, **kwargs):
        # Executa a inicialização padrão do Django para carregar os campos de forma correta
        super().__init__(*args, **kwargs)

        # O trecho abaixo está comentado (não roda), mas serve para alterar o campo via código:
        # self.fields['first_name'].widget.attrs.update({
        #     'class': 'classe-a classe-b',
        #     'placeholder': 'Aqui veio do init',
        # })

    class Meta:  # Cria a classe interna Meta para configurar as opções do formulário
        model = models.Contact  # Define que o formulário será baseado no modelo de banco de dados chamado Contact
        fields = (  # Inicia a tupla que define quais campos do modelo serão usados
            'first_name',  # Inclui o campo do primeiro nome no formulário
            'last_name',  # Inclui o campo do sobrenome no formulário
            'phone',  # Inclui o campo do telefone no formulário
        )  # Fecha a tupla de especificação dos campos

        # O dicionário 'widgets' serve para customizar a renderização HTML de cada campo
        # widgets = {
        #     # Altera as propriedades visuais do campo 'first_name'
        #     'first_name': forms.TextInput(
        #         # O 'attrs' (atributos) injeta propriedades diretamente na tag HTML <input>
        #         attrs={
        #             # Adiciona classes CSS para estilizar o campo na página (ex: para usar Bootstrap)
        #             'class': 'classe-a classe-b',
                    
        #             # Adiciona uma frase cinza de dica que some quando o usuário começa a digitar
        #             'placeholder': 'Escreva aqui',
        #         }
        #     )
        # }

    def clean(self):  # Define o método clean para realizar validações personalizadas no formulário
        # cleaned_data = self.cleaned_data  # Recupera o dicionário com os dados que já foram validados individualmente

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

