# Jenkins node with CLI

# Assumptions
# 1.) Jenkins node is also a Ubuntu node
# 2.) Jenkins node is a remote node with ssh support
# 3.) Jenkins CLI Java client is installed.  Note that python-jenkins library is not used because library can be out of date and for better security control
# 4.) Jenkins node is either a controller or an agent with docker engine
import os 
import re
import shutil
import time

from .ubuntu import Ubuntu

class Jenkins(Ubuntu):

    def __init__(self, host_address, username, password, jenkins_auth="", short_name="Jenkins", jenkins_url="", workspace="/home/jenkins/workspace", **kwargs):
        Ubuntu.__init__(self, host_address, username, password, short_name, **kwargs)
        self.jenkins_auth = jenkins_auth
        self.workspace = workspace
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

    def list_ws_dirs(self) -> [str]:
        dirs = []
        if os.path.isdir(self.workspace):
            for it in os.scandir(self.workspace):
                if it.is_dir():
                    dirs.append(it.path)
                    dirs += list_dirs(it.path)
        return dirs

    # Jenkins when using container to build creates root owned files which prevents ws clean up
    # Run this method as root would do the workspace clean up
    def ws_clean(self, dir_min_age_in_sec=1800):
        p = re.compile(".*@tmp$|.*@tmp@tmp$")
        dirs = list_ws_dirs()
        tmp_dirs = list(filter(lambda x: p.match(x), dirs))
        job_dirs = list(map(lambda y: y.split("@tmp")[0], tmp_dirs))
        # Jenkins active jobs should have two directories of either "a" and "a@tmp | a@tmp@tmp" OR "a" and "a_ws-cleanup_.*"
        # In active job should not have a directory of "a":
        inactive_job_dirs = list(filter(lambda z: not os.path.isdir(z), job_dirs))

        #print(f"DEBUG: inactive_job_dirs dict = {inactive_job_dirs}")
        for tmp_dir in tmp_dirs:
            try:
                dir_stat = os.stat(tmp_dir)
                last_modified_in_seconds = (time.time()-dir_stat.st_mtime)
                x = tmp_dir.split("@tmp")[0]
                #print(f"DEBUG: x = {x} {tmp_dir} {last_modified_in_seconds}")
                # Delete directories of finished job that are 30 minutes old
                if last_modified_in_seconds > dir_min_age_in_sec and x in inactive_job_dirs:
                    #print("DEBUG: IN IF")
                    dir_pattern = f"{x}@tmp$|{x}@tmp@tmp$|{x}_ws-cleanup_[0-9]+$"
                    pattern = re.compile(dir_pattern)
                    dirs_to_delete = list(filter(lambda x: pattern.match(x), dirs))
                    for a_dir in dirs_to_delete:
                        #print(f"DEBUG: deleting {a_dir}")
                        shutil.rmtree(a_dir)
            except FileNotFoundError:
                print("Directory does not exist, no need to delete.")