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
        self.node_instances = list(map(lambda node: UbuntuHealthCheck(**node), self.nodes))

    def check_mount_ok(self, node_instance, mount_path):
        match node_instance.mount_ok(mount_path):
            case [True,msg] if mount_path in msg:
                print_ok(f"{node_instance} mount path {mount_path}")
            case [_,msg]:
                print_fail(f"{node_instance} mount path {mount_path}", msg)
            case _:
                print_unkown(f"{node_instance} mount path {mount_path}")

    def check_systemd_timesyncd_ok(self, node_instance):
        if node_instance.systemd_timesyncd_ok()[0] or node_instance.ntp_ok()[0]:
            print_ok(f"{node_instance} time service")
        else:
            print_fail(f"{node_instance} time service", "not running")

    def check_mount_path_usage_ok(self, node_instance, mount_path="/", usage_limit=60):
        match node_instance.mount_path_usage_ok(mount_path, usage_limit):
            case [True,msg]:
                print_ok(f"{node_instance} mount path {mount_path} usage")
            case [_,msg]:
                print_fail(f"{node_instance} mount path {mount_path}usage", msg)
            case _:
                print_unkown(f"{node_instance} mount path {mount_path} usage")

    def check_java_ok(self, node_instance, java_version):
        match node_instance.java_version_ok(java_version):
            case [True,msg]:
                print_ok(f"{node_instance} java {java_version}")
            case [_,msg]:
                print_fail(f"{node_instance} java {java_version}", msg)
            case _:
                print_unkown(f"{node_instance} java version")
        match node_instance.java_ps_ok(java_version):
            case [True,msg]:
                print_ok(f"{node_instance} java {java_version} process")
            case [_,msg]:
                print_fail(f"{node_instance} java {java_version} process", msg)
            case _:
                print_unkown(f"{node_instance} java process")

    def check_docker_ok(self, node_instance):
        match node_instance.docker_ok():
            case [True,msg]:
                print_ok(f"{node_instance} docker")
            case [_,msg]:
                print_fail(f"{node_instance} docker", msg)
            case _:
                print_unkown(f"{node_instance} docker")

    def check_all(self):
        for node_instance in self.node_instances:
            self.check_mount_ok(node_instance, "/")
            self.check_systemd_timesyncd_ok(node_instance)
            self.check_mount_path_usage_ok(node_instance, mount_path="/", usage_limit=70)
            self.check_java_ok(node_instance, "11")
            self.check_docker_ok(node_instance)

# Demo Ubuntu Health Check on Jenkins Nodes
my_nodes = deserialized_jenkins_nodes()
demo = Demo(my_nodes)
demo.check_all()

