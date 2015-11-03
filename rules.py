import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words("english")

def adjust_conditional_probability(entity, word, tag, score):
	#if word in stopwords and entity != "O":
	#	score = float(0)
	return score

def adjust_conditional_entity_probability(entity_one, entity_two, entity, score):
	# two non-O entities that are distinct are almost always seperated by an O
	#if entity_one and entity_two and entity:
	#	if entity_one != "O" and entity_two != "O" and entity_one != entity_two: return float(0)
	#	if entity_two != "O" and entity != "O" and entity_two != entity: return float(0)
	return score