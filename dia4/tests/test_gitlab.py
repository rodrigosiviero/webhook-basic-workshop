#!/usr/bin/env python
import json
import os
import sys
from dataclasses import dataclass

sys.path.append(os.getcwd())
import gitlab_custom_webhook
import pytest
import requests

url = 'http://localhost:5000/webhook'


@dataclass
class Requests():
    status_code: int
    msg: str

    def json(self):
        return json.loads(self.msg)


@pytest.fixture()
def headers():
    return {
        'X-Gitlab-Token': gitlab_custom_webhook.gitlab_http_token,
        'Content-type': 'application/json',
    }


@pytest.fixture
def payload():
    return {
        'merge_request': {
            'iid': 'king_arthur',
            'author_id': 'black_knight',
            'merge_status': 'can_be_merged',
        },
        'object_attributes': {
            'author_id': 'king_arthur',
            'note': 'Aprovado!!!',
            'project_id': 'cheeseshop',
        }
    }


def test_gitlab_should_succeed(headers, payload):
    def _requests_call(url, headers, verify):
        return 200

    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 200
    assert msg == 'Merge Realizado com Sucesso!'


def test_gitlab_should_fail_with_invalid_gitlab_header(headers, payload):
    headers['X-Gitlab-Token'] = 'invalid_header'
    _requests_call = lambda x: x
    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 400
    assert msg == 'Seu Token está errado'


def test_gitlab_should_fail_with_invalid_mr_iid(headers, payload):
    payload['merge_request']['iid'] = ''
    _requests_call = lambda x: x
    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 400
    assert msg == 'Esse Webhook não tem um Merge_request presente'


def test_gitlab_should_fail_with_invalid_note_author(headers, payload):
    payload['object_attributes']['author_id'] = payload['merge_request']['author_id']
    _requests_call = lambda x: x
    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 400
    assert msg == 'O Autor do MR não pode aprovar o próprio MR'


def test_gitlab_should_fail_with_invalid_note_author(headers, payload):
    payload['object_attributes']['author_id'] = 'black_knight'
    _requests_call = lambda x: x
    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 400
    assert msg == 'O Autor do MR não pode aprovar o próprio MR'


def test_gitlab_should_fail_with_invalid_merge_status(headers, payload):
    payload['merge_request']['merge_status'] = 'invalid merge status'
    _requests_call = lambda x: x
    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 400
    assert msg == 'Esse MR não pode ser Mergeado'


def test_gitlab_should_fail_with_invalid_note(headers, payload):
    payload['object_attributes']['note'] = 'invalid note'
    _requests_call = lambda x: x
    status_code, msg = gitlab_custom_webhook.execute_gitlab_webhook(headers, payload, _requests_call)

    assert status_code == 400
    assert msg == 'Comentário não confere ou Algo deu errado.'
