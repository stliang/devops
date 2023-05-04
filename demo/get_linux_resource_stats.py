import re
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

def parse_resource_output(console_msg, line_key_reg, line_item_index):
    p = re.compile(line_key_reg)
    value = ""
    lines = console_msg.split("\n")
    for line in lines:
        if p.match(line):
            xs = line.split()
            value = xs[line_item_index]
            break
    return value

class Demo():
    def __init__(
        self,
        nodes
        ):
        self.nodes = nodes
        self.ubuntu_instances = list(map(lambda node: UbuntuHealthCheck(**node), self.nodes))

    def run(self):
        print(f"Short_Name,Address,Root_Mount_Size,Memory,CPU")
        for ubuntu_instance in self.ubuntu_instances:
            disk_size = ""
            mem_size = ""
            cpu_count = ""
            df_h = ubuntu_instance.df_h()
            free_h = ubuntu_instance.free_h()
            lscpu = ubuntu_instance.lscpu()
            disk_size = parse_resource_output(df_h, ".*/$", 1)
            mem_size = parse_resource_output(free_h, "^Mem:.*", 1)
            cpu_count = parse_resource_output(lscpu, "^CPU\(s\):.*", 1)
            print(f"{ubuntu_instance.short_name},{ubuntu_instance.host_address},{disk_size},{mem_size},{cpu_count}")

# Demo Ubuntu get system resource stats
my_nodes = deserialized_nodes()
demo = Demo(my_nodes)
demo.run()