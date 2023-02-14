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
            case {'java_version': version}:
                java_version = version
            case _:
                java_version = "java_version undefined"
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

    def check_docker_server_version_ok(self, ubuntu_instance):
        match ubuntu_instance.capabilities:
            case {'docker_server_version': version}:
                docker_server_version = version
            case _:
                docker_server_version = "Docker server version undefined"
        match ubuntu_instance.docker_server_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} docker server version {docker_server_version}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} docker server version {docker_server_version}", msg)
            case _:
                print_unkown(f"{ubuntu_instance} docker server version {docker_server_version}")

    def check_docker_client_version_ok(self, ubuntu_instance):
        match ubuntu_instance.capabilities:
            case {'docker_client_version': version}:
                docker_client_version = version
            case _:
                docker_client_version = "Docker server version undefined"
        match ubuntu_instance.docker_client_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} docker server version {docker_client_version}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} docker server version {docker_client_version}", msg)
            case _:
                print_unkown(f"{ubuntu_instance} docker server version {docker_client_version}")

    def check_all(self, ubuntu_instance):
        self.check_mount_ok(ubuntu_instance, "/")
        self.check_time_service_ok(ubuntu_instance)
        self.check_mount_path_usage_ok(ubuntu_instance, mount_path="/", usage_limit=70)
        self.check_java_ok(ubuntu_instance)
        self.check_docker_service_ok(ubuntu_instance)
        self.check_docker_server_version_ok(ubuntu_instance)
        self.check_docker_client_version_ok(ubuntu_instance)
    
    def run(self):
        for ubuntu_instance in self.ubuntu_instances:
            self.check_all(ubuntu_instance)

    def debug(self):
        output = {'nodes': []}
        for ubuntu_instance in self.ubuntu_instances:
            life_state = ubuntu_instance.life_state()
            ubuntu_instance.set_health_check_state(life_state)
            output['nodes'] += [ubuntu_instance.get_state()]
        print(f"processing node: {ubuntu_instance}")
        save_jenkins_nodes_state(output)

# Demo Ubuntu Health Check on Jenkins Nodes
my_nodes = deserialized_jenkins_nodes()
demo = Demo(my_nodes)
# demo.run()
demo.debug()