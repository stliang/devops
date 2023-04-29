import json
import requests

from requests.auth import HTTPBasicAuth

class Service(object):
    def __init__(self, service_address, username="", password="", timeout=(5, 15), **kwargs):
        self.service_address = service_address
        self.username = username
        self.password = password
        self.timeout = timeout
        self.__dict__.update(kwargs) # in case childern want to access their kwargs
        self.extra_kwargs = kwargs # for __str__ as I don't want to show credential

    def __str__(self):
        return f"{self.service_address} {self.extra_kwargs}"

    def get_dict(self, url="") -> dict:
        my_url=url if url else self.service_address
        try:
            response = requests.get(
                url=my_url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=self.timeout
            )
            data = response.json()
            return data
        except Exception:
            return {}