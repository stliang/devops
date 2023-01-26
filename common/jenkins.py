# Jenkins node with CLI

# Assumptions
# 1.) Jenkins node is also a Ubuntu node
# 2.) Jenkins node is a remote node with ssh support
# 3.) Jenkins CLI Java client is installed.  Note that python-jenkins library is not used because library can be out of date and for better security control
# 4.) Jenkins node is either a controller or an agent with docker engine
from .ubuntu import Ubuntu

class Jenkins(Ubuntu):

    # Supper ars: host_address, username, password, port=22,  try *args
    def __init__(self, host_address, username, password, short_name="Jenkins", jenkins_url="", **kwargs):
        Ubuntu.__init__(self, host_address, username, password, short_name, **kwargs)
        match jenkins_url:
            case "":
                self.jenkins_url = f"http://{self.host_address}"
            case _:
                self.jenkins_url = jenkins_url

    def __str__(self):
        return f"{self.short_name} {self.jenkins_url} {self.host_address}:{self.port}"

    def get_job(self, folder, job_name):
        # java -jar jenkins-cli.jar -s <Jenkins Address> -auth <key> get-job <Folder>/<Job Name> > <Job Name>.xml
        return ""

    # Check docker usage of host disk

    # Delete docker containers whithout tag