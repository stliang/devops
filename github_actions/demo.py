#!/usr/bin/env python3

import warnings
warnings.filterwarnings('ignore')

import json
import os
import pprint
import re
import requests
import sys
import yaml

from pathlib import Path
from requests.auth import HTTPBasicAuth

GITHUB_ACTIONS_CONFIG = str(Path.home() / ".github/config.yaml")

# github config YAML file example:
# token: ghp_*****************************
# owner: MY_TEAM
# repo: MY_APP
def deserialized_config() -> dict:
    config = {}
    try:
        with Path(GITHUB_ACTIONS_CONFIG).open("r") as stream:
            config = yaml.safe_load(stream)
    except:
        return {}
    return config

def pretty_print(my_dictionary):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(my_dictionary)

class ActionClient(object):
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.actions_url = f"https://api.github.com/repos/{owner}/{repo}/actions"
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {self.token}',
            'X-GitHub-Api-Version': '2022-11-28'
            }

    def __str__(self):
        return f"ActionClient"

    # timeout is (connect timeout, read timeout) tuple in seconds
    def try_get(self, url, timeout=(5, 15)) -> dict:
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            data = response.json()
            return data
        except Exception:
            return {}

    # timeout is (connect timeout, read timeout) tuple in seconds
    def try_get_file(self, output_file_name, url, timeout=(5, 1200)) -> [bool]:
        try:
            response = requests.get(url, headers=self.headers, allow_redirects=True, timeout=timeout)
            open(output_file_name, 'wb').write(response.content)
            return [True]
        except Exception:
            return []

    def list_repo_workflows(self) -> dict:
        url = f"{self.actions_url}/workflows"
        return self.try_get(url)

    def list_workflow_runs(self, workflow_id) -> dict:
        url = f"{self.actions_url}/workflows/{workflow_id}/runs"
        return self.try_get(url)
    
    def list_run_artifacts(self, run_id) -> dict:
        url = f"{self.actions_url}/runs/{run_id}/artifacts"
        return self.try_get(url)
    
    def download_artifact(self, output_file_name, artifact_id, format="zip"):
        url = f"{self.actions_url}/artifacts/{artifact_id}/{format}"
        return self.try_get_file(output_file_name, url)

    def get_workflow_id(self, workflow_name) -> [int]:
        data = self.list_repo_workflows()
        for workflow in data['workflows']:
            if workflow['name'] == workflow_name:
                return [workflow['id']]
        return []
    
    def get_last_successful_run(self, workflow_name) -> dict:
        workflows = self.list_repo_workflows()
        ids = self.get_workflow_id(workflow_name)
        for id in ids:
            run_data = self.list_workflow_runs(id)
            for run in run_data['workflow_runs']:
                if run['conclusion'] == 'success':
                    return run

def main():
    github_config = deserialized_config()
    if not github_config:
        github_config["token"] = os.getenv('GITHUB_TOKEN')
        github_config["owner"] = os.getenv('OWNER')
        github_config["repo"] = os.environ.get('REPO')
    # pretty_print(github_config)
    client = ActionClient(**github_config)
    run_data = client.get_last_successful_run("My Workflow Name")
    # pretty_print(run_data)
    artifact_data = client.list_run_artifacts(run_data['id'])
    # pretty_print(artifact_data)
    for artifact in artifact_data['artifacts']:
        match = re.search('.*_My_File_Name$', artifact['name'])
        if match:
            print(f'archive_download_url: {artifact["archive_download_url"]}')
            client.try_get_file(f'{artifact["name"]}.zip', artifact["archive_download_url"])

# Run programe
# Example:
# GITHUB_TOKEN=<my token here> OWNER=MY_TEAM REPO=MY_APP ./demo.py
main()
