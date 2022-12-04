from .constants import constants
from functools import reduce
from pathlib import Path
import glob
import re
import yaml

def composite_function(*func):
    def compose(f, g):
        return lambda x : f(g(x))  
    return reduce(compose, func, lambda x : x)

def deserialized_nodes() -> [dict]:
    nodes = []
    yamlFilenamesList = glob.glob(constants.NODE_FILE_PATH)
    for yaml_file in yamlFilenamesList:
        with Path(yaml_file).open("r") as stream:
            try:
                node_dict = yaml.safe_load(stream)
                nodes.extend(node_dict["nodes"])
            except yaml.YAMLError as exc:
                print(exc)
    return nodes

def list_files_like(dir, like_file_name) -> [str]:
    found = []
    for match in glob.glob(f"{dir}/*{like_file_name}*"):
        found.append(match)
    return found


def find_lines(search_term, file_path) -> [str]:
    found = []
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            if line.find(search_term) != -1:
                found.append(line)
    return found

def find_label(string) -> str:
    pattern = "[L|l]abel[:]*\s+'(.*)'"
    match = re.search(pattern, string) 
    if match:
        return match.groups()[0]
    else:
        return ''
    