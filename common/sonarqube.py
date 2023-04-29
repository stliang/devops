from .service import Service

class SonarQube(Service):

    # def __init__(self, service_address, username="", password="", **kwargs):
    #     Service.__init__(self, service_address, username, password, **kwargs)

    # def __str__(self):
    #     return f"{self.service_address}"

    # Example curl call
    # curl -u squ_*********************: "https://sonarqube.mycompany.com/api/measures/component?component=MyFeature&metricKeys=coverage&branch=main"
    def get_code_coverage(self, component, branch) -> [float]:
        url = f"{self.service_address}/api/measures/component?component={component}&metricKeys=coverage&branch={branch}"
        data = self.get_dict(url=url)
        print(f"DEBUG data from SonarQube:\n{data}")
        match data:
            case {'component': {'key': _, 'name': _, 'qualifier': _, 'measures': [{'metric': 'coverage', 'value': value, 'bestValue': _}],'branch': _}}:
                return [float(value)]
            case _:
                return []