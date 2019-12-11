"""
Overview
This file is responsible for making sure the actual values
retrieved effect the index in the correct manner

Setup for all tests: make_mock from test_docs
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


def make_mock(client):
    """
    function that gets called before each test to create the mock redis
    using the json files in test_docs folder.
    """
    for i in range(6):
        json_file = open(f"../test/test_docs/doc{i + 1}.json")
        json_data = json.load(json_file)
        client.post(f"/update?docID={i + 1}", json=json_data)


def test_single_doc(client):
    """
    This test checks to confirm that the retrieval returns correct data
    when there is a single match from single query.
    Setup: make_mock
    Modify: test_doc1 on update
    Assert: 3 in fish sand
    """
    json_file = open('../test/test_docs/doc1.json')
    json_data = json.load(json_file)

    client.post('/update?docID=3', json=json_data)

    json_file = open('../test/test_files/single_match.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    result = retrieve.json

    # Document 3
    assert result["fish sand"]['3']['tf'] == 0.04000000000000001
    assert result["fish sand"]['3']['tf-idf'] == 0.04000000000000001
    assert result["fish sand"]['3']['idf'] == 1.0


def test_multi_some(client):
    """
    Tests that multiple docs with the query get returned on single query
    Setup: make_mock
    Modify: multiple_match on releventDocs
    Assert: 2 docs returned for dolphin ocean
    """
    make_mock(client)

    json_file = open('../test/test_files/multiple_match.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    result = retrieve.json

    # Document 2
    assert result['dolphin ocean']['2']['tf'] == 0.0625
    assert result['dolphin ocean']['2']['tf-idf'] == 0.22499999999999998
    assert result['dolphin ocean']['2']['idf'] == 3.5999999999999996

    # Document 5
    assert result['dolphin ocean']['5']['tf'] == 0.04000000000000001
    assert result['dolphin ocean']['5']['tf-idf'] == 0.14400000000000002
    assert result['dolphin ocean']['5']['idf'] == 3.5999999999999996


def test_multi_none(client):
    """
    Tests that no docs return query since it doesn't appear
    in any.
    Setup: make_mock
    Modify: multi_none on releventDocs
    Assert: 0 docs returned for abc def
    """
    make_mock(client)

    json_file = open('../test/test_files/multi_none.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)

    assert len(retrieve.json['abc def']) == 0


def test_ngram_single_word_all(client):
    """
    Tests for single word appearing in all docs
    Setup: make_mock
    Modify: 1gram_all on releventDocs
    Assert: 5 docs returned for ocean
    """
    make_mock(client)

    json_file = open('../test/test_files/1gram_all.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    result = retrieve.json

    # Document 1
    assert result['ocean']['1']['tf'] == 0.2
    assert result['ocean']['1']['tf-idf'] == 0.24
    assert result['ocean']['1']['idf'] == 1.2

    # Document 2
    assert result['ocean']['2']['tf'] == 0.25
    assert result['ocean']['2']['tf-idf'] == 0.3
    assert result['ocean']['2']['idf'] == 1.2

    # Document 3
    assert result['ocean']['3']['tf'] == 0.2
    assert result['ocean']['3']['tf-idf'] == 0.24
    assert result['ocean']['3']['idf'] == 1.2

    # Document 4
    assert result['ocean']['4']['tf'] == 0.2
    assert result['ocean']['4']['tf-idf'] == 0.24
    assert result['ocean']['4']['idf'] == 1.2

    # Document 5
    assert result['ocean']['5']['tf'] == 0.2
    assert result['ocean']['5']['tf-idf'] == 0.24
    assert result['ocean']['5']['idf'] == 1.2


def test_ngram_single_some(client):
    """
    Tests for single word appearing in some docs
    Setup: make_mock
    Modify: 1gram_some on releventDocs
    Assert: 2 docs returned for block
    """
    make_mock(client)

    json_file = open('../test/test_files/1gram_some.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    result = retrieve.json

    # Document 2
    assert result['block']['2']['tf'] == 0.25
    assert result['block']['2']['tf-idf'] == 0.75
    assert result['block']['2']['idf'] == 3.0

    # Document 3
    assert result['block']['3']['tf'] == 0.2
    assert result['block']['3']['tf-idf'] == 0.6000000000000001
    assert result['block']['3']['idf'] == 3.0


def test_ngram_none(client):
    """
    Tests for single word appearing in no docs.
    Setup: make_mock
    Modify: 1gram_none on releventDocs
    Assert: 0 docs returned for abcd
    """
    make_mock(client)

    json_file = open('../test/test_files/1gram_none.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['abcd']) == 0


def test_ngram_multi_word(client):
    """
    Tests query with multiple ngrams appearing in
    some docs
    Setup: make_mock
    Modify: ngram_multi_word on releventDocs
    Assert: 2 docs returned for block
    """
    make_mock(client)

    json_file = open('../test/test_files/ngram_multi_word.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    result = retrieve.json

    # Document 2
    assert result['block']['2']['tf'] == 0.25
    assert result['block']['2']['tf-idf'] == 0.75
    assert result['block']['2']['idf'] == 3.0

    # Document 3
    assert result['block']['3']['tf'] == 0.2
    assert result['block']['3']['tf-idf'] == 0.6000000000000001
    assert result['block']['3']['idf'] == 3.0


def test_ngram_multi_word_none(client):
    """
    Tests query with multiple ngrams with none
    appearing in any docs
    Setup: make_mock
    Modify: ngram_multi_word_none on releventDocs
    Assert: 0 docs returned for Abc def
    """
    make_mock(client)

    json_file = open('../test/test_files/ngram_multi_word_none.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['Abc def']) == 0


def test_total_docs_update(client):
    """
    This test ensures that when new documents are added, the total_docs count
    is incremented
    Setup: make_mock
    Modify: None
    Assert: total_docs = 6
    """
    make_mock(client)
    assert int(client.application.index.get('total_docs')) == 6
