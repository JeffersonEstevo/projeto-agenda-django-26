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

# Lista principal que o Django consulta para rotear as requisições do navegador
urlpatterns = [
    # Redireciona a página inicial (vazia '') para as URLs do app 'contact'
    path('', include('contact.urls')),
    
    # Rota padrão para acessar o painel de administração (/admin/)
    path('admin/', admin.site.urls),
]
