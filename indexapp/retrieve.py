from flask import jsonify


def retrieve_docs(app, queries):
    """
    This function takes in a list of queries and returns the resulting matches
    on a per-query basis.
    @param app: The flask app that is calling this
    @param queries: List of queries to find exact matches for
    @return: json version of results per query
    """
    results = {}
    for query in queries:
        doc_positions = retrieve_for_query(app, query)
        query_results = clean_positions(doc_positions)
        results[query] = query_results

    return jsonify(results)


def retrieve_for_query(app, query):
    """
    This takes in a specific query and finds all of the exact matches for it.
    @param app: Flask app that is being called
    @param query: Words we are trying to match
    @return: A dictionary of doc_id -> (tf-idf, list of positions)
    """
    words = query.split()  # Terms that we are checking the index for
    total_docs = int(app.index.get('total_docs'))  # This is used in idf calc
    doc_to_pos = {}  # HashTable that holds doc_id -> (tf-idf, list of positions)

    # Initialize HashTable with all documents from the first word
    starting_docs = app.index.zrevrangebyscore(words[0], 1, 0, withscores=True)
    for doc in starting_docs:
        doc_id = int(doc[0])
        tf = doc[1]
        idf = total_docs / len(starting_docs)
        tf_idf = tf * idf
        term_positions = to_int_list(app.term_positions.lrange(f"{doc_id}:{words[0]}", 0, 1000))
        doc_to_pos[doc_id] = (tf_idf, tf, idf, term_positions)

    # For each of the following words in the query, check if the word comes next
    for word in words[1:]:
        docs = app.index.zrevrangebyscore(word, 1, 0, withscores=True)
        # Check each document to see if it contains a valid next word
        for doc in docs:
            doc_id = int(doc[0])
            # If this doc_id could be a match, try to find all potential matches
            if doc_id in doc_to_pos:
                # Check all values in the lists to find elements in order
                doc_tuple = doc_to_pos[doc_id]
                new_list = to_int_list(app.term_positions.lrange(f"{doc_id}:{word}", 0, 1000))
                new_list = intersect_list(doc_tuple[3], new_list)
                # If this is still a match add tf-idf and positions for this doc
                if new_list:
                    new_tf = doc[1]
                    new_idf = total_docs / len(docs)
                    new_tf_idf = new_tf * new_idf
                    new_tuple = (new_tf_idf * doc_tuple[0], new_tf * doc_tuple[1], new_idf * doc_tuple[2],
                                 new_list)
                    doc_to_pos[doc_id] = new_tuple
                # If this is not a match, remove it from the dictionary
                else:
                    del doc_to_pos[doc_id]

    return doc_to_pos


def intersect_list(old_list, new_list):
    """
    This takes two lists, and intersects them where a position in the previous
    list is 1 less than that in this list. This is how we determine what is an
    exact match.
    @param old_list: Old list of positions that we are trying to add to
    @param new_list: List of positions for current term in query
    @return: An intersected list where this word is a continuation of the exact
    match
    """
    # Add element + 1 to intersected list if element + 1 is in new list
    intersected_list = [value + 1 for value in old_list if value + 1 in new_list]
    return intersected_list


def to_int_list(byte_list):
    """
    Converts a list of bytes to a list of ints. This is needed because redis
    stores our term_positions as bytes.
    @param byte_list: list of term positions as bytes
    @return: list of term positions as ints
    """
    # For each element in list of bytes, turn it into an int
    for i in range(len(byte_list)):
        byte_list[i] = int(byte_list[i])
    return byte_list


def clean_positions(doc_positions):
    """
    This takes the dictionary of results found in retrieve_for_query, and
    converts them to an ordered list of tuples in the form (doc_id, tf-idf)
    where higher tf-idf's come before lower ones.
    @param doc_positions: Old dictionary representation of results
    @return: Ordered List of (doc_id, tf-idf) tuples
    """
    results = []
    # Turn doc_id:(tf-idf, tf, idf, positions[]) into List of (doc_id:{tf-idf, tf, idf})
    for k, v in doc_positions.items():
        results.append((k, {
            "tf-idf": v[0],
            "tf": v[1],
            "idf": v[2]
        }))
    # Sort list of tuples based on tf-idf score from high to low
    results.sort(key=lambda tup: tup[1]['tf-idf'], reverse=True)
    return results
