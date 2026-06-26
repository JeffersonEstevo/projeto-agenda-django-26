# Configuração para deploy

## Primeiros passos

- Prepare o arquivo `local_settings.py` localmente.
- Crie o seu servidor Ubuntu 22.04 / 20.04 LTS.

Comando para gerar uma `SECRET_KEY` segura:

```bash
python -c "import string as s;from secrets import SystemRandom as SR;print(''.join(SR().choices(s.ascii_letters + s.digits + s.punctuation, k=64)));"
```

## Criando sua chave SSH (No Computador Local)

```bash
ssh-keygen -t ed25519 -C 'seu_email@gmail.com'
```

## No servidor Ubuntu

### Conectando via SSH

```bash
ssh ubuntu@IP_DO_SERVIDOR
```

### Comandos iniciais e dependências

```bash
sudo apt update -y && sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y

# Adicionar repositório para versões estáveis do Python
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.11 python3.11-venv -y

# Instalar ferramentas de infraestrutura (Nginx, Postgres, Git)
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git -y
```

### Configurando o Git no Servidor

```bash
git config --global user.name 'Seu Nome'
git config --global user.email 'seu_email@gmail.com'
git config --global init.defaultBranch main
```

Criando as pastas do projeto e do repositório remoto Git (*Bare*):

```bash
mkdir ~/agendarepo ~/agendaapp
```

Configurando os repositórios para o fluxo de Deploy:

```bash
cd ~/agendarepo
git init --bare
```

### Sincronizando o código (Do Computador Local para o Servidor)

No seu **computador local**, dentro da pasta do projeto Django, adicione o servidor como um repositório remoto e faça o envio:

```bash
# Corrija o caminho para a pasta remota exata do servidor
git remote add agenda-prod ubuntu@IP_DO_SERVIDOR:~/agendarepo
git push agenda-prod main
```

De volta ao **servidor Ubuntu**, puxe o código para a pasta onde a aplicação vai rodar:

```bash
cd ~/agendaapp
git init
git remote add localrepo ~/agendarepo
git pull localrepo main
```

## Configurando o PostgreSQL

```bash
sudo -u postgres psql
```

Dentro do terminal interativo do PostgreSQL (`postgres=#`), execute:

```sql
CREATE ROLE usuario_agenda WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'senha_usuario_agenda';
CREATE DATABASE projeto_agenda WITH OWNER usuario_agenda;
GRANT ALL PRIVILEGES ON DATABASE projeto_agenda TO usuario_agenda;
\q
```

Reinicie o banco de dados para aplicar:

```bash
sudo systemctl restart postgresql
```

## Criando o local_settings.py no servidor

Crie o arquivo de configurações de produção dentro da pasta de configurações do Django:

```bash
nano ~/agendaapp/project/local_settings.py
```

Cole e ajuste as variáveis. Certifique-se de preencher a senha idêntica à do banco e definir `DEBUG = False`:

```python
SECRET_KEY = 'SUA_CHAVE_SECRETA_GERADA'
DEBUG = False
ALLOWED_HOSTS = ['IP_DO_SEU_SERVIDOR', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projeto_agenda',
        'USER': 'usuario_agenda',
        'PASSWORD': 'senha_usuario_agenda',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Configurações cruciais para que o Nginx localize os arquivos de estilo
STATIC_URL = '/static/'
STATIC_ROOT = '/home/ubuntu/agendaapp/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ubuntu/agendaapp/media/'
```

## Configurando o Ambiente Virtual e Django

```bash
cd ~/agendaapp
python3.11 -m venv venv
source venv/bin/activate

# Atualizar gerenciador e instalar dependências do projeto
pip install --upgrade pip
pip install django pillow gunicorn psycopg faker

# Comandos do banco de dados e arquivos
python manage.py migrate
python manage.py collectstatic  # Digite 'yes' para consolidar os arquivos na pasta static/
python manage.py createsuperuser
```

## Configuração do Processo com Gunicorn

O Gunicorn atuará como o servidor de aplicação WSGI, traduzindo as requisições web do Nginx para o código Python do Django.

### 1. Criação do arquivo de comandos
Crie um arquivo local ou uma pasta de anotações chamada `comandos/gunicorn.txt` para mapear o arquivo de serviço do Linux (`Systemd`).

**Importante:** Substitua as variáveis de acordo com os seguintes dados:
* `__GUNICORN_FILE_NAME__` = nome do projeto/soquete [`agenda`]
* `__YOUR_USER__` = usuário do sistema operacional no servidor [`ubuntu`]
* `__APP_ROOT_NAME__` = caminho da pasta principal do projeto Django [`agendaapp`]
* `__WSGI_FOLDER_NAME__` = pasta que contém o arquivo `wsgi.py` [`project`]

### 2. Criação dos arquivos de configuração no Sistema (`Systemd`)

Crie o arquivo do Soquete (`.socket`):
```bash
sudo nano /etc/systemd/system/agenda.socket
```
Cole a estrutura de soquete padrão:
```ini
[Unit]
Description=agenda socket

[Socket]
ListenStream=/run/agenda.socket

[Install]
WantedBy=sockets.target
```

Crie o arquivo do Serviço (.service):
```bash
sudo nano /etc/systemd/system/agenda.service
```
Cole a configuração do serviço apontando para o seu ambiente virtual (`venv`) e executando o Gunicorn:
```ini
[Unit]
Description=agenda daemon
Requires=agenda.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/agendaapp
ExecStart=/home/ubuntu/agendaapp/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/agenda.socket \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Ativação e Testes do Gunicorn
Ative e inicie os serviços no Linux:
```bash
sudo systemctl start agenda.socket
sudo systemctl enable agenda.socket
```

Execute a validação dos processos:
```bash
# Checando o status do soquete
sudo systemctl status agenda.socket

# Testando se o soquete responde a requisições internas HTTP
curl --unix-socket /run/agenda.socket localhost

# Verificando se o serviço principal foi ativado pela requisição do curl
sudo systemctl status agenda
```

## Configurando o Nginx para receber requisições HTTP

O Nginx vai atuar como o Servidor Web Proxy Reverso, recebendo conexões na porta 80 e servindo os arquivos estáticos diretamente por questões de performance.

### 1. Preparação dos arquivos de configuração
Mantenha um modelo salvo em `comandos/nginx.txt`. No servidor, delete a configuração padrão de boas-vindas para desocupar a porta 80:

```bash
cd /etc/nginx/sites-enabled/
sudo rm -f default

cd ../sites-available/
sudo nano agenda
```

### 2. Escrita do bloco Server do Nginx
Cole o conteúdo de configuração do proxy reverso. 

**Importante:** Substitua as tags conforme as diretrizes abaixo (Lembre-se de adicionar a barra `/` ao final de cada caminho de `alias` para evitar erros de renderização de CSS):
* `__YOUR_DOMAIN_OR_IP__` = O endereço IP ou domínio do servidor [`192.168.1.70`]
* `__APP_ABSOLUTE_PATH__` = Caminho raiz do projeto [`/home/ubuntu/agendaapp/`]
* `__STATIC_ABSOLUTE_PATH__` = Local dos estáticos coletados (**Com barra no final!**) [`/home/ubuntu/agendaapp/static/`]
* `__MEDIA_ABSOLUTE_PATH__` = Local dos arquivos de mídia enviados por usuários (**Com barra no final!**) [`/home/ubuntu/agendaapp/media/`]
* `__GUNICORN_FILE_NAME__` = Nome do soquete definido anteriormente [`agenda`]

Exemplo estruturado do bloco:
```nginx
server {
    listen 80;
    server_name 192.168.1.70;

    location /static/ {
        autoindex on;
        alias /home/ubuntu/agendaapp/static/;
    }

    location /media/ {
        autoindex on;
        alias /home/ubuntu/agendaapp/media/;
    }

    location / {
        proxy_pass http://unix:/run/agenda.socket;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
```

### 3. Linkagem de pastas e liberação de permissão de leitura
No Nginx, a pasta `sites-available` guarda os arquivos criados e a pasta `sites-enabled` contém links simbólicos que ativam esses arquivos.

```bash
# Criar o link simbólico mapeando o arquivo para a pasta de ativação
sudo ln -s /etc/nginx/sites-available/agenda /etc/nginx/sites-enabled/

# Verificar se o link foi criado com sucesso
cd /etc/nginx/sites-enabled/
ls -l

# Liberar permissão de travessia na pasta /home/ubuntu para que o Nginx consiga ler a pasta static
sudo chmod 755 /home/ubuntu

# Testar se a sintaxe do Nginx não possui erros
sudo nginx -t

# Reiniciar o Nginx para aplicar todas as configurações
sudo systemctl restart nginx
```

## Permitir arquivos maiores no nginx

```bash
sudo nano /etc/nginx/nginx.conf
```

Adicione dentro do bloco `http { ... }`:

```nginx
client_max_body_size 30M;
```

Valide e reinicie uma última vez:
```bash
sudo nginx -t
sudo systemctl restart nginx
```