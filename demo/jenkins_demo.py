import sys
sys.path.append('../')
from common.jenkins import Jenkins
from common.report import *
from common.file_helper import *
from pathlib import Path

class Demo():
    def __init__(
        self,
        node # {short_name: host_1, host_address: x.x.x.x, port: 22, username: ***, password: ***, jenkins_auth: *** jenkins_url: http://... }
        ):
        self.jenkins = Jenkins(**node)

    def save_jobs(self):
        views = self.jenkins.list_jobs()
        for view in views:
            # TODO: should check if view is a folder and use recursion to find the final job
            jobs = demo.jenkins.list_jobs(view)
            if len(jobs):
                dir = f"{Path.home()}/tmp/{view}"
                Path(dir).mkdir(parents=True, exist_ok=True)
                for job in jobs:
                    job_xml = demo.jenkins.get_job(f"{view}/{job}")
                    with open(f"{dir}/{job}", 'w') as file:
                        file.write(job_xml)
            else:
                # this view is a job
                dir = f"{Path.home()}/tmp"
                job_xml = demo.jenkins.get_job(view)
                with open(f"{dir}/{view}", 'w') as file:
                    file.write(job_xml)

my_nodes = deserialized_jenkins_nodes()
this_jenkins = my_nodes[0]
demo_jenkins = Demo(this_jenkins)
demo_jenkins.save_jobs()
