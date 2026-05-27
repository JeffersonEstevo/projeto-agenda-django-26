"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# django.contrib.admin traz a interface administrativa nativa do Django
from django.contrib import admin

# path define caminhos de URL; include permite conectar outras listas de URLs
from django.urls import path, include

#Importa a função auxiliar 'static', usada exclusivamente em ambiente de desenvolvimento.
# POR QUE USAR: O Django por padrão não serve arquivos de mídia (uploads) de forma automática.
# Essa função vincula as URLs dos arquivos aos seus caminhos reais na máquina, permitindo
# que você consiga visualizar as imagens enviadas pelos usuários diretamente no navegador.
from django.conf.urls.static import static

# Importa o objeto de configurações globais do Django para acessar as variáveis do projeto.
# POR QUE NÃO IMPORTAR DIRETO (de django.conf import settings): Você nunca deve importar 
# 'from meu_projeto import settings' diretamente por dois motivos críticos:
# 1. Sobrecarga de Ambientes: O objeto 'django.conf.settings' mescla as suas configurações 
#    padrão com as variáveis internas do próprio Django de forma dinâmica.
# 2. Portabilidade: Se você mudar o nome da pasta do projeto ou usar múltiplos arquivos de 
#    configuração (como settings_local.py e settings_prod.py), o import direto quebrará o código. 
#    O 'django.conf' garante que o Django sempre use o arquivo correto que está ativo na memória.
from django.conf import settings

# Lista principal que o Django consulta para rotear as requisições do navegador
urlpatterns = [
    # Redireciona a página inicial (vazia '') para as URLs do app 'contact'
    path('', include('contact.urls')),
    
    # Rota padrão para acessar o painel de administração (/admin/)
    path('admin/', admin.site.urls),
]

# Adiciona as rotas de mídia ao final da lista de URLs principais do seu projeto.
# POR QUE USAR: Instruirá o Django a escutar qualquer requisição feita no endereço do 'MEDIA_URL'
# (ex: /media/) e buscar o arquivo correspondente físico localizado dentro da pasta 'MEDIA_ROOT'.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Adiciona as rotas de arquivos estáticos (CSS, JS, imagens do layout) à lista de URLs.
# POR QUE USAR: Vincula o padrão de endereço web (STATIC_URL) à pasta física do disco (STATIC_ROOT).
# Isso permite que o servidor de desenvolvimento do Django encontre e carregue corretamente as 
# folhas de estilo e scripts no navegador enquanto você está construindo o site localmente.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
