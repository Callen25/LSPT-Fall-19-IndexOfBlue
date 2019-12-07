import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import json

if __name__ == '__main__':

	nltk.download('stopwords')
	nltk.download('punkt')

	filename = input('filename: ')

	with open(filename, 'r') as content_file:
		content = content_file.read()

	stop_words = set(stopwords.words('english'))

	word_tokens = word_tokenize(content) 
  
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
	filtered_sentence = []

	for w in word_tokens: 
		if w not in stop_words: 
			w = w.lower()
			filtered_sentence.append(w) 


	data = {}
	data['old'] = {}

	data['new'] = {}
	data['new']['total'] = len(filtered_sentence)
	data['new']['grams'] = {}
	data['new']['grams']['1'] = {}


	for i in range(len(filtered_sentence)):
		if filtered_sentence[i] in data['new']['grams']['1']:
			data['new']['grams']['1'][filtered_sentence[i]].append(i)
		else:
			data['new']['grams']['1'][filtered_sentence[i]] = [i]


	json_data = json.dumps(data)

	print(json_data)
  
	#print(word_tokens) 
	#print(filtered_sentence)