# Ubuntu Linux node
from .node import Node
from datetime import datetime
import re

def parse_action(in_string, separator_string) -> dict:
    out = {}
    for line in in_string.splitlines():
        xs = line.split(separator_string, 1)
        if len(xs) < 2: break
        k = xs[0].strip()
        v = xs[1].replace('"', '').strip()
        out[k] = v
    return out

def parse_console_output(console_msg, line_key_reg, line_item_index):
    p = re.compile(line_key_reg)
    value = ""
    lines = console_msg.split("\n")
    for line in lines:
        if p.match(line):
            xs = line.split()
            value = xs[line_item_index]
            break
    return value

def parse_os_release(in_string) -> dict:
    return parse_action(in_string, "=")

def parse_hostnamectl(in_string) -> dict:
    return parse_action(in_string, ":")

def systemctl_enable_str(service_name) -> str:
    return f"sudo systemctl enable {service_name} --no-pager"

def systemctl_disable_str(service_name) -> str:
    return f"sudo systemctl disable {service_name} --no-pager"

def systemctl_start_str(service_name) -> str:
    return f"sudo systemctl start {service_name} --no-pager"

def systemctl_stop_str(service_name) -> str:
    return f"sudo systemctl stop {service_name} --no-pager"

def systemctl_restart_str(service_name) -> str:
    return f"sudo systemctl restart {service_name} --no-pager"

def systemctl_status_str(service_name) -> str:
        return f"sudo systemctl status {service_name} --no-pager"

class Ubuntu(Node):

    def __init__(self, host_address, username, password, short_name="Ubuntu", capabilities={}, **kwargs):
        Node.__init__(self, host_address, username, password, **kwargs)
        self.short_name = short_name
        self.capabilities = capabilities
        self.state = {}

    def __str__(self):
        return f"{self.short_name} {self.host_address}:{self.port}"

    def get_datetime(self) -> datetime:
        datatime1 = self.send('date "+%Y;%m;%d;%H;%M;%S"')
        datatime2 = datatime1.strip(";").split(";")
        datetime3 = tuple(map(int, datatime2))
        # print(f"datatime1 = {datatime1}")
        # print(f"datatime2 = {datatime2}")
        # print(f"datatime3 = {datetime3}")
        datetime4 = datetime(*datetime3)
        return datetime4

    def time_drift_from_controller(self):
        # my_time is time from executing date command on remote host 
        my_time = self.get_datetime()
        # Controller is where python script is executed
        controller_time = datetime.now()
        delta = controller_time - my_time
        total_delta_seconds =  delta.total_seconds()
        # print(f"delta in seconds = {total_delta_seconds}")
        return total_delta_seconds

    def get_state(self):
        return self.state

    def get_life_capabilities(self):
        capabilities = {}
        docker_server_version = self.docker_server_version()
        if docker_server_version:
            capabilities['docker_server_version'] = docker_server_version
        docker_client_version = self.docker_client_version()
        if docker_client_version:
            capabilities['docker_client_version'] = docker_client_version
        java_version = self.java_version()
        if java_version:
            capabilities['java_version'] = java_version
        return capabilities

    def life_state(self):
        return {
            'short_name': self.short_name,
            'host_address': self.host_address,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'capabilities': self.get_life_capabilities()
        }

    def set_state(self, state):
        self.state = state

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

    def lsblk(self):
        return self.send("lsblk")

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

    def sntp(self, ntp_server):
        return self.send(f"sudo sntp -S {ntp_server}")

    def systemctl_status(self, unit):
        return self.send(f"systemctl status -l {unit}") # TODO test

    def systemctl_state(self, state):
        return self.send(f"systemctl --state={state} --no-pager --no-legend")

    def systemctl_failed(self):
        self.systemctl_state("failed")

    def systemctl_default_target(self):
        self.send("systemctl get-default")

    def systemctl_list_targets(self):
        self.send(f"systemctl list-units --type=target")

    def systemctl_set_default_target(self, target):
        self.send(f"sudo systemctl set-default {target}")

    # Activate stated target and its dependencies but deactivate all other units
    # Good for starting a rescue.target for system recovery
    def systemctl_isolate_target(self, target):
        self.send(f"sudo systemctl isolate {target}")

    def dmesg(self):
        return "TODO"

    def list_devices(self):
        return "TODO"

    def list_drivers(self):
        return "TODO"

    def dmidecode(self):
        return self.send("dmidecode")

    # use it to check if systemd is symlinked, if so, systemd is used for init system
    def sbin_init_symlink(self):
        return self.send("ls -l /sbin/init")

    def timedatectl_status(self):
        return self.send("sudo timedatectl status")

    def systemctl_action(self, service_name, cmd="status"):
        match cmd:
            case "start":
                self.send(systemctl_enable_str(service_name))
                return self.send(systemctl_start_str(service_name))
            case "stop":
                self.send(systemctl_stop_str(service_name))
                return self.send(systemctl_disable_str(service_name))
            case _:
                return self.send(systemctl_status_str(service_name))

    def systemd_timesyncd(self, cmd="status"):
        return self.systemctl_action("systemd-timesyncd.service", cmd)

    def ntp(self, cmd="status"):
        return self.systemctl_action("ntp.service", cmd)

    def date_since_epoch(self):
        return self.send("date +%s")

    def docker_service(self, cmd="status"):
        return self.systemctl_action("docker", cmd)

    def docker_version(self):
        return self.send("docker version")

    def docker_server_version(self):
        output = self.send("docker version --format '{{.Server.Version}}'")
        return output

    def docker_client_version(self):
        output = self.send("docker version --format '{{.Client.Version}}'")
        return output

    def df_h(self):
        return self.send("df -h")

    def java_version(self):
        output = self.send("java -version 2>&1 | head -n 1")
        p = re.compile('.*\"(\d+.\d+.\d+.*)\".*')
        m = p.match(output)
        return m.group(1)

    # Java Process
    def jps(self):
        return self.send("jps -v")

    def nvidia_smi(self):
        return self.send("nvidia-smi -L")

    # show CPU utilization
    def mpstat(self):
        return self.send("mpstat -P ALL")

    # show CPU utilization
    def lscpu(self):
        return self.send("lscpu")

    # show memory utilization
    def free(self):
        return self.send("free")

    # show memory utilization
    def free_h(self):
        return self.send("free -h")

    # show OS version
    def lsb_release(self):
        return self.send("lsb_release -a")

    # list services
    def list_services(self):
        return self.send("systemctl list-units --type=service --no-pager")
         
    # get service log
    def service_log(self, service_name):
        return self.send(f"sudo journalctl -u {service_name}")

    # list installed packages
    def list_installed_packages(self):
        return self.send(f"sudo apt list --installed")