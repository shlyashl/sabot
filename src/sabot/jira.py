import os
import json
import requests
from requests.auth import HTTPBasicAuth


def pull_into_crap(summary, description):
    jira_url = os.getenv("jira_url")
    jira_user = os.getenv("jira_user")
    jira_api_token = os.getenv("jira_api_token")
    jira_project_key = os.getenv("jira_project_key")
    issuetyp = [
        "Bi",
        "App",
        "Manage",
        "Integration",
        "Support"
    ]
    customfield_16408 = [
        "Даня",
        "Кирилл",
        "Кристина",
        "Миша",
        "Яна",
        "Глеб",
        "Денис",
        "Олег"
    ]
    customfield_14092 = [
        "Создание",
        "Доработка",
        "Багфикс",
        "Ад-хок / Bi",
        "Сквозные работы / Integration"
    ]
    issue_data = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issuetyp[3]
            },
            "customfield_16405": {"id": "17303"},
            "customfield_14092": {"value": customfield_14092[1]},
            "customfield_16408": {"value": customfield_16408[3]},
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{jira_url}/rest/api/2/issue",
        data=json.dumps(issue_data),
        headers=headers,
        auth=HTTPBasicAuth(jira_user, jira_api_token)
    )
    if response.status_code == 201:
        return f"{jira_url}/browse/{response.json()['key']}"
    else:
        return f"упс:\n{response.status_code}\n{response.text}"
