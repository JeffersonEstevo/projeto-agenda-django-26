# Importa o módulo de formulários do Django
from django import forms
# Importa a exceção usada para sinalizar erros de validação
from django.core.exceptions import ValidationError

# Importa o módulo 'models' que está na mesma pasta deste arquivo.
# Geralmente usado no Django ou FastAPI para acessar as tabelas do banco de dados.
from . import models

class ContactForm(forms.ModelForm):  # Declara a classe ContactForm herdando as funcionalidades de ModelForm do Django
    class Meta:  # Cria a classe interna Meta para configurar as opções do formulário
        model = models.Contact  # Define que o formulário será baseado no modelo de banco de dados chamado Contact
        fields = (  # Inicia a tupla que define quais campos do modelo serão usados
            'first_name',  # Inclui o campo do primeiro nome no formulário
            'last_name',  # Inclui o campo do sobrenome no formulário
            'phone',  # Inclui o campo do telefone no formulário
        )  # Fecha a tupla de especificação dos campos

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

