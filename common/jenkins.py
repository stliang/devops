# Jenkins node with CLI

# Assumptions
# 1.) Jenkins node is also a Ubuntu node
# 2.) Jenkins node is a remote node with ssh support
# 3.) Jenkins CLI Java client is installed.  Note that python-jenkins library is not used because library can be out of date and for better security control
# 4.) Jenkins node is either a controller or an agent with docker engine
from .ubuntu import Ubuntu

class Jenkins(Ubuntu):

    def __init__(self, host_address, username, password, jenkins_auth="", short_name="Jenkins", jenkins_url="", **kwargs):
        Ubuntu.__init__(self, host_address, username, password, short_name, **kwargs)
        self.jenkins_auth = jenkins_auth
        match jenkins_url:
            case "":
                self.jenkins_url = f"http://{self.host_address}"
            case _:
                self.jenkins_url = jenkins_url

    def __str__(self):
        return f"{self.short_name} {self.jenkins_url} {self.host_address}:{self.port}"

    def get_job(self, job_path):
        return self.send(f"java -jar jenkins-cli.jar -s {self.jenkins_url} -auth {self.jenkins_auth} get-job {job_path}")

    def list_jobs(self, view_name="") -> [str]:
        match view_name:
            case "":
                cmd = f"java -jar jenkins-cli.jar -s {self.jenkins_url} -auth {self.jenkins_auth} list-jobs"
                return self.send(cmd).split()
            case _:
                cmd = f"java -jar jenkins-cli.jar -s {self.jenkins_url} -auth {self.jenkins_auth} list-jobs {view_name}"
                return self.send(cmd).split()

    # Check docker usage of host disk

    # Delete docker containers whithout tag