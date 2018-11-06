import json


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
        self.interactions = [Interaction(interaction_as_dict) for interaction_as_dict in self.pact['interactions']]
