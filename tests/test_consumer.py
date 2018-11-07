import json
from pprint import pprint
from contract.consumer import I


def test_consumer_json_generation():
    consumer = (I("order-split-service").interacts_with("orders-api").
                to("get one seller order").
                when("seller order exists").
                with_request('get', '/v1/seller-orders/WMT9CE111CDAED0/',
                             headers={"Authorization": "Token xpto"}).
                expecting_response(200, body={"foo": "bar"}).done().

                to("get all seller order").
                when("a list of seller order exists").
                with_request('get', '/v1/seller-orders/',
                             headers={"Authorization": "Token xpto"}).
                expecting_response(200, body={"bar": "foo"}).done())

    result = consumer.ok()
    assert result is not None

    expected = {'consumer': {'name': 'order-split-service'},
                'interactions': [{'description': 'get one seller order',
                                  'provider_state': 'seller order exists',
                                  'request': {'headers': {'Authorization': 'Token xpto'},
                                                    'method': 'get',
                                                    'path': '/v1/seller-orders/WMT9CE111CDAED0/'},
                                  'response': {'body': {'foo': 'bar'}, 'status': 200, 'headers': {}}},

                                 {'description': 'get all seller order',
                                  'provider_state': 'a list of seller order exists',
                                  'request': {'headers': {'Authorization': 'Token xpto'},
                                              'method': 'get',
                                                    'path': '/v1/seller-orders/'},
                                  'response': {'body': {'bar': 'foo'}, 'status': 200, 'headers': {}}},
                                 ],
                'provider': {'name': 'orders-api'}}

    assert result == expected
    consumer.write()