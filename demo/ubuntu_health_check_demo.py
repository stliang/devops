import sys
sys.path.append('../')
from common.ubuntu_health_check import UbuntuHealthCheck
from common.report import *
from common.file_helper import *

def print_check_result(description, result):
    match result:
        case [True,_]:
            print_ok(description)
        case [False,console_output]:
            print_fail(description, console_output)
        case _:
            print_unkown(description)

class Demo():
    def __init__(
        self,
        nodes
        ):
        self.nodes = nodes
        self.ubuntu_instances = list(map(lambda node: UbuntuHealthCheck(**node), self.nodes))

    def check_mount_path_usage_ok(self, ubuntu_instance):
        results = ubuntu_instance.mount_path_usage_ok()
        for result in results:
            print_check_result("mount path usage", result)

    def check_capabilities(self, ubuntu_instance):
        for capability in ubuntu_instance.capabilities.items():
            match capability:
                case ('docker_client_version', _):
                    print_check_result("docker client version", ubuntu_instance.docker_client_version_ok())
                case ('docker_server_version', _):
                    print_check_result("docker server version", ubuntu_instance.docker_server_version_ok())
                case ('container_service', _):
                    print_check_result("container service", ubuntu_instance.container_service_ok())
                case ('java_version', _):
                    print_check_result("java version", ubuntu_instance.java_version_ok())
                case ('java_process', _):
                    print_check_result("java process", ubuntu_instance.java_ps_ok())
                case ('time_service', _):
                    print_check_result("time service", ubuntu_instance.time_service_ok())
                case _:
                    print("No capabilities defined in node object")
    
    def check_operational_limits(self, ubuntu_instance):
        for limit in ubuntu_instance.operational_limits.items():
            match limit:
                case ('cpu', _):
                    print_check_result("CPU utilization", ubuntu_instance.cpu_usage_ok())
                case ('mem', percentage):
                    print_check_result("Memory utilization", ubuntu_instance.mem_usage_ok())
                case ('jvm_heap', percentage):
                    print(f"work in progress ... jvm_heap {percentage}")
                case ('jvm_stack', percentage):
                    print(f"work in progress ... jvm_stack {percentage}")
                case ('mount_points', _):
                    self.check_mount_path_usage_ok(ubuntu_instance)
                case _:
                    print("No operational limits defined in node object")

    def check_sntp_ok(self, ubuntu_instance, ntp_server):
        result = ubuntu_instance.sntp_ok(ntp_server)
        match result:
            case (True, output):
                print_check_result("sntp can reach {ntp_server}: ", output)
            case _:
                print("sntp can not reach {ntp_server}")

    def check_time_drift_from_controller_ok(self, ubuntu_instance):
        result = ubuntu_instance.time_drift_from_controller_ok()
        print_check_result("Time drift check", result)

    def check_all(self, ubuntu_instance):
        print(f"\nChecking {ubuntu_instance}")
        self.check_capabilities(ubuntu_instance)
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

    def debug_sntp(self):
        for ubuntu_instance in self.ubuntu_instances:
            self.check_sntp_ok(ubuntu_instance, "10.44.36.11")

    def debug_time_drift(self):
        for ubuntu_instance in self.ubuntu_instances:
            self.check_time_drift_from_controller_ok(ubuntu_instance)

# Demo Ubuntu Health Check on Jenkins Nodes
my_nodes = deserialized_jenkins_nodes()
demo = Demo(my_nodes)
# demo.run()
# demo.debug()
# demo.debug_sntp()
demo.debug_time_drift()