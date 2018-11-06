import json
from pprint import pprint


class Response:

    def __init__(self, response_as_dict):
        self.__as_dict = response_as_dict
        self.status = response_as_dict['status']
        self.headers = response_as_dict['headers']
        self.body = response_as_dict['body']


class Request:

    def __init__(self, request_as_dict):
        self.__as_dict = request_as_dict
        self.method = request_as_dict['method']
        self.path = request_as_dict['path']
        self.headers = request_as_dict['headers']


class Interaction:

    def __init__(self, interaction_as_dict):
        self.__as_dict = interaction_as_dict
        self.description = interaction_as_dict['description']
        self.provider_state = interaction_as_dict['providerState']
        self.request = Request(interaction_as_dict['request'])
        self.response = Response(interaction_as_dict['response'])


class ConsumerRepresentation:

    def __init__(self, pact_path):
        self.__pact_path = pact_path
        self.setup()

    def setup(self):
        self.pact = json.loads(open(self.__pact_path, 'r').read())
        self.consumer_name = self.pact['consumer']['name']
        self.provider_name = self.pact['provider']['name']
        self.interactions = [Interaction(interaction_as_dict)
                             for interaction_as_dict in self.pact['interactions']]


class Pact:

    def __init__(self, pact_path):
        self.consumer = ConsumerRepresentation(pact_path)

    def select(self, interaction_description):
        self.selected_interaction = self.consumer.interactions[0]
        return self

    def assert_it(self):
        if not self._is_ready:
            raise Exception('you have to call do_it() first')

        self.__assert_status()
        self.__assert_fields()
        self.__assert_values()

    def __assert_status(self):
        assert self.response.status_code == self.selected_interaction.response.status

    def __assert_fields(self):
        response_body = self.response.json()
        expected_keys = self.selected_interaction.response.body.keys()
        assert set(expected_keys).issubset(set(response_body.keys())), expected_keys

    def __assert_values(self):
        for key, value in self.selected_interaction.response.body.items():
            assert value == self.response.json()[key], "expected {} ; given {}".format(value, self.response.json()[key])

        return self

    def mount_request(self):
        self.url = self.selected_interaction.request.path
        self.headers = self.selected_interaction.request.headers
        self.method = self.selected_interaction.request.method
        return self

    def call(self, client):
        self.response = getattr(client, self.method)(self.url)
        return self

    def ready(self):
        self._is_ready = True
        return self

    def debug(self):
        pprint(self.response.json())
        return self
