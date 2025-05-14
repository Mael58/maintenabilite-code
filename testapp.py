import pytest
import json

from app import app

@pytest.fixture()
def defapp():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(defapp):
    return defapp.test_client()


def test_request_example(client):
    response = client.get("/water")
    result = json.loads(response.data)
    print(result)
    assert 70 == result['water']
