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

    def check_timesyncd_ok(self, ubuntu_instance):
        match ubuntu_instance.systemd_timesyncd_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} timesyncd")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} timesyncd", msg)
            case _:
                print_unkown(f"{ubuntu_instance} timesyncd")

    def check_ntp_ok(self, ubuntu_instance):
        match ubuntu_instance.ntp_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} ntp")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} ntp", msg)
            case _:
                print_unkown(f"{ubuntu_instance} ntp")

    def check_mount_path_usage_ok(self, ubuntu_instance, mount_path="/", usage_limit=60):
        match ubuntu_instance.mount_path_usage_ok(mount_path, usage_limit):
            case [True,msg]:
                print_ok(f"{ubuntu_instance} mount path {mount_path} usage")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} mount path {mount_path}usage", msg)
            case _:
                print_unkown(f"{ubuntu_instance} mount path {mount_path} usage")

    def check_java_version_ok(self, ubuntu_instance):
        match ubuntu_instance.java_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} java {ubuntu_instance.capabilities['java_version']}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} java version", msg)
            case _:
                print_unkown(f"{ubuntu_instance} java version")

    def check_java_ps_ok(self, ubuntu_instance):
        match ubuntu_instance.java_ps_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} java process {ubuntu_instance.capabilities['java_process']}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} java process", msg)
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
        match ubuntu_instance.docker_server_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} docker server version {ubuntu_instance.capabilities['docker_server_version']}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} docker server version", msg)
            case _:
                print_unkown(f"{ubuntu_instance} docker server version")

    def check_docker_client_version_ok(self, ubuntu_instance):
        match ubuntu_instance.docker_client_version_ok():
            case [True,msg]:
                print_ok(f"{ubuntu_instance} docker server version {ubuntu_instance.capabilities['docker_client_version']}")
            case [_,msg]:
                print_fail(f"{ubuntu_instance} docker server version", msg)
            case _:
                print_unkown(f"{ubuntu_instance} docker server version")

    def check_capabilities(self, ubuntu_instance):
        for capability in ubuntu_instance.capabilities.items():
            match capability:
                case ('docker_client_version', _):
                    self.check_docker_client_version_ok(ubuntu_instance)
                case ('docker_server_version', _):
                    self.check_docker_server_version_ok(ubuntu_instance)
                case ('container_service', _):
                    self.check_docker_service_ok(ubuntu_instance)
                case ('java_version', _):
                    self.check_java_version_ok(ubuntu_instance)
                case ('java_process', _):
                    self.check_java_ps_ok(ubuntu_instance)
                case ('time_service', time_service):
                    match time_service:
                        case 'ntp':
                            self.check_ntp_ok(ubuntu_instance)
                        case 'timesyncd':
                            self.check_timesyncd_ok(ubuntu_instance)
                        case _:
                            print_unkown(f"{ubuntu_instance} time_service capability not defined")
                case _:
                    print("No capabilities defined in node object")
    
    def check_operational_limits(self, ubuntu_instance):
        for limit in ubuntu_instance.operational_limits.items():
            match limit:
                case ('cpu', percentage):
                    print(f"cpu {percentage}")
                case ('mem', percentage):
                    print(f"mem {percentage}")
                case ('container_service', percentage):
                    print(f"container_service {percentage}")
                case ('jvm_heap', percentage):
                    print(f"work in progress ... jvm_heap {percentage}")
                case ('jvm_stack', percentage):
                    print(f"work in progress ... jvm_stack {percentage}")
                case ('mount_points', mount_point_limits):
                    for mount_point, limit in mount_point_limits.items():
                        print(f"mount_point_limit {mount_point} {limit}%")
                        match ubuntu_instance.mount_path_usage_ok(mount_point, limit):
                            case [True,msg]:
                                print_ok(f"{ubuntu_instance} mount point {mount_point} within {limit}%")
                            case [_,msg]:
                                print_fail(f"{ubuntu_instance} mount point {mount_point}", msg)
                            case _:
                                print_unkown(f"{ubuntu_instance} mount point")
                case _:
                    print("No operational limits defined in node object")
        # self.check_mount_ok(ubuntu_instance, "/")
        #  self.check_mount_path_usage_ok(ubuntu_instance, mount_path="/", usage_limit=70)

    def check_all(self, ubuntu_instance):
        # self.check_capabilities(ubuntu_instance)
        self.check_operational_limits(ubuntu_instance)
    
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
demo.run()
# demo.debug()