from flask import Blueprint, current_app, request
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
    return retrieve_docs(app, request.json['queries'])


@bp.route('/update', methods=['POST'])
def update():
    """
    @params: None, takes in body of POST
    @returns: 201 created if the document was updated successfully
    @description: adds the new doc-id with transformed text
    @throws: returns with response 400 if any error occurs
    """
    return update_doc(app, request.args['docID'], request.json['old'], request.json['new'])
