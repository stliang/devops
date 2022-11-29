import sys
sys.path.append('../devops')
from common.ubuntu import Ubuntu
from common.report import *
from common.file_helper import *

class HealthCheck():
    def __init__(
        self,
        nodes # [{short_name: host_1, host_address: x.x.x.x, port: 22, username: ***, password: ***}, ...]
        ):
        self.nodes = nodes
        self.node_instances = map(lambda node: Ubuntu(**node), self.nodes)

    def mount_ok(self):
        for node_instance in self.node_instances:
            match node_instance.mount_ok():
                case [True,msg] if "/boot/efi" in msg:
                    print_ok(f"{node_instance} mount")
                case [_,msg]:
                    print_fail(f"{node_instance} mount", msg)
                case _:
                    print_unkown(f"{node_instance} mount")

    def check_all(self):
        self.mount_ok()

my_nodes = deserialized_nodes()
health_check = HealthCheck(my_nodes)
health_check.check_all()