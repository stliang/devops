from . import constants as C
from functools import reduce
from pathlib import Path
import glob
import itertools
import re
import yaml

def composite_function(*func):
    def compose(f, g):
        return lambda x : f(g(x))  
    return reduce(compose, func, lambda x : x)

def deserialized_nodes() -> [dict]:
    nodes = []
    yamlFilenamesList = glob.glob(C.NODE_FILE_PATH)
    for yaml_file in yamlFilenamesList:
        with Path(yaml_file).open("r") as stream:
            try:
                node_dict = yaml.safe_load(stream)
                nodes.extend(node_dict["nodes"])
            except yaml.YAMLError as exc:
                print(exc)
    return nodes

def deserialized_repos() -> [str]:
    repos = []
    repoFilenamesList = glob.glob(C.GITREPO_FILE_PATH)
    for repo_file in repoFilenamesList:
        with open(repo_file) as f:
            repos += map(lambda x: x.strip(), f.readlines())
    return repos

def list_files_like(directory, like_file_name) -> [str]:
    found = []
    for match in glob.glob(f"{directory}/*{like_file_name}*"):
        found.append(match)
    return found

def find_lines(file_path, search_function) -> [str]:
    found = []
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            found_str = search_function(line)
            if found_str:
                found.append(found_str)
    return found

def find_regex_group(regex_pattern, line) -> str:
    match = re.search(regex_pattern, line) 
    if match:
        return match.groups()[0]
    else:
        return ''

def find_label(line) -> str:
    pattern = "[L|l]abel[:]*\s+'(.*)'"
    return find_regex_group(pattern, line)

def find_lines_with_label(file_path) -> [str]:
    return find_lines(file_path, find_label)

def find_labels_in_like_files(directory, like_file_name) -> [str]:
    xs = list_files_like(directory, like_file_name)
    ys = map(lambda x: find_lines_with_label(x), xs)
    flat_ys = list(itertools.chain(*ys))
    return list(set(flat_ys))