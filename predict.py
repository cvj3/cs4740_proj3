from data.combined import combinedDict as combined
from data.tag import tagDict as tagged
from data.word import wordDict as words
import operator


def get_baseline_predictions(tests):
	results = {
		"PER": [],
		"LOC": [],
		"ORG": [],
		"MISC": []
	}
	for test in tests:
		word = test[0]
		tag = test[1]
		position = test[2]
		res = predict_baseline_fallback(word, tag)
		#res = predict_baseline_naive(word)
		if res != "O": results[res].append(position)
	return results

def predict_baseline_fallback(word, tag):
	try:
		res = max(combined[word + "|" + tag].iteritems(), key=operator.itemgetter(1))[0]
	except: #key error
		try: 
			res = max(words[word].iteritems(), key=operator.itemgetter(1))[0]
		except: 
			res = max(tagged[tag].iteritems(), key=operator.itemgetter(1))[0]
	return res

def predict_baseline_naive(word):
	try: 
		res = max(words[word].iteritems(), key=operator.itemgetter(1))[0]
	except:
		res = "O"
	return res 