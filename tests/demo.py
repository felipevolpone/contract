
from contract.consumer import I


def order_split_service__orders_api_contract():
    expectation = {"channel_slug": "b2w",
                   "channel_store": "walmart",
                   "code": "PRDOBGHRFBKSMEGF",
                   "seller_id": "dee709dc-41ec-45ef-afb7-544eec627b40"}

    (I("order-split-service").interacts_with("orders-api").
        to("get one seller order").
        when("seller order exists").
        with_request('get', '/v1/seller-orders/PRDOBGHRFBKSMEGF/',
                    headers={"Authorization": "Token xpto"}).
        expecting_response(200, body=expectation).done().
     write()
    )


if __name__ == '__main__':
    order_split_service__orders_api_contract()
