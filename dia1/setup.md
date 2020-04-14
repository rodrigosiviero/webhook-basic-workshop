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


Para fazermos


Abra seu editor preferido e crie um arquivo chamado webhook.py, em seguida vamos copiar e colar o seguinte conteudo:



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





