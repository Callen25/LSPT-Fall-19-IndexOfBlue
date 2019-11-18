from flask import Flask, request
from getRequests import exact, union, intersection
from postRequests import add, delete

@app.route('/exact')
def exact_match():
    exact()
    return 'Todo...'

@app.route('/union')
def union_match():
    union()
    return 'Todo...'

@app.route('/intersection')
def intersect_match():
    intersection()
    return 'Todo...'

@app.route('/add')
def add_document():
    add(docID)
    return 'Todo...'

@app.route('/remove')
def remove_document():
    remove(docID)
    return 'Todo...'
