# Dia 2

Olá, esse será o dia 2 do nosso workshop básico, nele iremos:


* Subir um Gitlab
* Testar nosso webhook atual
* Autenticar nosso Webhook
* Criando um webhook para Interagir com Gitlab
* Zappa
* Fazendo Deploy na AWS


## Gitlab

Bom sem segredos nessa parte, iremos subir um Gitlab para podermos interagir com ele, na pasta do dia 2 tem um arquivo chamado: docker-compose.yml 

Antes de executar o compose exporte a variável:

```
GITLAB_HOME
```

Para o lugar que você deseja gravar os volumes, no meu caso:

```
export GITLAB_HOME=/home/gitlab/
```

Abra seu terminal navegue até a pasta do dia 2 aonde o docker-compose.yml se encontra e digite o seguinte:

```
docker-compose up -d
```

OPCIONAL:

Se você quiser facilitar na hora de entrar no gitlab vamos adicionar uma entry no /etc/hosts:

Com bash:
```
echo $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dia2_web_1) gitlab.webhook | sudo tee -a /etc/hosts 
```
Se você quiser fazer na mão:

* Abra o /etc/hosts
* Execute o comando: 
```
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dia2_web_1
```
* Adicione a linha: <**_IP_**> gitlab.webhook

No meu caso ficou:

```
172.17.0.2 gitlab.webhook
```


Agora acesse:

http://gitlab.webhook


Já que não temos certificado usando o Chrome no meu caso clique em avançado e aceite proceder ao site mesmo sem certificado.

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/cert1.png?raw=true "Webhook")

Agora você irá preencher a senha do root caso seja a primeira vez que esteja subindo o Gitlab, coloque uma senha e depois logue como usuário: **_root_**

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/signin.png?raw=true "Webhook")

Beleza!

Agora estamos dentro do Gitlab, vamos criar um repositório para testarmos nosso webhook, se você não está com seu webhook(V1) e ngrok em pé é uma boa hora para subir novamente!


Voltando para o Gitlab:

* Clique _**Create Project**_
* De um nome ao seu projeto
* Deixe ele em **_public_**
* Clique em Initialize repository with a README
* Clique em _**Create Project**_

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/createproject.png?raw=true "Webhook")


## Testando Webhook

Beleza agora vamos configurar nosso webhook e testar!

Abra seu repositório e do lado esquerdo clique em:

* Settings
* Webhooks
* URL cole a do ngrok
* Selecione Comments
* Disabilite o enable ssl verification
* Add Hook

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/addwebhook.png?raw=true "Webhook")

Se tudo der certo você terá um webhook adicionado no Gitlab, agora podemos testar! :)

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/testwebhook.png?raw=true "Webhook")


Clique em:

* Test
* Push Events


Se você fez tudo certo você irá ver que seu webhook printou um push event do Gitlab no terminal do Flask!!


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/pushtest.png?raw=true "Webhook")

Parabéns, agora você sabe criar e usar um webhook no Gitlab :)

Segue o Json formatado para que possamos entender um pouco melhor oque está sendo retornado:

 
```
 {
    'object_kind': 'push',
    'event_name': 'push',
    'before': '72bf45d83be8c362604d8fd7ab7873c45aaf3cdd',
    'after': '72bf45d83be8c362604d8fd7ab7873c45aaf3cdd',
    'ref': 'refs/heads/master',
    'checkout_sha': '72bf45d83be8c362604d8fd7ab7873c45aaf3cdd',
    'message': None,
    'user_id': 1,
    'user_name': 'Administrator',
    'user_username': 'root',
    'user_email': '',
    'user_avatar': 'https://secure.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon',
    'project_id': 1,
    'project': {
        'id': 1,
        'name': 'Webhook',
        'description': '',
        'web_url': 'https://gitlab.webhook/root/webhook',
        'avatar_url': None,
        'git_ssh_url': 'git@gitlab.webhook:root/webhook.git',
        'git_http_url': 'https://gitlab.webhook/root/webhook.git',
        'namespace': 'Administrator',
        'visibility_level': 20,
        'path_with_namespace': 'root/webhook',
        'default_branch': 'master',
        'ci_config_path': None,
        'homepage': 'https://gitlab.webhook/root/webhook',
        'url': 'git@gitlab.webhook:root/webhook.git',
        'ssh_url': 'git@gitlab.webhook:root/webhook.git',
        'http_url': 'https://gitlab.webhook/root/webhook.git'
    },
    'commits': [{
        'id': '72bf45d83be8c362604d8fd7ab7873c45aaf3cdd',
        'message': 'Initial commit',
        'title': 'Initial commit',
        'timestamp': '2020-04-22T18:30:16+00:00',
        'url': 'https://gitlab.webhook/root/webhook/-/commit/72bf45d83be8c362604d8fd7ab7873c45aaf3cdd',
        'author': {
            'name': 'Administrator',
            'email': 'admin@example.com'
        },
        'added': ['README.md'],
        'modified': [],
        'removed': []
    }],
    'total_commits_count': 1,
    'push_options': {},
    'repository': {
        'name': 'Webhook',
        'url': 'git@gitlab.webhook:root/webhook.git',
        'description': '',
        'homepage': 'https://gitlab.webhook/root/webhook',
        'git_http_url': 'https://gitlab.webhook/root/webhook.git',
        'git_ssh_url': 'git@gitlab.webhook:root/webhook.git',
        'visibility_level': 20
    }
}
```

Perfeito! Vamos seguir para a próxima parte!


## Autenticando o Webhook

A partir deste ponto iremos trabalhar como a primeira versão de webhook fizemos, se você tiver em dúvida veja o dia1/webhook.py.

A primeira coisa para melhorarmos no nosso webhook é a autenticação, felizmente o Gitlab já nos presenteia com uma verificação via HTTP Header.

Vamos primeiramente testar!

Volte ao Gitlab e clique em edit no seu webhook, após isso vá até o topo da página e adicione em _**Secret**_ _**Token**_ um token qualquer:


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/tokensecret.png?raw=true "Webhook")


Agora vamos editar nosso webhook para que ele verifique o token enviado:

```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## URL do Gitlab
gitlab_http_token = "teste" ## token recebido do Gitlab

@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if (request.method == 'POST') and (request.headers.get('X-Gitlab-Token') == gitlab_http_token): # Se o request vindo for POST e o Header correto entre na condição.
        print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400, 'Your HTTP Secret token is wrong or this is not a POST request')              

if __name__ == '__main__':
    app.run()
```

Agora rode ele e teste novamente o seu webhook via Gitlab:

Você provavelmente receberá uma mensagem:

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/wrongtoken.png?raw=true "Webhook")


Agora pare seu Flask e coloque exatamente a senha que foi colocada na Interface do Gitlab no seu código e você deverá ver novamente o conteúdo e agora autenticado!