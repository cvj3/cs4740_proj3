from config import USING_BASELINE
if USING_BASELINE:
	from data.base_combined import combinedDict as combined
	from data.base_tagged import tagDict as tagged
	from data.base_words import wordDict as words
else:
	from data.combined import combinedDict as combined
	from data.tagged import tagDict as tagged
	from data.words import wordDict as words
	from data.entity import entityDict as entities
import operator
import itertools

ENTS = ["PER", "LOC", "ORG", "MISC", "O"]


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
		scores = {}
		bptr = {}
		for i in range(len(ENTS)):
			scores[i] = scores.get(i, {})
			scores[i][0] = conditional_entity_probability(None, ENTS[i]) * conditional_probability(ENTS[i], tokens[0], tags[0])
			bptr[i] = bptr.get(i, {})
			bptr[i][0] = bptr[i].get(0, 0)

		for t in range(1, len(tokens)):
			for i in range(len(ENTS)):
				best_score = 0
				best_index = 0
				for j in range(len(ENTS)):						
					score = scores[j][t-1] * conditional_entity_probability(ENTS[j], ENTS[i]) * conditional_probability(ENTS[i], tokens[t], tags[t])
					if j == 0:
						best_score = score
						best_index = j
					if score > best_score:
						best_score = score
						best_index = j
				scores[i][t] = best_score
				bptr[i][t] = best_index

		#T(n-1) = i that maximizes SCORE(i, n-1)
		T = {}
		n = len(tokens)
		best_i = 0
		best_score = scores[0][n-1]
		for i in scores.keys():
			score = scores[i][n-1]
			if score > best_score:
				best_score = score
				best_i = i
		T[n-1] = best_i

		#for i = n-2 to 0 do
		i = n-2
		while i >= 0:
			T[i] = bptr[T[i+1]][i+1]
			i -= 1

		for i in T.keys():
			entity = ENTS[T[i]]
			position = positions[i]
			if entity != "O": results[entity].append(position)
	return results

def conditional_probability(entity, word, tag):
	try:
		count = combined[entity][word + "|" + tag]
		total = sum(combined[entity].itervalues())
	except: #key error, fall back
		try: 
			count = words[entity][word]
			total = sum(words[entity].itervalues())
		except: # key error, fall back
			try: # if this fails, then there is no match, return a probability of 0
				count = tagged[entity][tag]
				total = sum(tagged[entity].itervalues())
			except:
				return 0
	return float(count) / float(total)

def conditional_entity_probability(entity_prev, entity):
	if not entity_prev:
		total = 0
		for e in ENTS:
			total += sum(entities[e].itervalues()) #total = total number of all seen entitites
		count = sum(entities[entity].itervalues()) #count = total occurences of given entity
	else:
		count = entities[entity_prev][entity]
		total = sum(entities[entity_prev].itervalues())
	return float(count) / float(total)


'''
# this was done with brute force, computing all permutations.
def get_hmm_predictions(tests):
	results = {
		"PER": [],
		"LOC": [],
		"ORG": [],
		"MISC": []
	}

	counter = 0
	for test in tests:
		print "On test %d" % counter
		counter += 1
		if counter == 3: break
		tokens = test[0]
		tags = test[1]
		positions = test[2]
		best_score = 0
		best_permutation = None
		permutations = itertools.product(ENTS, repeat=len(tokens)) #returns all possible permutations of ENTS for the tokens
		for permutation in permutations:
			score = score_permutation(tokens, tags, permutation, best_score)
			if score > best_score:
				best_score = score
				best_permutation = permutation
		for i in range(len(permutation)):
			res = permutation[i]
			position = positions[i]
			if res != "O": results[res].append(position)
	return results


def score_permutation(tokens, tags, permutation, best_score):
	score = 1
	for i in range(len(tokens)):
		if score < best_score: return 0
		entity = permutation[i]
		word = tokens[i]
		tag = tags[i]		
		score *= conditional_probability(entity, word, tag)
		if i == 0: continue
		entity_prev = permutation[i-1]
		score *= conditional_entity_probability(entity_prev, entity)

'''