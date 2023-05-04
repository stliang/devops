import sys
sys.path.append('../')
from common.sonarqube import SonarQube
from common.report import *
from common.file_helper import *

class Demo():
    def __init__(
        self,
        address,
        username,
        test_cases
        ):
        self.test_cases = test_cases
        self.sonarqube = SonarQube(address, username)

    def check_code_coverage(self, component, branch, min) -> bool:
        match self.sonarqube.get_code_coverage(component, branch):
            case [value]:
                return value >= min
            case _:
                return False

    def test(self) -> [(bool, str)]:
        results = []
        for test_case in self.test_cases:
            match test_case:
                case {'min': min, 'component': component, 'branch': branch, 'metric_key': 'coverage'}:
                    results.append((self.check_code_coverage(component, branch, min), f"{component} {branch}"))
        return results

    def run(self):
        failures = ""
        test_results = self.test()
        for (isPass, msg) in test_results:
            if not isPass:
                failures += f"failed: {msg}; "
        if failures:
            nagios_report("CRITICAL", f"Code coverage {failures}")
        else:
            nagios_report("OK", "All branches in components passed code coverage gate")

# Demo code coverage test
sonarqube_tests = deserialized_sonarqube_tests()
demo = Demo(**sonarqube_tests)
demo.run()