import os
import tempfile

import pytest

from flaskr import flaskr


@pytest.fixture
def client():
    # make mock index
    client = dict();
    client["ocean"] = [(doc1, [0]), (doc2, [1]), (doc3, [1])];
    client["chore"] = [(doc1, [1])];
    client["fish"] = [(doc1, [2]), (doc2, [3])];
    client["sand"] = [(doc1, [3])];
    client["cup"] = [(doc1, [4])];
    client["dolphin"] = [(doc2, [0])];
    client["block"] = [(doc2, [2]), (doc3, [0])];
    client["star"] = [(doc3, [2])];
    client["pick"] = [(doc3, [3])];
    client["spoon"] = [(doc3, [4])];

def test_add_success(client):
    doc1 = "./test_docs/doc1.txt"
    add1 = client.add(doc1)
    assert add1 == 'Todo...'
    remove1 = client.remove(doc1)
    assert remove1 == 'Todo...'
    
    
def test_add_fail(client):
    pass

def update_add_success(client):
    pass
    
def update_add_fail(client):
    pass

def test_remove_success(client):
    pass
       
def test_remove_fail(client):
    pass

def test_exact_match(client):
    docs = client.get('/exact?query=ocean_block')
    assert docs == [doc2]

def test_multi_exact_match(client):
    pass

def test_no_exact_match(client):
    pass

# def test_union(client):
#     docs = client.get('/union?query=chore_dolphin')
#     assert docs == [doc1,doc2]

#     docs = client.get('/union?query=sky')
#     assert docs is None


# def test_intersect(client):
#     docs = client.get('/intersect?query=fish')
#     assert docs == [doc1,doc2]
