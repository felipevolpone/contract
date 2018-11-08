# py-contract

(For the lack of a better name), py-contract is a tool that helps you to keep
two the communication between two (or more) parts of your microservice
architecture "on the same page". e.g.: Making sure that if you change the API
the API consumer will break; or if it breaks, you will know that while running
the contract test not in production.

With py-contract you're able to generate a contract (a .json file) that you can
share with the team that develops the service that we will integrate with or
provide data to. With this contract, you can write e2e tests that can tell you
if a change will break someone that integrates with you.
Take a look into the example to understand how it works.

## Install

```
pip install py-contract
```

## Getting start

To show how py-contract works, we will create a scenario where we have two
microservices: the billing-api and the users-api. In this case, the billing-api
calls the users-api to get, as an example, the name of the user.

First of all, we have to describe this scenario. So, we create a `demo.py` file
in the billing-api project and copy the example bellow.

```python
# demo.py file
from contract.consumer import I

def create_billing_api__users_api_contract():
    (I("billing-api").interacts_with("users-api").
        to("get one user").
        when("user exists").
        with_request('get', '/v1/users/USR9CE111CDAED0/',
                        headers={"Authorization": "Token xpto"}).
        expecting_response(200, body={"results": {"user": {"name": "felipe"}}}).
        done().
     write())


if __name__ == '__main__':
    create_billing_api__users_api_contract()
```

Once you run this script, it will create a `billing_api__users_api.json` file.
In this file you have the contract defined. With that information, the users-api
will be able to write tests and make sure that a change in their API, will not
break the billing-api integration.

Now, you copy the contract file to the users-api codebase. There you can create
a `test_contract_billing_api.py` file and copy the content bellow.

```python
import pytest
from contract.provider import Pact

pact = Pact('pacts/billing_api__users_api.json')

expected = {
    "user": {"name": "felipe", "lastname": "volpone"},
}

client_api = client_http(200, expected)
pact.select('get one user').mount_request().call(client_api).assert_it()
```

Let's explain it by parts.

`pact = Pact('pacts/billing_api__users_api.json')` creates a pact based on a
contract file, that is specified by parameter. In `pact.select('get one user')`,
we are selecting which interaction of the contract we wan't to get to run the
contract test. `mount_request` does the setup of the request. `call(client_api)`
will use the data you specified here
`with_request('get', '/v1/users/USR9CE111CDAED0/', headers={"Authorization": "Token xpto"}).`
to call the API with the info provided. Then, `assert_it` will check if the data
you specified in the contract is the same that the API call returned.