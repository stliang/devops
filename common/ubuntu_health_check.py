import sys
from common.ubuntu import Ubuntu
from common.report import *
from common.file_helper import *

class UbuntuHealthCheck(Ubuntu):

    def mount_ok(self, mount_path) -> [bool, str]:
        findmnt = self.findmnt_verify()
        # return ["Success, no errors or warnings detected" in findmnt and mount_path in findmnt, findmnt]
        return [mount_path in findmnt, findmnt]

    def systemd_timesyncd_ok(self) -> [bool, str]:
        output = self.systemd_timesyncd()
        # return ["active (running)" in output and "Synchronized to time server" in output, output]
        return ["active (running)" in output, output]

    def ntp_ok(self) -> [bool, str]:
        output = self.ntp()
        return ["active (running)" in output, output]