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

    def blkid(self):
        return self.send("blkid")

    # checks fstab works or not
    def findmnt_verify(self):
        return self.send("sudo findmnt --verify --verbose") # file system type read needs sudo
    
    def fstab(self):
        return self.send("cat /etc/fstab")

   def journalctl_kernel(self):
        return self.send("journalctl -k --no-pager")

    # TODO test to see if this command finds "failed for Local File Systems"
    def journalctl_errors(self):
        return self.send("journalctl -p 3 -xb --no-pager")

    def tainted_state(self):
        return self.send("cat /proc/sys/kernel/tainted")

    # def var_log_journal_exists(self) -> Boolean:
    #     return self.send("ls -l /var/log/journal") # /etc/systemd/journald.conf with Storage=auto would need journal dir across reboot

    def journal_disk_usage(self):
        return self.send("journalctl --disk-usage")

    def journal_list_boots(self):
        return self.send("journalctl --list-boots --no-pager")

    def boot_log(self):
        return self.send("sudo cat /var/log/boot.log")

    def systemctl_status(self, unit):
        return self.send("systemctl status -l {unit}") # TODO test

    def systemctl_state(self, state):
        return self.send("systemctl --state={state} --no-pager --no-legend")

    def systemctl_failed(self):
        self.systemctl_state("failed")

    def systemctl_default_target(self):
        self.send("systemctl get-default")

    def dmesg(self):
        return "TODO"