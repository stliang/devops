import sys
from common.ubuntu import Ubuntu
from common.report import *
from common.file_helper import *
import re

class UbuntuHealthCheck(Ubuntu):

    def __init__(self, host_address, username, password, usage_limits={}, **kwargs):
        Ubuntu.__init__(self, host_address, username, password, **kwargs)
        self.usage_limits = usage_limits

    def set_health_check_state(self, state):
        self.set_state(state | {'usage_limits': self.usage_limits})

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
            case {'java_version': version}:
                p = re.compile('(\d+).\d+.\d+')
                m = p.match(output)
                major_version = m.group(1)
                return [major_version in output, output]
            case _:
                return [False, "Java capability not defined in node object"]

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