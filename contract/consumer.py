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



class I:

    def __init__(self, consumer_name):
        self.consumer_name = consumer_name

    def depends_on(self, provider_name):
        self.provider_name = provider_name
        return self

    def to(self, description):
        self.interaction_description = description
        return self

    def when(self, provider_state):
        self.interaction_provider_state = provider_state
        return self

    def with_request(self, method, path, headers=None):
        self.request_method = method
        self.request_path = path
        self.request_headers = headers
        return self

    def expecting_response(self, response_status, body={}):
        self.response_status = response_status
        self.response_body = body
        return self

    def done(self):
        interaction = InteractionToJson(provider_state=self.interaction_provider_state,
                                        description=self.interaction_description)
        request = RequestToJson(method=self.request_method, path=self.request_path, headers=self.request_headers)
        response = ResponseToJson(status=self.response_status, body=self.response_body)

        interaction_json = interaction.to_json()
        interaction_json['request'] = request.to_json()
        interaction_json['response'] = response.to_json()
        self._as_json = {'interactions': [interaction_json], 'consumer': {'name': self.consumer_name},
                         'provider': {'name': self.provider_name}}
        return self._as_json

    def to_json(self):
        return json.dumps(self._as_json)