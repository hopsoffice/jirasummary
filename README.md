# Jira Summary

Server-less application that get a summary of Jira issues from text.

## Why do i need Jira Summary?

I use [Zapier] to show the Jira issue summary that mentioned in daily log for my team.
But [Zapier][]'s Jira Integration are able to find only one issue for one zap.
It takes too many zaps to find all Jira issue and update a item in notion.

So Jira Summary will find you all Jira issues in daily log text in 1 zap.


```
# Code By Zapier
import json
import urllib.request
import urllib.error
import datetime

def get_issues(text):
    payload = {'text': text}
    request = urllib.request.Request('https://<your API Gateway address>/issues/', method='POST', data=json.dumps(payload).encode('utf-8'))
    request.add_header('X-Jira-Summary-Token', '1346F3E5-450F-42A2-9A8A-6E1BAAC6103E')
    request.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError:
        return {}


logs = input_data['logs']
issues = get_issues(logs)
for key, content in issues.items():
  logs = logs.replace(key, '[ {} | {} ]'.format(key, content))

output = {'text': logs, 'today': datetime.date.today().isoformat()}
```

[Zapier]: https://zapier.com/


# Requirements

- [Python 3.8][python]
- [Poetry][]
- [Direnv][]
- [Jira API Token][jiraapitoken]
- AWS Account ( For deploy application. )

[Poetry]: https://github.com/python-poetry/poetry
[python]: https://www.python.org/
[Direnv]: https://direnv.net/
[jiraapitoken]: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/


# Installation

Install the dependencies

```
$ python -m venv .venv
$ venv .venv/bin/activate
$ potery install
```

Write your own envrc.

```
$ cp .envrc.template .envrc
$ vim .envrc
$ cat .envrc 

export jira_username=<your user name>
export jira_token=<your token>
export jira_baseurl=<your url>
export secret_key=<your secret key>

$ direnv allow
```


# Deployment

Use [zappa][] to deploy application on AWS Lambda + API Gateway.


[zappa]: https://github.com/zappa/Zappa


# API Specification

## /

```
# request

GET / HTTP/1.1
User-Agent: curl/7.64.1
Host: www.example.com


# response

HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Content-Type: text/plain

pong
```

## /issues/

- required
  - payload:
    - `{"text": <your text>}`
  - headers:
    - `X-Jira-Summary-Token`

```
# request

POST /issues/ HTTP/1.1
User-Agent: curl/7.64.1
Host: www.example.com
Content-Type: application/json
X-Jira-Summary-Token: sometoken

{"text": "JIRA-1 , JIRA-2"}


# response

HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Content-Type: application/json

{
    "JIRA-1": "Summary of JIRA 1",
    "JIRA-1": "Summary of JIRA 2"
}
```
