
import pytest


class response:

    def __init__(self, status, response_body):
        self.status = 200
        self.response_body = response_body

    @property
    def status_code(self):
        return self.status

    def json(self):
        return self.response_body


class client_http:

    def __init__(self, status, response_body):
        self.status = status
        self.response_body = response_body

    def get(self, url):
        return response(self.status, self.response_body)

