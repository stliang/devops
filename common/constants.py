from pathlib import Path

class constants:
    NODE_FILE_PATH = str(Path.home() / ".nodes/*.yaml")
    GITREPO_FILE_PATH = str(Path.home() / ".gitrepos/*.repo")
    GITREPO_DIREDTORY = str(Path.home() / "Documents/gitrepos")