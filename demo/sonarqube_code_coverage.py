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
        print(f"calling sonarqube get_code_coverage with {component}, {branch}, {min}")
        match self.sonarqube.get_code_coverage(component, branch):
            case [value]:
                return value >= min
            case _:
                return False

    def run(self) -> [bool]:
        for test_case in self.test_cases:
            print(f"DEBUG test_case:\n{test_case}")
            match test_case:
                case {'min': min, 'component': component, 'branch': branch, 'metric_key': 'coverage'}:
                    return [self.check_code_coverage(component, branch, min)]
                case _:
                    return []

# Demo code coverage test
sonarqube_tests = deserialized_sonarqube_tests()

# sonarqube_tests YAML file example:
# address: https://sonarqube.mycompany.com
# username: squ_*****************************
# test_cases:
#   - {min: 75.0, component: FeatureA, branch: main, metric_key: coverage}
print(sonarqube_tests)

demo = Demo(**sonarqube_tests)
demo.run()