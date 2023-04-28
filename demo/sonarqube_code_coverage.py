import sys
sys.path.append('../')
from common.sonarqube import SonarQube
# from common.report import *
# from common.file_helper import *

class Demo():
    def __init__(
        self,
        sonarqube_url,
        code_coverage_test_list
        ):
        self.sonarqube_url = sonarqube_url
        self.code_coverage_test_list = code_coverage_test_list

    def check_code_coverage(self, code_coverage_test_list):
        return []

    def run(self):
        return []

# Demo code coverage test
code_coverage_metadata = deserialized_code_coverage_metadata()
demo = Demo(code_coverage_metadata["sonarqube_url"], code_coverage_metadata["list"])
demo.run()