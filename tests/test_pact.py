import pytest
from contract.provider import Pact
from .conftest import client_http


def test_pact_green_path():
    pact = Pact('tests/pacts/pact1.json')

    expected = {
        "user": {"name": "felipe", "lastname": "volpone"},
        "repo": {"host": "github", "name": "py-contract"}
    }

    # fake client. it will fake a http call
    client_api = client_http(200, expected)

    pact.select('get one user').mount_request().call(client_api).assert_it()


def test_pact_select_interaction_doesnot_exists():
    # fake client. it will fake a http call
    client_api = client_http(200, {})

    pact = Pact('tests/pacts/pact1.json')
    with pytest.raises(Exception):
        pact.select('i dont exist').mount_request().call(client_api).assert_it()
