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

## Aprovando um merge request

Agora vamos de fato fazer um webhook que interaja com o Gitlab, para isso precisamos primeiro fazer algumas configurações no nosso projeto.

* Desabilite no Autodevops em:
  * Settings > CI/CD
* Crie uma nova branch chamada _**develop**_
  * Repository > + > New branch


Perfeito! Agora temos como fazer um Merge request!

Crie uma modificação qualquer no README em _**develop**_ e depois crie um merge request para _**master**_.


Você terá algo assim:

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/mr.png?raw=true "Webhook")



Perfeito! Agora vamos começar nosso webhook para aprovação de Merge Requests!

A primeira coisa que faremos é testar nosso Webhook novamente agora com oque precisamos de fato consumir que será comentário, o funcionamento será o seguinte:


1. Usuário A cria MR
2. Usuário B revisa o MR
3. Usuário B comenta no MR - "Aprovado"
4. Webhook aceita o merge


Quais as condições para que isso aconteça via webhook?

1. o Comentário precisa vir de um MR
2. O Usuário que criou o MR não pode aprovar o próprio MR
3. O MR precisa ser "mergeavel"
4. String do comentário precisa ser "Aprovado"


Se todas essas condições passarem o webhook irá fazer o MR.


Ok Vamos lá!

Só para relembrar iremos começar trabalhar em um arquivo novo com o conteúdo do nosso webhook_secret.py:

```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## uso posterior
gitlab_http_token = "teste"

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


1. Inicie o Flask
2. Inicie o ngrok
3. Tenha certeza que seu webhook está consumindo a url do ngrok.
4. Comente no seu próprio MR
5. Vá Até o terminal do Flask e copie seu JSON
6. Cole ele em um arquivo e deixe ele identado para facilitar


Perfeito! Agora temos nosso payload com oque iremos trabalhar, vamos verificar a primeira condição que definimos lá em cima


### O Comentário precisa vir de um MR

Beleza, temos nosso payload e precisamos verificar se o webhook enviou o nosso payload e ele veio de fato de um Merge Request, lembrando que qualquer tipo de comentário ativara nosso webhook então é importante fazer esse tratamento :)


Estamos procurando dentro do payload o dicionário: merge_request se ele tiver essa estrutura muito provavelmente seu webhook te enviou um comentário que está dentro de um merge_request, então vamos primeiro tratar o payload e assinalar uma variável para esse MR.

```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## uso posterior
gitlab_http_token = "teste"

@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if (request.method == 'POST') and (request.headers.get('X-Gitlab-Token') == gitlab_http_token): # Se o request vindo for POST e o Header correto entre na condição.
        #print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        json_payload = request.json        # Assinalando o request.json para uma variável
        mr_iid = json_payload['merge_request']['iid'] # Aqui iremos assinalar o conteudo do merge_request -> iid para a variável
        if mr_iid:
            print(f'Esse Webhook é de um Merge_request com Internal ID: {mr_iid}')
        else:
            print('Erro')
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400, 'Your HTTP Secret token is wrong or this is not a POST request')              

if __name__ == '__main__':
    app.run()
```


Você deverá ver no terminal do Flask:

```
Esse Webhook é de um Merge_request com Internal ID: 1
127.0.0.1 - - [23/Apr/2020 12:33:59] "POST /webhook HTTP/1.1" 200 -
```


Beleza! Temos nossa primeira condição completa! Vamos para a segunda.

### O Usuário que criou o MR não pode aprovar o próprio MR

Faremos a mesma coisa, precisamos agora:

* Achar o Autor do MR
* Achar o Autor do Comentário
* Checar se um é diferente do outro

Seguindo o mesmo passos iremos analisar a estrutura e achar o autor do Comentário e o autor do MR para comparar, para fazer este teste eu criei um novo user no Gitlab, fiz impersonate e comentei no MR.


Object attributes são os atributos do comentário então o nosso autor tem ID 34
```
	'object_attributes': { 
		'attachment': None,
		'author_id': 34,
		'change_position': None,
		'commit_id': None,
```

Merge request são os atributos do MR então o author_id é 1

```
	'merge_request': {
		'assignee_id': 1,
		'author_id': 1,
		'created_at': '2020-04-23 14:42:28 UTC',
		'description': '',
		'head_pipeline_id': None,
		'id': 1,
```

Utilizando a mesma lógica iremos:

* Assinalar os valores para variáveis
* Checar um com outro


Vai ficar assim:


```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## uso posterior
gitlab_http_token = "teste"

@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if (request.method == 'POST') and (request.headers.get('X-Gitlab-Token') == gitlab_http_token): # Se o request vindo for POST e o Header correto entre na condição.
        print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        json_payload = request.json        # Assinalando o request.json para uma variável
        mr_iid = json_payload['merge_request']['iid'] # Aqui iremos assinalar o conteudo do merge_request -> iid para a variável
        mr_author = json_payload['merge_request']['author_id']
        note_author = json_payload['object_attributes']['author_id']
        mr_status = json_payload['merge_request']['merge_status']
        if mr_iid:
            print(f'Esse Webhook é de um Merge_request com Internal ID: {mr_iid}')
            if mr_author is not note_author:
                print(f'Autor do MR: {mr_author} e o Autor do Comentário: {note_author}')
            else:
                print('O Autor do MR não pode aprovar o próprio MR')
        else:
            print('Erro')
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400, 'Seu Token está errado ou isso não é um POST')              

if __name__ == '__main__':
    app.run()

```

Se tudo deu certo seu output será:

```
Esse Webhook é de um Merge_request com Internal ID: 1
Autor do MR: 1 e o Autor do Comentário: 34
```

Ou

```
Esse Webhook é de um Merge_request com Internal ID: 1
O Autor do MR não pode aprovar o próprio MR
```

Beleza agora temos a 2 condição pronta, vamos seguir.


### MR é "mergeavel"

* Checar se o MR é mergeavel

Novamente essa parte é fácil, precisamos pegar do dicionário merge_request se o status dele é mergeavel:

```
		'merge_status': 'can_be_merged',
		'merge_user_id': None,
		'merge_when_pipeline_succeeds': False,
		'milestone_id': None,
```

Pegaremos o merge_status usando o mesmo processo de antes:

```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## uso posterior
gitlab_http_token = "teste"

@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if (request.method == 'POST') and (request.headers.get('X-Gitlab-Token') == gitlab_http_token): # Se o request vindo for POST e o Header correto entre na condição.
        print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        json_payload = request.json        # Assinalando o request.json para uma variável
        mr_iid = json_payload['merge_request']['iid'] # Aqui iremos assinalar o conteudo do merge_request -> iid para a variável
        mr_author = json_payload['merge_request']['author_id']
        note_author = json_payload['object_attributes']['author_id']
        mr_status = json_payload['merge_request']['merge_status']
        if mr_iid:
            print(f'Esse Webhook é de um Merge_request com Internal ID: {mr_iid}')
            if mr_author is not note_author:
                print(f'Autor do MR: {mr_author} e o Autor do Comentário: {note_author}')
                if mr_status == 'can_be_merged':
                    print('Esse MR pode ser Mergeado')
                else:
                    print('Esse MR não pode ser Mergeado')
            else:
                print('O Autor do MR não pode aprovar o próprio MR')
        else:
            print('Erro')
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400, 'Seu Token está errado ou isso não é um POST')              

if __name__ == '__main__':
    app.run()

```


Boa! Se você fez tudo certo até agora você verá:

Esse Webhook é de um Merge_request com Internal ID: 1
Autor do MR: 1 e o Autor do Comentário: 34
Esse MR pode ser Mergeado


### Checar o comentário

Se o comentário for: "Aprovado!!!" iremos aprovar o MR se não iremos retornar uma mensagem que não foi possível realizar o mesmo.


Seguindo a mesma lógica:

```

from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## uso posterior
gitlab_http_token = "teste"


@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if (request.method == 'POST') and (request.headers.get('X-Gitlab-Token') == gitlab_http_token): # Se o request vindo for POST e o Header correto entre na condição.
        print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        json_payload = request.json        # Assinalando o request.json para uma variável
        mr_iid = json_payload['merge_request']['iid'] # Aqui iremos assinalar o conteudo do merge_request -> iid para a variável
        mr_author = json_payload['merge_request']['author_id']
        note_author = json_payload['object_attributes']['author_id']
        mr_status = json_payload['merge_request']['merge_status']
        mr_notes = json_payload['object_attributes']['note']
        if mr_iid:
            print(f'Esse Webhook é de um Merge_request com Internal ID: {mr_iid}')
            if mr_author is not note_author:
                print(f'Autor do MR: {mr_author} e o Autor do Comentário: {note_author}')
                if mr_status == 'can_be_merged':
                    print('Esse MR pode ser Mergeado')
                    if mr_notes == 'Aprovado!!!':
                        print('Faça o Merge')
                    else:
                        print('Comentário não confere ou Algo deu errado.')
                else:
                    print('Esse MR não pode ser Mergeado')
            else:
                print('O Autor do MR não pode aprovar o próprio MR')
        else:
            print('Erro')
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400, 'Seu Token está errado ou isso não é um POST')              

if __name__ == '__main__':
    app.run()

```


Agora se você não digitou corretamente você deve receber:

```
Esse Webhook é de um Merge_request com Internal ID: 1
Autor do MR: 1 e o Autor do Comentário: 34
Esse MR pode ser Mergeado
Comentário não confere ou Algo deu errado.
127.0.0.1 - - [23/Apr/2020 14:46:59] "POST /webhook HTTP/1.1" 200 -

```

E finalmente se estiver correto:

```
Esse Webhook é de um Merge_request com Internal ID: 1
Autor do MR: 1 e o Autor do Comentário: 34
Esse MR pode ser Mergeado
Faça o Merge
```

Pronto, agora estamos checando todas as condições previstas, vamos ao próximo passo de fazer de fato o MR.

Até agora temos:


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/dia2_diagram1.png?raw=true "Webhook")


### Interagindo com o Gitlab


Finalmente vamos interagir com o Gitlab de fato via API, para isso vamos usar o requests para realizar as chamadas da API e teremos que utilizar um token para realizar essas chamadas.

Primeiramente precisamos setar nossa url do gitlab e o header que passaremos que será o Private Token que criaremos:

Coloque no começo do seu arquivo logo abaixo da definição do app.

```
url_base = 'https://gitlab.webhook/gitlab/api/v4/'
gitlab_headers = {"PRIVATE-TOKEN": "token"}
gitlab_http_token = "teste"
```

Para fazer a chamada Post usando requests é simples veja o snippet abaixo:

```
r = requests.put(url, headers=headers_variable)
```

Para realizar o Merge iremos olhar a documentação do Gitlab API: https://docs.gitlab.com/ce/api/merge_requests.html

Mais especificamente o **_Accept MR_**


```
PUT /projects/:id/merge_requests/:merge_request_iid/merge
```

```
Parameters:

id (required) - The ID or URL-encoded path of the project owned by the authenticated user
merge_request_iid (required) - Internal ID of MR
```

Esses são os 2 parametros que usaremos para fazer o merge, perceba que já  merge_request_iid, precisamos agora pegar o ID do projeto e fazer a chamada via requests.


E assim fica o código final:


```
from flask import Flask, request, abort   # Imports do Flask
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://gitlab.webhook/api/v4/' ## uso posterior
gitlab_http_token = "teste"
gitlab_headers = {"PRIVATE-TOKEN": ""}

@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if (request.method == 'POST') and (request.headers.get('X-Gitlab-Token') == gitlab_http_token): # Se o request vindo for POST e o Header correto entre na condição.
        json_payload = request.json        # Assinalando o request.json para uma variável
        mr_iid = json_payload['merge_request']['iid'] # Aqui iremos assinalar o conteudo do merge_request -> iid para a variável
        mr_author = json_payload['merge_request']['author_id']
        note_author = json_payload['object_attributes']['author_id']
        mr_status = json_payload['merge_request']['merge_status']
        mr_notes = json_payload['object_attributes']['note']
        mr_creator = json_payload['user']['name']
        project_id = json_payload['object_attributes']['project_id']
        if mr_iid:
            print(f'Esse Webhook é de um Merge_request com Internal ID: {mr_iid}')
            if mr_author is not note_author:
                print(f'Autor do MR: {mr_author} e o Autor do Comentário: {note_author}')
                if mr_status == 'can_be_merged':
                    print('Esse MR pode ser Mergeado')
                    if mr_notes == 'Aprovado!!!':
                        r = requests.put(f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/merge", headers=gitlab_headers, verify=False)
                        if r.status_code == '200':
                            print("Merge Realizado com Sucesso!")
                    else:                               
                        print('Comentário não confere ou Algo deu errado.')
                else:
                    print('Esse MR não pode ser Mergeado')

            else:
                print('O Autor do MR não pode aprovar o próprio MR')
        else:
            print('Esse Webhook não tem um Merge_request presente')
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400, 'Seu Token está errado ou isso não é um POST')              

if __name__ == '__main__':
    app.run()
```


Note que tivemos que adicionar:

```
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

Pois estamos em um servidor sem Certificado!










