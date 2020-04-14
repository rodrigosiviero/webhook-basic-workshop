# Dia 1

## O que é um webhook?

* Conceito de API
* HTTP custom CallBack
* Ativadas por eventos. e.g. Push para repositório
* Consumida/Integrada por aplicações/terceiros
* "Tempo real"
* Muito utilizado em Continuous Integration


## Mas o que faremos?


Para esse primeiro dia iremos:

* Fazer setup do ambiente
* Criar nosso primeiro Webhook
* Consumir esse webhook via terminal
* Integrar ele com Gitlab local

Para ilustrar será isso:


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/Dia1.png?raw=true "Webhook")


Bom vamos começar!


## Setup do ambiente


Para o Setup precisaremos de Python3 e Docker e Docker compose, se você ainda não tem instale ambos para dar continuidade!

* Verifique a versão do seu Docker e se você está com compose também:

```
docker --version
docker-compose --version
```
* Verifique a versão do seu Python com:

```
python --version ou python3 --version
```

* Instale o Flask, requests:
  
```
pip install flask requests
```



## Criando meu primeiro Webhook


Vamos agora criar nosso webhook, ele será simples e não irá fazer basicamente nada agora!


Abra seu editor preferido e crie um arquivo chamado webhook.py, em seguida vamos copiar e colar o seguinte conteudo:


```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app


@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if request.method == 'POST':          # Se o request vindo for POST entre na condição
        print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400)                        

if __name__ == '__main__':                # Função Main
    app.run()                             # Executando de fato o script

```

Para executar seu servidor Flask, simplesmente execute no terminal:

```
python webhook.py

```

Se tudo funcionar você irá ver uma tela assim:


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/flask.png?raw=true "Webhook")


## Consumindo seu webhook

Se você rodou o servidor do flask e tem sua API no ar, chegou a hora de testarmos!

Abra um **outro** terminal e execute o seguinte:


```
curl -H "Content-Type: application/json" -X POST -d '{"mensagem": "Olá Mundo!! Olá Webhook"}' 127.0.0.1:5000/webhook
```

No momento de execução você deve receber um:

```
{"status":"success"}
```

Se você agora olhar no terminal aonde está rodando o servidor você deverá ver a requisição que acabou de fazer!

![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/olamundo.png?raw=true "Webhook")


Nesse comando estamos passando o -H que é o Header do request como Content-Type, ele serve para indicar para o servidor que estamos mandando um payload do tipo _JSON_.

O próximo parametro -X POST é o tipo de HTTP request, como nosso webhook só aceita POST iremos usar somente ele aqui.

E finalmente passamos o -d, que é de data, ele indica o payload que iremos enviar para nossa API/Webhook, nesse caso é o _JSON_:


```
{
   "mensagem":"Olá Mundo!! Olá Webhook"
}
```


## Modificando webhook.


Beleza, agora temos um webhook/API no ar, precisamos preparar ele agora para o próximo passo, vamos deixar mais agradavel a leitura para quem for receber o payload, para isso precisamos instalar o requests, caso você ainda não tenha feito, faça agora.


Esse é o código:


```
from flask import Flask, request, abort   # Imports do Flask

app = Flask(__name__) # Instância do Flask chamada app


@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if request.method == 'POST':          # Se o request vindo for POST entre na condição
        json_payload = request.json       # Pegaremos o request em json e atribuieremos para uma variável.
        name = json_payload['nome']       # Fazendo o parse da variavel que criamos com nossos dados em json e pegando o nome
        message= json_payload['mensagem'] # A mesma coisa acima porém a mensagem!
        print(f"{name} te enviou uma mensagem: {message}") # Iremos agora printar de forma formatada a mensagem recebida!
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400)                        

if __name__ == '__main__':                # Função Main
    app.run()                             # Executando de fato o script
```


## Brincando com o Webhook

Se você seguiu tudo até agora parabéns você tem um webhook no ar! Agora vamos expor ele para a Internet assim seus colegas vão conseguir consumir o mesmo.

Instale o Ngrok com:

Linux:

```
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
./ngrok
```

MacOS:
```
brew cask install ngrok
cd /usr/local/bin
ln -s /Applications/ngrok ngrok
```

O Ngrok é um serviço que ajuda você a expor um determinado protocolo nesse caso _**http**_ para a internet, assim qualquer um irá conseguir acessar utilizando um dominio.

Agora exponha seu serviço para internet usando:


```
ngrok http 5000
```

Algo assim irá aparecer:


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/Dia1_ngrok.png?raw=true "Webhook")

Isso significa que você está redirecionando o Flask para o ngrok, que te gerou um dominio temporário externo e você compartilhar para seus amigos o mesmo!

Agora pegue sua URL e mande para seus amigos e enviem qualquer tipo de mensagem!


Agora temos diversas pessoas mandando diversos posts para diversos webhooks distintos, temos mais ou menos algo assim:


![alt text](https://github.com/rodrigosiviero/webhook-basic-woorkshop/blob/master/images/final_day1.png?raw=true "Webhook")


# Dia 2

Agora que você terminou(ou não), vamos para o dia 2! Caso você não tenha terminado os arquivos estão na pasta do dia1!

[CLIQUE AQUI!](../dia2/webhook.md)