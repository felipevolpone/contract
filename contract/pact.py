
from .provider import ConsumerRepresentation
from pprint import pprint


class Contract:

    def __init__(self, pact_path):
        self.consumer = ConsumerRepresentation(pact_path)

    def select(self, interaction_description):
        for interaction in self.consumer.interactions:
            if interaction.description == interaction_description:
                self.selected_interaction = interaction
                break

        if self.selected_interaction is None:
            raise Exception("There is no interaction with name {}".format(interaction_description))

        return self

    def assert_it(self):
        self.__assert_status()
        self.__assert_fields()
        # self.__assert_values()

    def __assert_status(self):
        print("expected {} ; given {}".format(self.selected_interaction.response.status,
                                              self.response.status_code))
        assert self.response.status_code == self.selected_interaction.response.status

    def __assert_fields(self):
        response_body = self.response.json()
        expected_keys = self.selected_interaction.response.body.keys()
        assert set(expected_keys).issubset(set(response_body.keys())), expected_keys

    def __assert_values(self):
        for key, value in self.selected_interaction.response.body.items():
            message = "expected {} ; given {}".format(value, self.response.json()[key])
            assert value == self.response.json()[key], message

        return self

    def call(self, client):
        self.url = self.selected_interaction.request.path
        self.headers = self.selected_interaction.request.headers
        self.method = self.selected_interaction.request.method

        if self.method != 'get':
            raise Exception("Only HTTP GET is supported for now")

        self.response = getattr(client, self.method)(self.url)
        return self

    def debug(self):
        pprint(self.response.json())
        return self
