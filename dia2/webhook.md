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



 


