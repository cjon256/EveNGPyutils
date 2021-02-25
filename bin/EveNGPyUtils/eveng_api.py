import json

import requests
import urllib3


class EveNGAuthnticationFailure(Exception):
    pass


class EveNGServer:
    def __init__(self, base_url, headers, password, username):
        self._cookies = None
        self.base_url = base_url
        self.username = username
        self.password = password
        self.headers = headers

    def login(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = f'{self.base_url}/api/auth/login'
        data = {
            "username": self.username,
            "password": self.password,
            "html5": "-1",
        }
        login = requests.post(url=url, data=json.dumps(data), verify=False)
        if login.status_code == 200:
            self._cookies = login.cookies
        else:
            raise EveNGAuthnticationFailure(f"failed to log {self.username} into {url}")

    def list_labs(self):
        def _get_labs(directory):
            data = self.query('folders' + directory + "/")
            labs = []
            for lab in data['data']['labs']:
                labs.append(f"{lab['path']}")
            for folder in data['data']['folders']:
                # for some reason it does not like to list Running
                if folder['name'] == "Running":
                    continue
                # only going down the folder tree
                if folder['name'] == "..":
                    continue
                labs.extend(_get_labs(f"{directory}{folder['path']}"))
            return labs
        return _get_labs("")

    def query(self, url):
        if self._cookies is None:
            self.login()
        url = f'{self.base_url}/api/' + url
        import pdb
#        pdb.set_trace()
        nodes = requests.get(
            url=url,
            headers=self.headers,
            cookies=self._cookies,
            verify=False)
        response = nodes.json()
        return response


class EveNGTopology:
    def __init__(self, server, name):
        self.server = server
        self.name = name

    def start_all_singly(self):
        result = self.list_nodes()
        for node in result['data'].keys():
            # XXX need to collect the results and give some sort of feedback
            self.server.query(f'labs/{self.name}/nodes/{node}/start')

    def start_all(self):
        """
        For Whatever reason this did not seem to want to work for me.
        Thus the above function that does the same thing by more slowly
        """
        return self.server.query(f'labs/{self.name}/nodes/start')

    def stop_all(self):
        return self.server.query(f'labs/{self.name}/nodes/stop')

    def wipe_all_singly(self):
        result = self.list_nodes()
        for node in result['data'].keys():
            # XXX need to collect the results and give some sort of feedback
            self.server.query(f'labs/{self.name}/nodes/{node}/wipe')

    def wipe_all(self):
        """
        For Whatever reason this did not seem to want to work for me.
        Thus the above function that does the same thing by more slowly
        """
        return self.server.query(f'labs/{self.name}/nodes/wipe')

    def list_nodes(self):
        return self.server.query(f'labs/{self.name}/nodes')
