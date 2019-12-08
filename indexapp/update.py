from flask import Response


def update_doc(app, doc_id, old_doc, new_doc):
    """
    @param app: Flask app that is calling this function
    @param doc_id: id of document we are updating
    @param old_doc: json of old_doc to be removed from index
    @param new_doc: json of new_doc to be added to index
    @returns: 201 status code if created successfully, 400 if not formatted correctly
    @description: replaces all data from old document with that from the new document
    """
    old_doc_valid = 'grams' in old_doc and '1' in old_doc['grams']
    new_doc_valid = 'grams' in new_doc and '1' in new_doc['grams'] and 'total' in new_doc

    if old_doc_valid:
        remove_doc(app, doc_id, old_doc['grams']['1'])
        if not new_doc_valid:
            app.index.decr('total_docs')

    if new_doc_valid:
        # If there is a new doc to add, add the words and their tf scores
        add_doc(app, doc_id, new_doc['grams']['1'], new_doc['total'])
        if not old_doc_valid:
            app.index.incr('total_docs')

    # If there is nothing to add or remove, return a 400 for bad format
    if not new_doc_valid and not old_doc_valid:
        return Response("Invalid Format, nothing to add or remove", status=400, mimetype='application/json')

    return Response(f"Document: {doc_id}, successfully updated", status=201, mimetype='application/json')


def remove_doc(app, doc_id, words):
    """
    @param app: Flask app that is calling this function
    @param doc_id: id of document to be removed
    @param words: words associated to this document to be removed
    @description: removes doc_id-word associations for given doc_id and words
    """
    with app.index.pipeline() as index_pipe, app.term_positions.pipeline() as term_pipe:
        for word in words:
            # Remove id for word in word -> doc_id mapping, if word only appears in this document then remove word
            if app.index.exists(word):
                if app.index.zcard(word) > 1:
                    index_pipe.zrem(word, doc_id)
                else:
                    index_pipe.delete(word)
            # Remove word and its associated positions within the document
            if app.term_positions.exists(f"{doc_id}:{word}"):
                term_pipe.delete(f"{doc_id}:{word}")

        index_pipe.execute()
        term_pipe.execute()


def add_doc(app, doc_id, words, total):
    """
    @param app: Flask app that is calling this function
    @param doc_id: id of document we are adding
    @param words: dictionary of words and their positions in the document
    @param total: total number of words in document (used for tf calculation)
    @description: add words in this document along with their positions to index
    """
    with app.index.pipeline() as index_pipe, app.term_positions.pipeline() as term_pipe:
        for word in words:
            # Add this word to term -> doc_id mapping
            index_pipe.zadd(word, {doc_id: len(words[word]) / total})
            # Update the list of positions for this word in this document (word -> list of positions)
            term_pipe.rpush(f"{doc_id}:{word}", *words[word])
        # Add them to redis in batch
        index_pipe.execute()
        term_pipe.execute()
