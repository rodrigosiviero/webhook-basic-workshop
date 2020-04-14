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