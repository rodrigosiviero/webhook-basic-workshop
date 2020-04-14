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


Agora exponha seu serviço para internet usando:


```
ngrok http 5000
```


O Ngrok é um serviço que ajuda você a expor um determinado protocolo nesse caso _**http**_ para a internet, assim qualquer um irá conseguir acessar utilizando um dominio.





