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
    This test ensures that the correct http satus code is returned for a basic
    index update.
    """
    json_file = open('../test/test_files/update_sample1.json')
    json_data = json.load(json_file)

    update = client.post('/update?docID=3', json=json_data)

    assert update.status_code == 201



# def test_add_success(client):
#     doc1 = "./test_docs/doc1.txt"
#     add1 = client.add(doc1)
#     assert add1 == 'Todo...'
#     remove1 = client.remove(doc1)
#     assert remove1 == 'Todo...'
#
#
# def test_add_fail(client):
#     pass
#
# def update_add_success(client):
#     pass
#
# def update_add_fail(client):
#     pass
#
# def test_remove_success(client):
#     pass
#
# def test_remove_fail(client):
#     pass
#
# def test_exact_match(client):
#     docs = client.get('/exact?query=ocean_block')
#     assert docs == [doc2]
#
# def test_multi_exact_match(client):
#     pass
#
# def test_no_exact_match(client):
#     pass
#
# # def test_union(client):
# #     docs = client.get('/union?query=chore_dolphin')
# #     assert docs == [doc1,doc2]
#
# #     docs = client.get('/union?query=sky')
# #     assert docs is None
#
#
# # def test_intersect(client):
# #     docs = client.get('/intersect?query=fish')
# #     assert docs == [doc1,doc2]
