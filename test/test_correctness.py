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
        post = client.post(f"/update?docID={i + 1}", json=json_data)
        print(post.status_code)


def test_single_doc(client):
    """
    This test checks to confirm that the retrieval returns correct data
    when there is a single match.
    """
    json_file = open('../test/test_docs/doc1.json')
    json_data = json.load(json_file)

    client.post('/update?docID=3', json=json_data)

    json_file = open('../test/test_files/single_match.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert '3' in retrieve.json['fish sand']


def test_multi_some(client):
    """
    Tests that multiple docs with the query get returned
    """
    make_mock(client)

    json_file = open('../test/test_files/multiple_match.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['dolphin ocean']) == 2


def test_multi_none(client):
    """
    Tests that no docs return query since it doesn't appear
    in any.
    """
    make_mock(client)

    json_file = open('../test/test_files/multi_none.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['abc def']) == 0


def test_ngram_single_word_all(client):
    """
    Tests for single word appearing in all docs
    """
    make_mock(client)

    json_file = open('../test/test_files/1gram_all.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['ocean']) == 5


def test_ngram_single_some(client):
    """
    Tests for single word appearing in some docs
    """
    make_mock(client)

    json_file = open('../test/test_files/1gram_some.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['block']) == 2


def test_ngram_none(client):
    """
    Tests for single word appearing in no docs.
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
    """
    make_mock(client)

    json_file = open('../test/test_files/ngram_multi_word.json')
    json_data = json.load(json_file)

    retrieve = client.post('/relevantDocs', json=json_data)
    assert len(retrieve.json['block']) == 2


def test_ngram_multi_word_none(client):
    """
    Tests query with multiple ngrams with none
    appearing in any docs
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
    """
    make_mock(client)
    assert int(client.application.index.get('total_docs')) == 6
