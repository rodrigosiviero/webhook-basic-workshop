from flask import Flask, request, abort
import requests

app = Flask(__name__)

url_base = 'https://alcs.accenture.com/gitlab/api/v4/'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
