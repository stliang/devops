import sys
from common.ubuntu import Ubuntu
from common.report import *
from common.file_helper import *
import re

# This UbuntuHealthCheck class work with defined operation limits.  Prometheus node_exporter
# should do the samething.  Absent of that, use UbuntuHealthCheck.
class UbuntuHealthCheck(Ubuntu):

    def __init__(self, host_address, username, password, operational_limits={}, **kwargs):
        Ubuntu.__init__(self, host_address, username, password, **kwargs)
        self.operational_limits = operational_limits

    def set_health_check_state(self, state):
        self.set_state(state | {'operational_limits': self.operational_limits})

    def docker_service_ok(self) -> [bool, str]:
        output = self.docker_service()
        return ["active (running)" in output, output]

    def docker_server_version_ok(self) -> [bool, str]:
        output = self.docker_server_version()
        match self.capabilities:
            case {'docker_server_version': version}:
                return [version in output, output]
            case _:
                return [False, "Docker capability not defined in node object"]

    def docker_client_version_ok(self) -> [bool, str]:
        output = self.docker_client_version()
        match self.capabilities:
            case {'docker_client_version': version}:
                return [version in output, output]
            case _:
                return [False, "Docker capability not defined in node object"]


    def mount_ok(self, mount_path) -> [bool, str]:
        output = self.findmnt_verify()
        # return ["Success, no errors or warnings detected" in findmnt and mount_path in findmnt, findmnt]
        return [mount_path in output, output]

    def systemd_timesyncd_ok(self) -> [bool, str]:
        output = self.systemd_timesyncd()
        # return ["active (running)" in output and "Synchronized to time server" in output, output]
        return ["active (running)" in output, output]

    def ntp_ok(self) -> [bool, str]:
        output = self.ntp()
        return ["active (running)" in output, output]

    # sample java version output: openjdk version "11.0.17" 2022-10-18
    def java_version_ok(self) -> [bool, str]:
        output = self.java_version()
        match self.capabilities:
            case {'java_version': version}:
                return [version in output, output]
            case _:
                return [False, "Java capability not defined in node object"]

    # sample jps output: java-11-openjdk-amd64
    def java_ps_ok(self) -> [bool, str]:
        output = self.jps()
        match self.capabilities:
            case {'java_process': version}:
                return [version in output, output]
            case _:
                return [False, "Java process capability not defined in node object"]

    def mount_path_usage_ok(self, mount_path, usage_limit) -> [bool, str]:
        output = self.df_h()
        # get max usage
        lines = output.split("\n")
        # If root mount usage is not found, then current usage is consider to be zero
        current_usage = 0
        for line in lines:
            tokens = line.split()
            if tokens[len(tokens)-1] == mount_path:
                current_usage = int(tokens[len(tokens)-2].rstrip('%'))
                break
        return [usage_limit > current_usage, output]

# Linux 5.15.0-52-generic (jenkins-vi5) 	02/17/2023 	_x86_64_	(8 CPU)

# 03:27:05 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
# 03:27:05 PM  all    1.36    0.01    0.60    0.01    0.00    0.01    0.00    0.00    0.00   98.01
# 03:27:05 PM    0    1.96    0.01    0.73    0.01    0.00    0.01    0.00    0.00    0.00   97.28
# 03:27:05 PM    1    1.63    0.01    0.65    0.01    0.00    0.01    0.00    0.00    0.00   97.70
# 03:27:05 PM    2    1.37    0.01    0.59    0.01    0.00    0.01    0.00    0.00    0.00   98.02
# 03:27:05 PM    3    1.28    0.01    0.58    0.01    0.00    0.00    0.00    0.00    0.00   98.12
# 03:27:05 PM    4    1.17    0.00    0.56    0.01    0.00    0.00    0.00    0.00    0.00   98.25
# 03:27:05 PM    5    1.15    0.01    0.57    0.01    0.00    0.00    0.00    0.00    0.00   98.26
# 03:27:05 PM    6    1.16    0.01    0.57    0.02    0.00    0.01    0.00    0.00    0.00   98.23
# 03:27:05 PM    7    1.18    0.01    0.58    0.01    0.00    0.04    0.00    0.00    0.00   98.18
    # sample jps output: java-11-openjdk-amd64
    def cpu_usage_ok(self, usage_limit) -> [bool, str]:
        output = self.jps()
        match self.capabilities:
            case {'java_process': version}:
                return [version in output, output]
            case _:
                return [False, "Java process capability not defined in node object"]
    
#                   total        used        free      shared  buff/cache   available
# Mem:       32744528     2605840    19308660       41124    10830028    29649336
# Swap:       2097148       33024     2064124
