import json

import requests
import urllib3
from flask import Flask, request, make_response

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

url_base = 'http://gitlab.webhook/api/v4/'
gitlab_http_token = "teste"
gitlab_headers = {"PRIVATE-TOKEN": ""}


def _check_conditions(gitlab_header, payload):
    mr_iid = payload['merge_request']['iid']
    mr_author = payload['merge_request']['author_id']
    note_author = payload['object_attributes']['author_id']
    mr_status = payload['merge_request']['merge_status']
    mr_notes = payload['object_attributes']['note']

    if gitlab_header['X-Gitlab-Token'] != gitlab_http_token:
        return False, 400, 'Seu Token está errado'

    if not mr_iid:
        return False, 400, 'Esse Webhook não tem um Merge_request presente'

    if mr_author == note_author:
        return False, 400, 'O Autor do MR não pode aprovar o próprio MR'

    if mr_status != 'can_be_merged':
        return False, 400, 'Esse MR não pode ser Mergeado'

    if mr_notes != 'Aprovado!!!':
        return False, 400, 'Comentário não confere ou Algo deu errado.'
    return True, 200, ''


def _requests_call(url):  # pragma:no cover
    response = requests.put(url, headers=gitlab_headers, verify=False)
    return response.status_code


def execute_gitlab_webhook(gitlab_header, payload, _requests_call):
    mr_iid = payload['merge_request']['iid']
    project_id = payload['object_attributes']['project_id']

    conditions_ok, status_code, msg = _check_conditions(gitlab_header, payload)

    if conditions_ok:
        url = f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/merge"
        status_code = _requests_call(url, headers=gitlab_headers, verify=False)

        if status_code == 200:
            return 200, "Merge Realizado com Sucesso!"
    else:
        return status_code, msg


@app.route('/webhook', methods=['POST'])
def webhook():  # pragma:no cover
    status_code, msg = execute_gitlab_webhook(request.headers['X-Gitlab-Token'], request.json, _requests_call)
    response = make_response(json.dumps({'message': msg}), status_code)
    response.headers['Content-type'] = 'application/json'
    return response


if __name__ == '__main__':  # pragma:no cover
    app.run()
