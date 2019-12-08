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


def test_total_docs_update(client):
    json_file1 = open('../test/test_docs/doc1.json')
    json_file2 = open('../test/test_docs/doc2.json')
    json_file3 = open('../test/test_docs/doc3.json')

    json_data1 = json.load(json_file1)
    json_data2 = json.load(json_file2)
    json_data3 = json.load(json_file3)

    client.post('/update?docID=1', json=json_data1)
    client.post('/update?docID=2', json=json_data2)
    client.post('/update?docID=3', json=json_data3)

    assert int(client.application.index.get('total_docs')) == 3
