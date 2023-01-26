from pathlib import Path

GITREPO_DIREDTORY = str(Path.home() / "Documents/gitrepos")
NODE_FILE_PATH = str(Path.home() / ".nodes/*.yaml")
JENKINS_NODE_FILE_PATH = str(Path.home() / ".jenkins/nodes/*.yaml")  # may conflict with Jenkins' files
GITREPO_FILE_PATH = str(Path.home() / ".gitrepos/*.repo")