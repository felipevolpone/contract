from contract.provider import ConsumerRepresentation


def test_consumer_representation():
    consumer = ConsumerRepresentation('tests/pacts/pact1.json')
    assert consumer.pact is not None
    assert consumer.provider_name == "orders-api"
    assert consumer.consumer_name == "order-split-service"

    assert len(consumer.interactions) == 1
    first_interaction = consumer.interactions[0]

    assert first_interaction.description == "get a seller order"
    assert first_interaction.provider_state == "seller order exists"

    assert first_interaction.request.method == "get"
    assert first_interaction.request.path == "/v1/seller-orders/WMT9CE111CDAED0/"
    assert first_interaction.request.headers == {"Authorization": "Token 48d13e002cfe03b4e4392205fe5d9cef42781824"}

    assert first_interaction.response.status == 200
    assert first_interaction.response.headers == {}
    assert 'channel_store' in first_interaction.response.body
    assert 'code' in first_interaction.response.body