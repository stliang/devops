# Linux node
from .node import Node

def parse_action(in_string, separator_string) -> dict:
    out = {}
    for line in in_string.splitlines():
        xs = line.split(separator_string, 1)
        if len(xs) < 2: break
        k = xs[0].strip()
        v = xs[1].replace('"', '').strip()
        out[k] = v
    return out

def parse_os_release(in_string) -> dict:
    return parse_action(in_string, "=")

def parse_hostnamectl(in_string) -> dict:
    return parse_action(in_string, ":")

class Linux(Node):

    def uname(self):
        return self.send("uname -r")

    def os_release(self) -> dict:
        return parse_os_release(self.send("cat /etc/os-release"))

    def hostnamectl(self) -> dict:
        return parse_hostnamectl(self.send("hostnamectl"))

    def efibootmgr(self):
        return self.send("efibootmgr -v")

    def show_grub_cfg(self):
        return self.send("cat /boot/grub/grub.cfg")

   def show_mount(self):
        return self.send("mount")

    def dmesg(self):
        return "TODO"