from common.ubuntu import Ubuntu
from common.file_helper import *
import unittest

# Run this test as "python ./unit_test.py"
class TestDevOpsMethods(unittest.TestCase):

    def setUp(self):
        self.nodes = deserialized_nodes()
        self.node_instances = map(lambda node: Ubuntu(**node), self.nodes)

    def test_mount(self):
        for node_instance in self.node_instances:
            print(f"testing node: {node_instance}")
            mount_checked = node_instance.mount_ok() # [Boolean, String]
            self.assertTrue(mount_checked[0])
            break

if __name__ == '__main__':
    unittest.main()