import json
from pprint import pprint
from contract.consumer import I


def test_consumer_json_generation():
    consumer = (I("order-split-service").
              depends_on("orders-api").
              to("get a seller order").
              when("seller order exists").
              with_request('get', '/v1/seller-orders/WMT9CE111CDAED0/',
                           headers={"Authorization": "Token xpto"}).
              expecting_response(200, body={}))

    result = consumer.done()

    assert result is not None
    expected = {'consumer': {'name': 'order-split-service'},
                'interactions': [{'description': 'get a seller order',
                                  'provider_state': 'seller order exists',
                                  'request': {'headers': {'Authorization': 'Token xpto'},
                                                    'method': 'get',
                                                    'path': '/v1/seller-orders/WMT9CE111CDAED0/'},
                                  'response': {'body': {}, 'status': 200}}],
                'provider': {'name': 'orders-api'}}
    assert result == expected