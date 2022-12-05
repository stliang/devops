import sys
import os
sys.path.append('../')
import common.constants    as C
import common.file_helper  as F
import common.gitrepo      as G
import common.report       as R

# As a Build and Release engineer, I want to find out which nodes a git repo uses for
# building so that I can move the build job and nodes to newer Jenkins server without
# breakig other jobs.

# # First findout the agent labels used in Jenkinsfile of gitrepo
# repos_to_checkout = F.deserialized_repos()
# repo_names = [G.extract_repo_name(repo_url) for repo_url in repos_to_checkout]
# print(repo_names)
# git_account = G.GitRepo(C.GITREPO_DIREDTORY)
# checked_out_repos = [git_account.clone_repo(repo_url) for repo_url in repos_to_checkout]
# print(checked_out_repos)

# xs = {}
# for repo_name in repo_names:
#     xs[repo_name] = F.find_labels_in_like_files(f"{C.GITREPO_DIREDTORY}/{repo_name}/.jenkins", "Jenkins")
# print(xs)

# check tests/nsa/regression/.jenkins/Jenkinsfile
# check tests/nsa/ci/.jenkins/Jenkinsfile
# check tests/nsa/ci/.jenkins/Jenkinsfile

# get all Jenkins nodes and their assocaited labels

# import jenkins

# URL = os.getenv('JENKINS_URL')
# USER = os.getenv('JENKINS_USER')
# PASSWORD = os.environ.get('JENKINS_PASSWORD')

# server = jenkins.Jenkins(URL, username=USER, password=PASSWORD)
# user = server.get_whoami()
# version = server.get_version()
# print('Hello %s from Jenkins %s' % (user['fullName'], version))

# node_names = server.get_nodes()
# for name in node_names:
#     print(server.get_node_info(name))

# # import requests module
# import requests

# # Making a get request
# response = requests.get('http://rsc-jenkins-01.eth.rsshpc1.sc1.science.roche.com:8080/computer/api/python')

# # print response
# print(response.content)

# # print json content
# # print(response.json())


import requests
from requests.exceptions import HTTPError

try:
    response = requests.get('http://rsc-jenkins-01.eth.rsshpc1.sc1.science.roche.com:8080/computer/api/json?pretty=true')
    response.raise_for_status()
    # access JSOn content
    jsonResponse = response.json()
    print("Entire JSON response")
    print(jsonResponse)

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')


# Of the labels being used, which Jenkins agent / node has that label

# Of the nodes' other labels, which other build jobs use them

# Once we have those infomation, we can determine the impact of moving a node as a
# node can have multiple labels and thus used by multiple jobs



