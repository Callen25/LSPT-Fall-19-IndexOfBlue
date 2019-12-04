'''
@params: parsable json object
@returns: dictionary with data from json
@description: creates a object from json which can be used
              easily in python
@throws: JsonifyError if any error occurs
'''
def parseJSON():
    pass

'''
@params: args from http
@returns: set of doc ids
@description: gets all of the exact matches from index
@throws: MatchError if any error occurs
'''
def exact():
    # results
    # for doc in documents:
    #     if(is_exact(doc)) results.add(doc)
    pass

'''
@params: docid, string to match
@returns: boolean
@description: returns if there is an exact match
@throws: MatchError if any error occurs
'''
def is_exact(doc):
    pass

# '''
# @params: args from http
# @returns: set of doc ids
# @description: gets all of the union matches from index
# @throws: MatchError if any error occurs
# '''
# def union():
#     pass

# '''
# @params: args from http
# @returns: set of doc ids
# @description: gets all of the intersection matches from index
# @throws: MatchError if any error occurs
# '''
# def intersection():
#     pass


'''
@params: dictionary
@returns: json object
@description: creates a jsonobject from the dict which 
              can be used as the response in http
              
@throws: JsonifyError if any error occurs
'''
def serializeJSON():
    pass
