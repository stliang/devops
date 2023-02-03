import sys
sys.path.append('../')
from common.ubuntu_health_check import UbuntuHealthCheck
from common.report import *
from common.file_helper import *

class Demo():
    def __init__(
        self,
        nodes # [{short_name: host_1, host_address: x.x.x.x, port: 22, username: ***, password: ***}, ...]
        ):
        self.nodes = nodes
        self.node_instances = map(lambda node: UbuntuHealthCheck(**node), self.nodes)

    def check_mount_ok(self, mount_path):
        for node_instance in self.node_instances:
            match node_instance.mount_ok(mount_path):
                case [True,msg] if mount_path in msg:
                    print_ok(f"{node_instance} mount")
                case [_,msg]:
                    print_fail(f"{node_instance} mount", msg)
                case _:
                    print_unkown(f"{node_instance} mount")

    def check_systemd_timesyncd_ok(self):
        for node_instance in self.node_instances:
            if node_instance.systemd_timesyncd_ok() or node_instance.ntp_ok():
                print_ok(f"{node_instance} time service")
            else:
                print_fail(f"{node_instance} time service", "not running")

    # def check_all(self):
    #     print("Checking mount")
    #     self.demo_mount_ok("/boot/efi")
    #     print("Demo systemd_timesyncd")
    #     self.demo_systemd_timesyncd_ok()

# Demo Ubuntu Health Check on Jenkins Nodes
my_nodes = deserialized_jenkins_nodes()
demo = Demo(my_nodes)
# demo.check_all()
# demo.check_mount_ok("/")
demo.check_systemd_timesyncd_ok()