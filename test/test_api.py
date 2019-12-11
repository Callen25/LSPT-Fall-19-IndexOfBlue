"""
Overview
This test file is responsible for testing the api and checking if
the flask app in able to respond in the simple cases
"""

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


def test_basic_update(client):
    """
    This test ensures that the correct http status code is returned for a basic
    index update.
    """
    json_file = open('../test/test_files/update_sample1.json')
    json_data = json.load(json_file)

    update = client.post('/update?docID=3', json=json_data)

    assert update.status_code == 201


def test_bad_update(client):
    """
    This test ensures the correct http status code is returned for a mis-formatted
    update json.
    """
    json_file = open('../test/test_files/update_bad_sample1.json')
    json_data = json.load(json_file)

    update = client.post('/update?docID=1', json=json_data)

    assert update.status_code == 400
    
def test_bad_update_no_occurrences(client):
    """
    This test ensures the correct http status code is returned for a mis-formatted
    update json.
    """
    json_file = open('../test/test_docs/bad_occurrences.json')
    json_data = json.load(json_file)

    update = client.post('/update?docID=1', json=json_data)

    assert update.status_code == 400


def test_blank_update(client):
    """
    A request that does not change the index should result in a 400 error.
    Does not contain any values that need to added or removed
    """
    json_file = open('../test/test_files/update_bad_sample2.json')
    json_data = json.load(json_file)

    update = client.post('/update?docID=1', json=json_data)

    assert update.status_code == 400

def test_invalid_remove(client):
    """
    A request that attempts to remove words that do not exist.
    Returns 201 and does not crash the index
    """
    json_file = open('../test/test_files/not_present.json')
    json_data = json.load(json_file)

    update = client.post('/update?docID=1', json=json_data)

    assert update.status_code == 201

def test_basic_retrieve(client):
    """
    This test ensures that the correct http status code is returned for a basic
    index retrieval.
    """
    json_file = open('../test/test_files/update_sample1.json')
    json_data = json.load(json_file)

    client.post('/update?docID=3', json=json_data)

    json_file = open('../test/test_files/retrieve_sample1.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)

    assert retrieve.status_code == 200
