import pytest
from indexapp import create_app
import json


@pytest.fixture
def client():
    """
    This creates a client specifically for testing purposes. This client is
    initialized with a mock version of redis, so that code using redis is not
    affected by unit tests.
    """
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_basic_retrieve_correctness(client):
    json_file = open('../test/test_docs/doc1.json')
    json_data = json.load(json_file)

    client.post('/update?docID=3', json=json_data)

    json_file = open('../test/test_files/doc1_retrieve_test.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert retrieve.json['fish sand'][0][0] == 3
