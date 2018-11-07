
from contract.provider import Pact


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


def test_pact():
    pact = Pact('tests/pacts/pact1.json')

    expected = {"branded_store_slug": "olist",
                "cancelation_reason": "shipment_delayed",
                "cancelation_status": "canceled",
                "channel_slug": "walmart",
                "channel_store": "walmart",
                "code": "WMT9CE111CDAED0",
                "order_id": "893c08a1-b534-4516-ac70-53eb4abdf714",
                "seller_id": "cd0d70e0-b217-4cb9-aa4a-bddd42f39c4f",
                "seller_name": "Seller cd0d70e0b2174cb9aa4abddd42f39c4f",
                "status": "approved"}

    # fake client. that will fake a http call
    client_api = client_http(200, expected)

    pact.select('get one seller order').mount_request().call(client_api).assert_it()
