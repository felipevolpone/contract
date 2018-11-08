import pytest
from contract.pact import Contract
from .conftest import client_http


def test_pact_green_path():
    contract = Contract('tests/contracts/pact1.json')

    expected = {
        "user": {"name": "felipe", "lastname": "volpone"},
        "repo": {"host": "github", "name": "py-contract"}
    }

    # fake client. it will fake a http call
    client_api = client_http(200, expected)

    contract.select('get one user').call(client_api).assert_it()


def test_pact_select_interaction_doesnot_exists():
    # fake client. it will fake a http call
    client_api = client_http(200, {})

    contract = Contract('tests/contracts/pact1.json')
    with pytest.raises(Exception):
        contract.select('i dont exist').call(client_api).assert_it()
