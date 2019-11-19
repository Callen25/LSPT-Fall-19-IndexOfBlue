from redis import Redis
from flask import Response

# Todo: come up with a way to save redis configuration (password) securely
index = Redis(host='localhost', port=6379, db=0)  # k, v store for term -> doc_id
term_positions = Redis(host='localhost', port=6379, db=1)  # k, v store for doc:term -> list of positions


# Todo: probably remove this, Flask automatically converts json to dictionary
def parse_json():
    """
    @params: parsable json object
    @returns: dictionary with data from json
    @description: creates a object from json which can be used
                  easily in python
    @throws: JsonifyError if any error occurs
    """
    pass


# Todo: implement remove_doc functionality
def update_doc(doc_id, new_doc):
    """
    @param doc_id: id of document we are updating
    @param new_doc: json of new_doc to be added to index
    @returns: 201 status code if created successfully, 422 status code otherwise
    @description: gets all of the exact matches from index
    """
    if new_doc:
        # If there is a new doc to add, add the words and their tf scores
        add_doc(doc_id, new_doc['grams']['1'], new_doc['total'])
    return Response(f"Document: {doc_id}, successfully added", status=201, mimetype='application/json')


def add_doc(doc_id, words, total):
    """
    @param doc_id: id of document we are adding
    @param words: dictionary of words and their positions in the document
    @param total: total number of words in document (used for tf calculation)
    @description: add words in this document along with their positions to index
    """
    with index.pipeline() as index_pipe, term_positions.pipeline() as term_pipe:
        for word in words:
            # Add this word to term -> doc_id mapping
            index_pipe.zadd(word, {doc_id: len(words[word]) / total})
            # Update the list of positions for this word in this document (word -> list of positions)
            term_pipe.rpush(f"{doc_id}:{word}", *words[word])
        # Add them to redis in batch
        index_pipe.execute()
        term_pipe.execute()


def remove(doc_id):
    """
    @params: args from http
    @returns: set of doc ids
    @description: gets all of the exact matches from index
    @throws: MatchError if any error occurs
    """
    pass
