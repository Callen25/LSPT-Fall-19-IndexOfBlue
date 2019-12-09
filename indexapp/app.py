from flask import Blueprint, current_app, request, Response
from .update import update_doc
from .retrieve import retrieve_docs

app = current_app

bp = Blueprint("base", __name__)


@bp.route('/relevantDocs', methods=['POST'])
def get_docs():
    """
    @params: http header
    @returns: Json response with list of doc-ids, tf-idf score
    @description: returns data from index that has and exact
                  match with the query
    @throws: returns with response 400 if any error occurs
    """
    try:
        return retrieve_docs(app, request.json)
    except KeyError:
        return Response("Bad Request: Invalid Format", status=400, mimetype='application/json')


@bp.route('/update', methods=['POST'])
def update():
    """
    @params: None, takes in body of POST
    @returns: 201 created if the document was updated successfully
    @description: adds the new doc-id with transformed text
    @throws: returns with response 400 if any error occurs
    """
    try:
        if 'remove' in request.json:
            remove = request.json['remove']
        else:
            remove = {}
        if 'add' in request.json:
            add = request.json['add']
        else:
            add = {}
        return update_doc(app, request.args['docID'], remove, add)
    except KeyError:
        return Response("Bad Request: Invalid Format", status=400, mimetype='application/json')

