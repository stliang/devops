# from file_helper import *
import git

class GitRepo:
    def __init__(self, repo_home="", username="", password="", **kwargs):
        self.username = username
        self.password = password
        self.repo_home = repo_home

    def clone_repo(self, repo_url):
        x = repo_url.split("/")[-1]
        repo_name = x.split(".")[0]
        git.Repo.clone_from(repo_url, '{repo_home}/{repo_name}')