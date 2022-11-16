from .constants import constants
from pathlib import Path
import glob
import yaml

def deserialized_nodes() -> [dict]:
    nodes = []
    yamlFilenamesList = glob.glob(str(constants.NODE_FILE_PATH))
    for yaml_file in yamlFilenamesList:
        with Path(yaml_file).open("r") as stream:
            try:
                node_dict = yaml.safe_load(stream)
                nodes.extend(node_dict["nodes"])
            except yaml.YAMLError as exc:
                print(exc)
    return nodes