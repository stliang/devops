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
        # for k, v in operational_limits.items():
        #     operational_limits[k] = float(v)
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
                return []

    def docker_client_version_ok(self) -> [bool, str]:
        output = self.docker_client_version()
        match self.capabilities:
            case {'docker_client_version': version}:
                return [version in output, output]
            case _:
                return []

    # def mount_ok(self, mount_path) -> [bool, str]:
    #     output = self.findmnt_verify()
    #     return [mount_path in output, output]

    def systemd_timesyncd_ok(self) -> [bool, str]:
        output = self.systemd_timesyncd()
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
                return []

    # sample jps output: java-11-openjdk-amd64
    def java_ps_ok(self) -> [bool, str]:
        output = self.jps()
        match self.capabilities:
            case {'java_process': version}:
                return [version in output, output]
            case _:
                return []

    def mount_path_usage_ok(self) -> [[bool, str]]:
        return_value = []
        output = self.df_h()
        lines = output.split("\n")
        match self.operational_limits:
            case {'mount_points': mount_point_limits}:
                for mount_point, limit in mount_point_limits.items():
                    for line in lines:
                        tokens = line.split()
                        if tokens[len(tokens)-1] == mount_point:
                            current_usage = float(tokens[len(tokens)-2].rstrip('%'))
                            if current_usage < limit:
                                return_value.append([True, f'{mount_point} within {limit}%'])
                            else:
                                return_value.append([False, f'{mount_point} exceeded {limit}%'])
                            break
        return return_value

    def cpu_usage_ok(self) -> [bool, str]:
        match self.operational_limits:
            case {'cpu': limit}:
                output = self.mpstat()
                lines = output.split("\n")
                for line in lines:
                    if 'all' in line:
                        xs = line.split()
                        current_cpu_usage = 100 - float(xs[len(xs)-1])
                        if current_cpu_usage < limit:
                            return [True, output]
                        else:
                            return [False, output]
                return [False, output]
            case _:
                return []
    
    def mem_usage_ok(self) -> [bool, str]:
        match self.operational_limits:
            case {'mem': limit}:
                output = self.free()
                lines = output.split("\n")
                for line in lines:
                    if 'Mem:' in line:
                        xs = line.split()
                        current_mem_usage = float(xs[2])
                        total_mem = float(xs[1])
                        usage_percentage = (current_mem_usage / total_mem) * 100
                        if usage_percentage < limit:
                            return [True, output]
                        else:
                            return [False, output]
                return [False, output]
            case _:
                return []

    def time_service_ok(self) -> [bool, str]:
        match self.capabilities:
            case {"time_service": "ntp"}:
                return self.ntp_ok()
            case {"time_service": "timesyncd"}:
                return self.systemd_timesyncd_ok()
            case _:
                return []

    def container_service_ok(self) -> [bool, str]:
        match self.capabilities:
            case {"container_service": "docker"}:
                return self.docker_service_ok()
            case _:
                return []

    def sntp_ok(self, ntp_server) -> [bool, str]:
        output = self.sntp(ntp_server)
        return [not "no UCST response" in output, output]