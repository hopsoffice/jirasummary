import base64
import json
import os
import re
import urllib.error
import urllib.request

from flask import Flask, abort, request

token = os.environ['jira_token']
username = os.environ['jira_username']
auth = base64.b64encode(f'{username}:{token}'.encode('utf-8')).decode('utf-8')
base_url = os.environ['jira_baseurl']
auth_token = os.environ['secret_key']


def get_issue(key: str):
    url = f'https://{base_url}/rest/api/latest/issue/{key}?fields=summary,assignee'
    request = urllib.request.Request(url)
    request.add_header('Authorization', f'Basic {auth}')
    try:
        with urllib.request.urlopen(request) as response:
           return json.loads(response.read())
    except urllib.error.HTTPError:
        return None


app = Flask(__name__)


@app.route('/', methods=['GET'])
def pong():
    return 'pong'


@app.route('/issues/', methods=['POST'])
def isssues():
    header_token = request.headers.get('X-Jira-Summary-Token')
    if not header_token or auth_token != header_token.lower():
        abort(401)
    payload = request.get_json()
    result = {}
    for issue in set(re.findall('[A-Za-z]+\-[0-9]+', payload['text'])):
        found = get_issue(issue)
        if found:
            result[issue] = found['fields']['summary']

    return result


if __name__ == '__main__':
    app.run(debug=True, port=8000)
