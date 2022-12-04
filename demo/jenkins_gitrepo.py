import sys
sys.path.append('../')
from common.constants import constants
from common.gitrepo import GitRepo
from common.file_helper import *
from common.report import *


# As a Build and Release engineer, I want to find out which nodes a git repo uses for
# building so that I can move the build job and nodes to newer Jenkins server without
# breakig other jobs.

# First findout the agent labels used in Jenkinsfile of gitrepo
repos_to_checkout = deserialized_repos()
print(repos_to_checkout)

git_account = GitRepo(constants.GITREPO_DIREDTORY)
checked_out_repos = [git_account.clone_repo(repo_url) for repo_url in repos_to_checkout]
print(checked_out_repos)

# Of the labels being used, which Jenkins agent / node has that label

# Of the nodes' other labels, which other build jobs use them

# Once we have those infomation, we can determine the impact of moving a node as a
# node can have multiple labels and thus used by multiple jobs



