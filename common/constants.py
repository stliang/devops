from pathlib import Path

GITREPO_DIREDTORY = str(Path.home() / "Documents/gitrepos")
GITREPO_FILE_PATH = str(Path.home() / ".gitrepos/*.repo")
NODE_FILE_PATH = str(Path.home() / ".nodes/*.yaml")
SONARQUBE_FILE_PATH = str(Path.home() / ".services/sonarqube_tests.yaml")
JENKINS_NODE_FILE_DIR = str(Path.home() / ".jenkins/nodes")
JENKINS_NODE_FILE_PATH = str(f"{JENKINS_NODE_FILE_DIR}/*.yaml")  # may conflict with Jenkins' files