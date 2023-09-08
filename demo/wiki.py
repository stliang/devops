import os
import re
import sys

sys.path.append('../')
from atlassian import Confluence
from common.ubuntu_health_check import UbuntuHealthCheck
from common.file_helper import *

def parse_resource_output(console_msg, line_key_reg, line_item_index):
    p = re.compile(line_key_reg)
    value = "N/A"
    lines = console_msg.split("\n")
    for line in lines:
        # print(line)
        if p.match(line):
            # print(f"MATCHED: {line}")
            xs = line.split()
            # print(f"SPLITED: {xs}")
            value = xs[line_item_index]
            break
    return value
    
class Demo(object):
    def __init__(self, nodes, wiki_address, bearer_token, page_id=None, page_parent_id=None, port=443):
        self.wiki_address = wiki_address
        self.port = port
        self.bearer_token = bearer_token
        self.page_parent_id = page_parent_id
        self.page_id = page_id
        self.confluence = Confluence(url=f'{self.wiki_address}:{self.port}/confluence', token=self.bearer_token)
        self.nodes = nodes
        self.ubuntu_instances = list(map(lambda node: UbuntuHealthCheck(**node), self.nodes))

    def set_page_id(self, page_id):
        self.page_id = page_id
    
    def get_page_id(self):
        return self.page_id

    def update_csv(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)
        self.confluence.attach_file(filename, page_id=self.page_id)

    def run(self):
        content = ["Short_Name,Address,IPMI_LAN,Root_Mount_Size,Root_Mount_Usage,Memory,CPU,Build_Node_Type"]
        for ubuntu_instance in self.ubuntu_instances:
            disk_size = ""
            mem_size = ""
            cpu_count = ""
            df_h = ubuntu_instance.df_h()
            free_h = ubuntu_instance.free_h()
            lscpu = ubuntu_instance.lscpu()
            ipmi_lan = ubuntu_instance.ipmi_lan()
            disk_size = parse_resource_output(df_h, ".*/$", 1)
            disk_usage = parse_resource_output(df_h, ".*/$", 4)
            ipmi_ip = parse_resource_output(ipmi_lan, "^IP Address\s+:.*", 3)
            mem_size = parse_resource_output(free_h, "^Mem:.*", 1)
            cpu_count = parse_resource_output(lscpu, "^CPU\(s\):.*", 1)
            content.append(f"{ubuntu_instance.short_name},{ubuntu_instance.host_address},{ipmi_ip},{disk_size},{disk_usage},{mem_size},{cpu_count},{ubuntu_instance.build_node_type}")
        print('\n'.join(content))
        self.update_csv(
            filename="test_file.csv",
            content='\n'.join(content)
            )

# Demo Ubuntu get system resource stats
my_nodes = deserialized_nodes()
demo = Demo(
    nodes=my_nodes,
    wiki_address=os.environ['WIKI_URL'],
    bearer_token=os.environ['TOKEN'],
    page_id=733028762
    )
demo.run()