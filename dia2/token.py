
from flask import Flask, request, abort
import requests

app = Flask(__name__)

url_base = 'http://gilab.webhook/gitlab/api/v4/' ## uso posterior
gitlab_headers = {"PRIVATE-TOKEN": "JoPz-9mQUX896yg1Udzb"} ## Header para ser enviado ao Gitlab

@app.route('/webhook', methods=['POST'])  # Aqui estamos criando o decorador "route" do Flask, ele irá criar uma rota - http://localhost:5000/webhook
def webhook():                            # Defininindo a função webhook
    if request.method == 'POST':          # Se o request vindo for POST entre na condição
        print(request.json)               # Simplesmente iremos voltar o request com os dados que estão vindo
        return '', 200                    # Retorne 200
    else:                                 # Se o request for diferente de POST volte abort come erro 400 - Bad request, nesse caso irá voltar 405 por causa do Flask.  
        abort(400)              

if __name__ == '__main__':
    app.run()
