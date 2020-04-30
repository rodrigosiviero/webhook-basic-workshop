from flask import Flask, request, abort   # Imports do Flask
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__) # Instância do Flask chamada app

url_base = 'http://localhost/api/v4/' ## uso posterior
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

        if not mr_iid:
            return "Esse Webhook não contém um comentário", 400
        
        if mr_author == note_author:
            return "Autor do MR é Igual ao aprovador", 400
 
        if mr_status != 'can_be_merged':
            return 'Esse MR não é mergeavel', 400
        
        if mr_notes == 'Aprovado!!!':
            r = requests.put(f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/merge", headers=gitlab_headers, verify=False)
            if r.status_code != 200:
                return 'Algo deu errado no MR', 404
        return 'Comentário aprovado', 200
    else:                               
        return 'Seu Token está errado ou isso não é um POST', 405
if __name__ == '__main__':
    app.run()