import os
from pprint import pprint
from contract.consumer import I


def test_consumer_json_generation():
    users_list_expectation_response = [
        {"user": {"name": "felipe"}},
        {"user": {"name": "john"}},
    ]

    consumer = (I("billing-api").interacts_with("users-api").
                to("get one user").
                when("user exists").
                with_request('get', '/v1/users/USR9CE111CDAED0/',
                             headers={"Authorization": "Token xpto"}).
                expecting_response(200, body={"results": {"user": {"name": "felipe"}}}).done().

                to("get all users").
                when("a list of users exists").
                with_request('get', '/v1/users/',
                             headers={"Authorization": "Token xpto"}).
                expecting_response(200, body={"results": users_list_expectation_response}).done())

    result = consumer.ok()
    assert result is not None

    expected = {'consumer': {'name': 'billing-api'},
                'interactions': [{'description': 'get one user',
                                  'provider_state': 'user exists',
                                  'request': {'headers': {'Authorization': 'Token xpto'},
                                                    'method': 'get', 'path': '/v1/users/USR9CE111CDAED0/'},
                                  'response': {'body': {'results': {'user': {'name': 'felipe'}}},
                                               'status': 200, 'headers': {}}},

                                 {'description': 'get all users',
                                  'provider_state': 'a list of users exists',
                                  'request': {'headers': {'Authorization': 'Token xpto'},
                                              'method': 'get', 'path': '/v1/users/'},
                                  'response': {'body': {'results': [{'user': {'name': 'felipe'}},
                                                                    {'user': {'name': 'john'}}]},
                                               'status': 200, 'headers': {}}},
                                 ],
                'provider': {'name': 'users-api'}}

    assert result == expected
    consumer.write(pact_dir='tests/pacts')
    assert os.path.isfile('tests/pacts/billing_api__users_api.json')
