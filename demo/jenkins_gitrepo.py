import sys
sys.path.append('../')
import common.constants    as C
import common.file_helper  as F
import common.gitrepo      as G
import common.report       as R

# As a Build and Release engineer, I want to find out which nodes a git repo uses for
# building so that I can move the build job and nodes to newer Jenkins server without
# breakig other jobs.

# First findout the agent labels used in Jenkinsfile of gitrepo
repos_to_checkout = F.deserialized_repos()
repo_names = [G.extract_repo_name(repo_url) for repo_url in repos_to_checkout]
print(repo_names)
git_account = G.GitRepo(C.GITREPO_DIREDTORY)
checked_out_repos = [git_account.clone_repo(repo_url) for repo_url in repos_to_checkout]
print(checked_out_repos)

# Of the labels being used, which Jenkins agent / node has that label

# Of the nodes' other labels, which other build jobs use them

# Once we have those infomation, we can determine the impact of moving a node as a
# node can have multiple labels and thus used by multiple jobs



