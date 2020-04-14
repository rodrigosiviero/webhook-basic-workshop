
from flask import Flask, request, abort
import requests

app = Flask(__name__)

url_base = 'https://alcs.accenture.com/gitlab/api/v4/'
gitlab_headers = {"PRIVATE-TOKEN": "JoPz-9mQUX896yg1Udzb"}

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if (request.headers.get('X-Gitlab-Token') == 'teste'):
            json_payload = request.json
            print(json_payload)
            project_id = json_payload['object_attributes']['project_id']
            mr_notes = json_payload['object_attributes']['note']
            mr_iid = json_payload['merge_request']['iid']
            mr_creator = json_payload['user']['name']
            mr_status = json_payload['merge_request']['merge_status']
            not_approved_payload = {"body": "/tableflip This MR cannot be merged, please merge it manually"}
            if mr_iid:
                print("This is a MR note hook")
                if mr_status == "can_be_merged" and mr_notes == "Approved":
                    print("MR Aprovado")
                    r = requests.put(f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/merge", headers=gitlab_headers)
                    if r.status_code == '200':
                        r = requests.post(f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/notes?body={mr_creator} your merge was successfully done" , headers=gitlab_headers)
                    else:
                        r = requests.post(f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/notes?body=/shrug {mr_creator} something went wrong with your merge" , headers=gitlab_headers)
                elif mr_status == "cannot_be_merged" and mr_notes == "Approved":
                    print("Deve ser mergeado manual")
                    r = requests.post(f"{url_base}projects/{project_id}/merge_requests/{mr_iid}/notes", params=not_approved_payload , headers=gitlab_headers)
                else:
                    print("Nao aprovado")
            return '', 200
        else: 
            return '', 401
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
