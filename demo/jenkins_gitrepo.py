import sys
sys.path.append('../')
import common.constants    as C
import common.file_helper  as F
import common.gitrepo      as G
import common.report       as R
import json
import os
import requests
from requests.exceptions import HTTPError

# As a Build and Release engineer, I want to find out which nodes a git repo uses for
# building so that I can move the build job and nodes to newer Jenkins server without
# breakig other jobs.

# findout the agent labels used in Jenkinsfile of gitrepo
repos_to_checkout = F.deserialized_repos()
repo_names = [G.extract_repo_name(repo_url) for repo_url in repos_to_checkout]
git_account = G.GitRepo(C.GITREPO_DIREDTORY)
checked_out_repos = [git_account.clone_repo(repo_url) for repo_url in repos_to_checkout]

repo_labels = {}
for repo_name in repo_names:
    repo_labels[repo_name] = F.find_labels_in_like_files(f"{C.GITREPO_DIREDTORY}/{repo_name}/.jenkins", "Jenkins")

# get all Jenkins nodes and their assocaited labels
JENKINS_URL = os.getenv('JENKINS_URL')
jenkins_nodes = {}
try:
    response = requests.get(JENKINS_URL)
    response.raise_for_status()
    jsonResponse = response.json()
    for node in jsonResponse["computer"]:
        jenkins_nodes[node['displayName']] = list(map(lambda label: label['name'], node['assignedLabels']))
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

# Jenkins node usage by git repo
repo_nodes = {}
for repo_key, repo_labels in repo_labels.items():
    repo_nodes[repo_key] = []
    for repo_label in repo_labels:
        for node_key, node_labels in jenkins_nodes.items():
            if repo_label in node_labels:
                repo_nodes[repo_key] += [node_key]
print(json.dumps(repo_nodes, sort_keys=True, indent=4))