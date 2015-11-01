from config import USING_IB
from data_trigram.words import wordDict as words
from data_trigram.entsums import entSums as entsums
from data_trigram.tagged import tagDict as tagged
from data_trigram.start_entity import startEnt
from data_trigram.end_entity import endEnt
from data_trigram.entity import entityDict as entities
import operator
import itertools
import string
import nltk
from nltk.stem.snowball import SnowballStemmer
s = SnowballStemmer("english")

if USING_IB: STATES = ["I-PER", "I-LOC", "I-ORG", "I-MISC", "B-PER", "B-LOC", "B-ORG", "B-MISC", "O"]
else: STATES = ["PER", "LOC", "ORG", "MISC", "O"]

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

		tokens = [s.stem(word.lower()) for word in tokens]
		filteredtags = []
		for tag in tags:
			if tag in string.punctuation: tag = "."
			filteredtags.append(tag)
		tags = filteredtags

		positions = test[2]
		viterbi = {}
		backpointer = {}
		if len(tokens) == 1: continue
		viterbi["START"] = {}
		backpointer["START"] = {}
		#backpointer[two][three][i] = one means that for i, with state three, and previous state two, that 'one' is the best state to be at i - 2
		#initialization step
		for state in STATES:
			viterbi["START"][state] = {}
			viterbi["START"][state][0] = conditional_entity_probability(None, None, state) * conditional_probability(state, tokens[0], tags[0])
			backpointer["START"][state] = {}
			backpointer["START"][state][0] = "START"

		#initialization step two
		for state_one in STATES:
			viterbi[state_one] = {}
			backpointer[state_one] = {}
			for state_two in STATES:
				viterbi[state_one][state_two] = {}
				backpointer[state_one][state_two] = {}
				viterbi[state_one][state_two][1] = viterbi["START"][state_one].get(0, 0) * conditional_entity_probability(None, state_one, state_two) * conditional_probability(state_two, tokens[1], tags[1])
				backpointer[state_one][state_two][1] = "START"

		#recursion steps
		for i in range(2, len(tokens)):
			word = tokens[i]
			tag = tags[i]
			for state in STATES:
				for state_two in STATES:
					highest = 0
					best_state = "O"
					for state_one in STATES:
						score = viterbi[state_one][state_two].get(i-1, 0) * conditional_entity_probability(state_one, state_two, state) * conditional_probability(state, word, tag)
						if score >= highest:
							highest = score
							best_state = state_one
					viterbi[state_two][state][i] = highest
					backpointer[state_two][state][i] = best_state

		#termination steps
		last = len(tokens) - 1
		highest_score = 0
		best_state_last = "O"
		best_state_second_last = "O"
		for state_second_last in STATES:
			for state_last in STATES:
				score = viterbi[state_second_last][state_last].get(last, 0)# * conditional_entity_probability(None, state_last, None)
				if score >= highest:
					highest = score
					best_state = state_last
					best_state_second_last = state_second_last


		#follow backtrace
		predictions = []
		predictions.append((best_state, positions[last]))
		predictions.insert(0, (best_state_second_last, positions[last-1]))
		one = best_state_second_last
		two = best_state
		i = last - 2
		while i >= 0:
			predicted_state = backpointer[one][two][i + 2]
			position = positions[i]
			predictions.insert(0,(predicted_state, position))
			two = one
			one = predicted_state
			i -= 1

		for pair in predictions:
			res = pair[0]
			pos = pair[1]
			res = res.replace("I-", "").replace("B-", "")
			if res != "O": results[res].append(pos)
		
	return results

def conditional_probability(entity, word, tag):
	one = (float(words[entity].get(word, 0)) + 1) / (entsums[entity])
	two = float(tagged[entity].get(tag, 0)) / (entsums[entity])
	return float(one) * float(two)



def conditional_entity_probability(entity_one, entity_two, entity):
	try:
		if not entity_one and not entity_two: # START START ENT
			total = 0
			count = sum(startEnt[entity].itervalues())
			for ent_one in startEnt.keys():
				total += sum(startEnt[ent_one].itervalues())
		elif not entity_one and entity_two: #START ENT ENT			
			count = startEnt[entity_two].get(entity, 0)
			total = sum(startEnt[entity_two].itervalues())
		else: # ENT ENT ENT
			count = entities[entity_one].get(entity_two, {}).get(entity, 0)
			if not count: return 0
			total = sum(entities[entity_one][entity_two].itervalues())
		return float(count) / float(total)
	except:
		return 0

