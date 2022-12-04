# Jenkins on Linux node
from .node import Node

class Jenkins(Node):

    def __str__(self):
        return f"{self.short_name} {self.host_address}:{self.port}"