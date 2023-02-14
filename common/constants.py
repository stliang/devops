from pathlib import Path

GITREPO_DIREDTORY = str(Path.home() / "Documents/gitrepos")
NODE_FILE_PATH = str(Path.home() / ".nodes/*.yaml")
JENKINS_NODE_FILE_DIR = str(Path.home() / ".jenkins/nodes")
JENKINS_NODE_FILE_PATH = str(f"{JENKINS_NODE_FILE_DIR}/*.yaml")  # may conflict with Jenkins' files
GITREPO_FILE_PATH = str(Path.home() / ".gitrepos/*.repo")