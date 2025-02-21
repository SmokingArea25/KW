import requests


class RequestHandler:
    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method, url, headers=None, json=None):
        method = method.lower()
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=json
        )
        return response
