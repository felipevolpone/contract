from contract.provider import ConsumerRepresentation


def test_consumer_parse_contract():
    consumer = ConsumerRepresentation('tests/contracts/pact1.json')
    assert consumer.pact is not None
    assert consumer.provider_name == "users-api"
    assert consumer.consumer_name == "billing-api"

    assert len(consumer.interactions) == 1
    first_interaction = consumer.interactions[0]

    assert first_interaction.description == "get one user"
    assert first_interaction.provider_state == "user exists"

    assert first_interaction.request.method == "get"
    assert first_interaction.request.path == "/v1/users/USR9CE111CDAED0/"
    assert first_interaction.request.headers == {
        "Authorization": "Token xpto"
    }

    assert first_interaction.response.status == 200
    assert first_interaction.response.headers == {}
    assert 'user' in first_interaction.response.body
    assert 'repo' in first_interaction.response.body
