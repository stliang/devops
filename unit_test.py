from common.linux import Linux
# from pathlib import Path
import unittest
# import yaml

class TestStringMethods(unittest.TestCase):
    # path = Path.home() / ".nodes/linux.yaml"
    # with path.open("r") as stream:
    #     linux_nodes = []
    #     try:
    #         node_dict = yaml.safe_load(stream)
    #         for node in node_dict["nodes"]:
    #             node_instance = Linux(**node)
    #             print(yaml.dump(node_instance.os_release())) # Yaml dump resulting single quotes in VERSION_ID are fine
    #             print(yaml.dump(node_instance.hostnamectl()))
    #     except yaml.YAMLError as exc:
    #         print(exc)