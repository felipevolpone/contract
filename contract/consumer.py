import json


class PropertieableJson:
    def __init__(self, *args, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def to_json(self):
        return vars(self)


class InteractionToJson(PropertieableJson):
    pass


class RequestToJson(PropertieableJson):
    pass


class ResponseToJson(PropertieableJson):
    pass


class Interaction:

    def __init__(self, description, am_instance=None):
        self.description = description
        self.am_instance = am_instance

    def when(self, provider_state):
        self.interaction_provider_state = provider_state
        return self

    def with_request(self, method, path, headers=None):
        self.request_method = method
        self.request_path = path
        self.request_headers = headers
        return self

    def expecting_response(self, response_status, body=None, headers=None):
        self.response_status = response_status
        self.response_body = body if body else {}
        self.response_headers = headers if headers else {}
        return self

    def done(self):
        return self.am_instance

    def to_json(self):
        interaction = InteractionToJson(
                provider_state=self.interaction_provider_state,
                description=self.description
        )

        request = RequestToJson(
            method=self.request_method,
            path=self.request_path,
            headers=self.request_headers
        )

        response = ResponseToJson(
            status=self.response_status,
            body=self.response_body,
            headers=self.response_headers
        )

        interaction_json = interaction.to_json()
        interaction_json['request'] = request.to_json()
        interaction_json['response'] = response.to_json()
        return interaction_json


class I:

    def __init__(self, consumer_name):
        self.consumer_name = consumer_name
        self._interactions = []

    def interacts_with(self, provider_name):
        self.provider_name = provider_name
        return self

    def to(self, description):
        interaction = Interaction(description=description, am_instance=self)
        self._interactions.append(interaction)
        return interaction

    def ok(self):
        interactions_as_json = []

        for interaction in self._interactions:
            interactions_as_json.append(interaction.to_json())

        return {'interactions': interactions_as_json,
                'consumer': {'name': self.consumer_name},
                'provider': {'name': self.provider_name}}

    def write(self, pact_dir='contracts'):
        pact_namefile = (
                '{}__{}'.
                format(self.consumer_name, self.provider_name)
                .replace('-', '_')
        )
        with open('{}/{}.json'.format(pact_dir, pact_namefile), 'w') as pact_file:
            pact_file.write(json.dumps(self.ok(), indent=4))
