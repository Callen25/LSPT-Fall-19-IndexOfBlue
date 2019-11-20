import os
import tempfile

import pytest

from flaskr import flaskr


@pytest.fixture
def client():
    # make mock index
    

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