from flask import Flask, request
# from getRequests import exact, union, intersection
from src.postRequests import update_doc


app = Flask(__name__)

'''
@params: http header
@returns: Json response with list of doc-ids, tf-idf score
@description: returns data from index that has and exact
              match with the query
@throws: returns with response 400 if any error occurs
'''
@app.route('/relevantDocs', methods=['POST'])
def get_docs():
    return 'Todo..'

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
@app.route('/update', methods=['POST'])
def update():
    params = request.args
    json = request.json
    return update_doc(params['docID'], json)


if __name__ == '__main__':
    app.run(debug=True)
