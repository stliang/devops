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

    def run(self):
        for ubuntu_instance in self.ubuntu_instances:
            print(f"Short_Name,Address,Root_Mount_Size,Memory,CPU")
            df_h = ubuntu_instance.df_h()
            lines = df_h.split("\n")
            lines.pop(0)
            for line in lines:
                # print(f"{line}")
                xs = line.split()
                if "/" == xs[len(xs) - 1]:
                    print(f"{ubuntu_instance.short_name},{ubuntu_instance.host_address},{xs[1]}")

# Demo Ubuntu get root mount disk size
my_nodes = deserialized_nodes()
demo = Demo(my_nodes)
demo.run()