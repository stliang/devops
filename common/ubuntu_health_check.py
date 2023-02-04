import sys
from common.ubuntu import Ubuntu
from common.report import *
from common.file_helper import *

class UbuntuHealthCheck(Ubuntu):

    def docker_ok(self) -> [bool, str]:
        output = self.docker()
        return ["active (running)" in output, output]

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
    def java_version_ok(self, java_version) -> [bool, str]:
        output = self.java_version()
        return [java_version in output, output]

    # sample jps output: java-11-openjdk-amd64
    def java_ps_ok(self, java_version) -> [bool, str]:
        output = self.jps()
        return [java_version in output, output]

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