from config import USING_IB
from data.base_combined import combinedDict as base_combined
from data.base_tagged import tagDict as base_tagged
from data.base_words import wordDict as base_words
from data.entsums import entSums as entsums
from data.words import wordDict as words
from data.tagged import tagDict as tagged
from data.start_entity import startEnt
from data.end_entity import endEnt
from data.entity import entityDict as entities
import operator
import itertools
import string

if USING_IB: STATES = ["I-PER", "I-LOC", "I-ORG", "I-MISC", "B-PER", "B-LOC", "B-ORG", "B-MISC", "O"]
else: STATES = ["PER", "LOC", "ORG", "MISC", "O"]


def get_baseline_predictions(tests):
	results = {
		"PER": [],
		"LOC": [],
		"ORG": [],
		"MISC": []
	}
	for test in tests:
		word = test[0].lower()
		tag = test[1]
		position = test[2]
		res = predict_baseline_fallback(word, tag)
		res = res.replace("I-", "").replace("B-", "")
		if res != "O": results[res].append(position)
	return results

def predict_baseline_fallback(word, tag):
	try:
		res = max(base_combined[word + "|" + tag].iteritems(), key=operator.itemgetter(1))[0]
	except: #key error
		try: 
			res = max(base_words[word].iteritems(), key=operator.itemgetter(1))[0]
		except:
			res = max(base_tagged[tag].iteritems(), key=operator.itemgetter(1))[0]
	return res

def predict_baseline_naive(word):
	try: 
		res = max(base_words[word].iteritems(), key=operator.itemgetter(1))[0]
	except:
		res = "O"
	return res 


def get_hmm_predictions(tests):
	results = {
		"PER": [],
		"LOC": [],
		"ORG": [],
		"MISC": []
	}
	counter = 0
	for test in tests:
		counter += 1
		if counter % 100 == 0: print "On test %d" % counter
		tokens = test[0]
		tags = test[1]
		positions = test[2]
		viterbi = {}
		backpointer = {}

		tokens = [word.lower() for word in tokens]
		filteredtags = []
		for tag in tags:
			if tag in string.punctuation: tag = "."
			filteredtags.append(tag)
		tags = filteredtags

		#initialization step
		for state in STATES:
			viterbi[state] = {}
			viterbi[state][0] = conditional_entity_probability(None, state) * conditional_probability(state, tokens[0], tags[0])
			backpointer[state] = {}
			backpointer[state][0] = "START"

		#recursion steps
		for i in range(1, len(tokens)):
			word = tokens[i]
			tag = tags[i]
			for state in STATES:
				highest = 0
				best_state = "O"
				for sprime in STATES:
					score = viterbi[sprime].get(i-1, 0) * conditional_entity_probability(sprime, state) * conditional_probability(state, word, tag)
					if score >= highest:
						highest = score
						best_state = sprime
				viterbi[state][i] = highest
				backpointer[state][i] = best_state

		#termination steps
		last = len(tokens) - 1
		highest = 0
		best_state = "O"
		for state in STATES:
			score = viterbi[state].get(last, 0)# * conditional_entity_probability(state, None) #- tended to make final state O too often
			if score >= highest:
				highest = score
				best_state = state
		viterbi["END"] = {}
		viterbi["END"][last] = highest
		backpointer["END"] = {}
		backpointer["END"][last] = best_state

		#follow backtrace
		predictions = []
		predictions.append((best_state, positions[last]))
		back_state = best_state
		i = last - 1
		while i >= 0:
			predicted_state = backpointer[back_state][i + 1]
			position = positions[i]
			predictions.insert(0,(predicted_state, position))
			back_state = predicted_state
			i -= 1

		for pair in predictions:
			res = pair[0]
			pos = pair[1]
			res = res.replace("I-", "").replace("B-", "")
			if res != "O": results[res].append(pos)
		
	return results

def conditional_probability(entity, word, tag):
	one = (float(words[entity].get(word, 0)) + 1) / (entsums[entity] + 1)
	two = float(tagged[entity].get(tag, 0)) / entsums[entity]
	return float(one) * float(two)

def conditional_entity_probability(entity_prev, entity):
	#try:
	if not entity_prev and entity:
		count = startEnt.get(entity, 0)
		total = sum(startEnt.itervalues())
	elif not entity and entity_prev:			
		count = endEnt.get(entity_prev, 0)
		total = sum(endEnt.itervalues())
	else:
		count = entities[entity_prev].get(entity, 0)
		total = sum(entities[entity_prev].itervalues())
	#except:
	#	return float(0)
	return float(count) / float(total)

