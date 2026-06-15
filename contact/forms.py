# Importa o módulo de formulários do Django
from django import forms
# Importa a exceção usada para sinalizar erros de validação
from django.core.exceptions import ValidationError

# Importa o módulo 'models' que está na mesma pasta deste arquivo.
# Geralmente usado no Django ou FastAPI para acessar as tabelas do banco de dados.
from . import models

# Importa o formulário padrão de criação de usuário do sistema de autenticação do Django
from django.contrib.auth.forms import UserCreationForm

# Importa o modelo User nativo do sistema de autenticação do Django.
# Este modelo já possui campos padrão como username, password, email, first_name e last_name.
from django.contrib.auth.models import User

class ContactForm(forms.ModelForm):  # Declara a classe ContactForm herdando as funcionalidades de ModelForm do Django
    # Cria o campo 'picture' manualmente como um texto obrigatório
    picture = forms.ImageField(
        # Define o elemento HTML do campo (um botão para envio de arquivo)
        widget=forms.FileInput(
            # Adiciona atributos direto na tag HTML do campo
            attrs={
                # Restringe a seleção do usuário para aceitar apenas arquivos de imagem
                'accept': 'image/*',
            }
        )
    )

    class Meta:  # Cria a classe interna Meta para configurar as opções do formulário
        model = models.Contact  # Define que o formulário será baseado no modelo de banco de dados chamado Contact
        fields = (  # Inicia a tupla que define quais campos do modelo serão usados
            'first_name',  # Inclui o campo do primeiro nome no formulário
            'last_name',  # Inclui o campo do sobrenome no formulário
            'phone',  # Inclui o campo do telefone no formulário
            'email',  # Inclui o campo do email no formulário
            'description', # Inclui o campo de descrição no formulário
            'category', # Inclui o campo de categoria no formulário
            'picture',  # Inclui o campo de picture no formulário
        )  # Fecha a tupla de especificação dos campos

    def clean(self):  # Define o método clean para realizar validações personalizadas no formulário
        # Armazena o dicionário de dados já limpos e validados pelo Django nesta variável local
        cleaned_data = self.cleaned_data
        # Busca de forma segura o valor do campo 'first_name' dentro do dicionário de dados limpos
        first_name = cleaned_data.get('first_name')
        # Busca de forma segura o valor do campo 'last_name' dentro do dicionário de dados limpos
        last_name = cleaned_data.get('last_name')

        # Compara se o texto digitado no primeiro nome é exatamente igual ao sobrenome
        if first_name == last_name:
            # Cria a instância do erro com a mensagem de alerta e o código de identificação
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            # Vincula e exibe essa mensagem de erro especificamente no campo do primeiro nome
            self.add_error('first_name', msg)
            # Vincula e exibe a mesma mensagem de erro também no campo do sobrenome
            self.add_error('last_name', msg)

        return super().clean()  # Executa e retorna a lógica de validação padrão da classe mãe do Django

    # Declara o método que o Django executa automaticamente para validar o campo 'first_name'
    def clean_first_name(self):
        # Recupera com segurança o valor já pré-validado do campo 'first_name' no dicionário de dados limpos
        first_name = self.cleaned_data.get('first_name')

        # Avalia se a string digitada pelo usuário no formulário é exatamente igual a 'ABC'
        if first_name == 'ABC':
            # Registra um erro de validação vinculado especificamente ao campo 'first_name'
            self.add_error(
                'first_name', # Define o nome do campo do formulário que receberá o erro
                ValidationError( # Instancia o objeto de erro do Django
                    'Veio do add_error', # Define o texto da mensagem que será exibida na tela
                    code='invalid' # Categoriza o tipo do erro com o identificador 'invalid'
                )
            )

        # Devolve o valor do campo (tratado) para o formulário, garantindo que ele não fique vazio/None
        return first_name


# Cria uma classe customizada para o formulário de registro, herdando os recursos do Django
# Define um formulário de registro personalizado herdando do UserCreationForm do Django
class RegisterForm(UserCreationForm):
    # Campo obrigatório para o primeiro nome, exigindo no mínimo 3 caracteres
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    # Campo obrigatório para o sobrenome, exigindo no mínimo 3 caracteres
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    # Campo para o endereço de e-mail (valida o formato @ automaticamente)
    email = forms.EmailField()

    # Configurações de metadados do formulário
    class Meta:
        # Vincula este formulário ao modelo de usuário padrão do Django
        model = User
        # Define a ordem e quais campos serão exibidos no formulário final
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    # Método de validação customizado para o campo 'email'
    def clean_email(self):
        # Captura o e-mail digitado pelo usuário (já limpo pelo Django)
        email = self.cleaned_data.get('email')

        # Consulta o banco de dados para verificar se o e-mail já está cadastrado
        if User.objects.filter(email=email).exists():
            # Se o e-mail já existir, adiciona uma mensagem de erro específica ao campo
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        # Retorna o e-mail (válido ou com erro associado) para o fluxo do formulário
        return email
    