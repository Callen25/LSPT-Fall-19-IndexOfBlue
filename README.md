# LSPT-Fall-19-IndexOfBlue

## Getting Started

To install all the necessary packages, run **pip install -r requirements.txt**. (We recommend using a virtual environment)

To run locally, redis needs to be installed. Details about doing so can be seen [here](https://redis.io/topics/quickstart)

## API Reference

Our API is centered around REST. Our API accepts JSON encoded request bodies and returns JSON encoded responses
and uses standard http response codes and verbs

### Errors

We use conventional http response codes, in general: codes in the 2xx range indicate success, while codes in the 4xx indicate failure given the information provided. Response codes in 5xx indicate server error.

### Update

Use this endpoint to add, remove, and update an existsing document the in index

Request type | Endpoint | Arguments | body type
------------ | -------------|-------|----------
POST | /update | docID | JSON

docID is a required query parameter that specifies which docuemt will be referenced

If you want to add a document that does not exist remove should be empty<br />
If you want to remove a document that add should be empty<br />
If you want to update an existing specify what should be added and what should be removed<br />

JSON BODY EXAMPE
```
{
	"add": {
		"stripped": "old text here lets delete this",
		"total": 6,
		"grams": {
			"1": {
				"old": [0],
				"text": [1],
				"here": [2],
				"lets": [3],
				"delete": [4],
				"this": [5]
			}
		}
	},
	"remove": {
		"stripped": "ebook use anyone anywhere united States most other parts world no cost with almost no restrictions whatsoever",
		"total": 17,
		"grams": {
			"1": {
				"ebook": [0],
				"use": [1],
				"anyone": [2],
				"anywhere": [3],
				"united": [4],
				"states": [5],
				"most": [6],
				"other": [7],
				"parts": [8],
				"world": [9],
				"no": [10, 14],
				"cost": [11],
				"with": [12],
				"almost": [13],
				"restrictions": [15],
				"whatsoever": [16]
			}
		},
		"title": "Hello World"
	}
}
```

### Retrieve from index

This endpoint is used to get relevent documents based on a list of ngrams as requested by Ranking


Request type | Endpoint | body type
------------ | -------------|-----
POST | /releventDocs | JSON

POST Body:
```
{
	[
		"try this query",
		"try this",
		"also try this"
	]
}
```

Response:
```
{
   “NGRAM1”:
    [
       “Documentid1”:{documentData},
       “Documentid1”: {documentData},...
    ],
    “NGRAM2”:...
}
```
Where documentData is as follows
```
{
   "tf": INT,
   "idf" : INT,
   "tf-idf" : INT
 }

```
