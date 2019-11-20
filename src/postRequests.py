from redis import Redis
from flask import Response

# Todo: come up with a way to save redis configuration (password) securely
index = Redis(host='localhost', port=6379, db=0)  # k, v store for term -> doc_id
term_positions = Redis(host='localhost', port=6379, db=1)  # k, v store for doc:term -> list of positions


def update_doc(doc_id, old_doc, new_doc):
    """
    @param doc_id: id of document we are updating
    @param old_doc: json of old_doc to be removed from index
    @param new_doc: json of new_doc to be added to index
    @returns: 201 status code if created successfully, 422 status code otherwise
    @description: replaces all data from old document with that from the new document
    """
    if old_doc:
        remove_doc(doc_id, old_doc['grams']['1'])
    if new_doc:
        # If there is a new doc to add, add the words and their tf scores
        add_doc(doc_id, new_doc['grams']['1'], new_doc['total'])
    return Response(f"Document: {doc_id}, successfully updated", status=201, mimetype='application/json')


def remove_doc(doc_id, words):
    """
    @param doc_id: id of document to be removed
    @param words: words associated to this document to be removed
    @description: removes doc_id-word associations for given doc_id and words
    """
    with index.pipeline() as index_pipe, term_positions.pipeline() as term_pipe:
        for word in words:
            # Remove id for word in word -> doc_id mapping, if word only appears in this document then remove word
            if index.zcard(word) > 1:
                index_pipe.zrem(word, doc_id)
            else:
                index_pipe.delete(word)
            # Remove word and its associated positions within the document
            term_pipe.delete(f"{doc_id}:{word}")

        index_pipe.execute()
        term_pipe.execute()


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
