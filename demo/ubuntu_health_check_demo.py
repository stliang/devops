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
        self.ubuntu_instances = list(map(lambda node: UbuntuHealthCheck(**node), self.nodes))

    def check_mount_ok(self, ubuntu_instance, mount_path):
        match ubuntu_instance.mount_ok(mount_path):
            case [True,msg] if mount_path in msg:
                print_ok(f"{ubuntu_instance} mount path {mount_path}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} mount path {mount_path}", msg)
            case _:
                print_unkown(f"{ubuntu_instance} mount path {mount_path}")

    def check_time_service_ok(self, ubuntu_instance):
        if ubuntu_instance.systemd_timesyncd_ok()[0] or ubuntu_instance.ntp_ok()[0]:
            print_ok(f"{ubuntu_instance} time service")
        else:
            print_fail(f"{ubuntu_instance} time service", "not running")

    def check_mount_path_usage_ok(self, ubuntu_instance, mount_path="/", usage_limit=60):
        match ubuntu_instance.mount_path_usage_ok(mount_path, usage_limit):
            case [True,msg]:
                print_ok(f"{ubuntu_instance} mount path {mount_path} usage")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} mount path {mount_path}usage", msg)
            case _:
                print_unkown(f"{ubuntu_instance} mount path {mount_path} usage")

    def check_java_ok(self, ubuntu_instance):
        match ubuntu_instance.capabilities:
            case {'java': version}:
                java_version = version
            case _:
                java_version = "version undefined"
        match ubuntu_instance.java_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} java {java_version}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} java {java_version}", msg)
            case _:
                print_unkown(f"{ubuntu_instance} java version")
        match ubuntu_instance.java_ps_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} java {java_version} process")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} java {java_version} process", msg)
            case _:
                print_unkown(f"{ubuntu_instance} java process")

    def check_docker_service_ok(self, ubuntu_instance):
        match ubuntu_instance.docker_service_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} docker service")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} docker service", msg)
            case _:
                print_unkown(f"{ubuntu_instance} docker service")

    def check_docker_version_ok(self, ubuntu_instance):
        match ubuntu_instance.capabilities:
            case {'docker': version}:
                docker_version = version
            case _:
                docker_version = "version undefined"
        match ubuntu_instance.docker_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} docker version {docker_version}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} docker version {docker_version}", msg)
            case _:
                print_unkown(f"{ubuntu_instance} docker version {docker_version}")

    def check_all(self, ubuntu_instance):
        self.check_mount_ok(ubuntu_instance, "/")
        self.check_time_service_ok(ubuntu_instance)
        self.check_mount_path_usage_ok(ubuntu_instance, mount_path="/", usage_limit=70)
        self.check_java_ok(ubuntu_instance)
        self.check_docker_service_ok(ubuntu_instance)
        self.check_docker_version_ok(ubuntu_instance)
    
    def run(self):
        for ubuntu_instance in self.ubuntu_instances:
            self.check_all(ubuntu_instance)

    def debug(self):
        for ubuntu_instance in self.ubuntu_instances:
            print(ubuntu_instance.capabilities)

# Demo Ubuntu Health Check on Jenkins Nodes
my_nodes = deserialized_jenkins_nodes()
demo = Demo(my_nodes)
demo.run()
# demo.debug()