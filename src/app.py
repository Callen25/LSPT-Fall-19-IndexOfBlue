from flask import Flask, request
# from getRequests import exact, union, intersection
# from postRequests import add, delete

'''
@params: http header
@returns: Json response with list of doc-ids, tf-idf score
@description: returns data from index that has and exact
              match with the query
@throws: returns with response 400 if any error occurs
'''
@app.route('/releventDocs')
def exact_match():
    exact()
    return 'Todo...'

# '''
# @params: None
# @returns: Json response with list of doc-ids, tf-idf score
# @description: returns data from index that has and exact
#               match with the query
# @throws: returns with response 400 if any error occurs
# '''
# @app.route('/exact')
# def exact_match():
#     exact()
#     return 'Todo...'


# '''
# @params: None
# @returns: Json response with list of doc-ids, tf-idf score
# @description: returns data from index that has any matching
#               data from a union operation
# @throws: returns with response 400 if any error occurs
# '''
# @app.route('/union')
# def union_match():
#     union()
#     return 'Todo...'

# '''
# @params: None
# @returns: Json response with list of doc-ids, tf-idf score
# @description: returns data from index that has any matching
#               data from an intersection operation
# @throws: returns with response 400 if any error occurs
# '''
# @app.route('/intersection')
# def intersect_match():
#     intersection()
#     return 'Todo...'

'''
@params: None
@returns: 200 ok if the document was added to the index
@description: adds the new doc-id with transformed text
@throws: returns with response 400 if any error occurs
'''
@app.route('/update')
def add_document():
    #add(docID)
    return 'Todo...'

# '''
# @params: None
# @returns: Json response with list of doc-ids, tf-idf score
# @description: removes the doc-id and associated transformed text
# @throws: returns with response 400 if any error occurs
# '''
# @app.route('/remove')
# def remove_document():
#     remove(docID)
#     return 'Todo...'
