import os
import string
from common import writeData
from config import USING_IB
# import sys


__author__ = "Alin Barsan, Curtis Josey"


# param1 = path, param2 = filename
def main(param1, param2):
    # Read and Parse XML
    textArray, posArray, entityArray, startEnt, endEnt = readData(param1, param2, False)

    # build Data
    entities, word, tag, entsums = buildData(textArray, posArray, entityArray)

    # Write out to a dictionary file (lib/data.py)
    writeData('data_trigram', 'entity.py', 'entityDict', entities)
    writeData('data_trigram', 'words.py', 'wordDict', word)
    writeData('data_trigram', 'entsums.py', 'entSums', entsums)
    writeData('data_trigram', 'tagged.py', 'tagDict', tag)
    writeData('data_trigram', 'start_entity.py', 'startEnt', startEnt)
    writeData('data_trigram', 'end_entity.py', 'endEnt', endEnt)

# read training file and return parsed data
def readData(path, filename, verboseMode=False):
    textArray = []
    posArray = []
    entityArray = []
    startEnt = {}
    endEnt = {}

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path + '/' + filename)

    # loop until done
    with open(filename) as f:
        iLoop = 0
        # read / parse 3 lines at a time
        for line in f:
            iLoop += 1

            if iLoop == 1:
                line = line.lower()
            if not USING_IB and iLoop == 3: line = line.replace("I-", "").replace("B-", "")
            # split with no args accomodates 'whitespace' (tabs or spaces)
            line = line.strip().split()
            if iLoop == 1:
                # words
                textArray.append(line) # Storing each line seperately now.  before, end of one line was treated as coming right before the start of another
            elif iLoop == 2:
                # preprocess punctuation
                for i in range(len(line)):
                    if line[i] in string.punctuation:
                        line[i] = "."
                # part of speech
                posArray.append(line)
            else:
                # preprocess punctuation
                for i in range(len(line)):
                    if line[i] in string.punctuation:
                        line[i] = "O"
                # entity type / set
                entityArray.append(line)
                if len(line) >= 2:
                    startEnt[line[0]] = startEnt.get(line[0], {})
                    startEnt[line[0]][line[1]] = startEnt[line[0]].get(line[1], 0) + 1
                    endEnt[line[-1]] = endEnt.get(line[-1], 0) + 1
                iLoop = 0

    # return arrays
    return textArray, posArray, entityArray, startEnt, endEnt

# build data into dictionary objects
def buildData(textArray, posArray, entityArray):
    entityDict = dict()
    wordDict = dict()
    tagDict = dict()
    wordSums = dict()
    entSums = dict()

    for i in range(len(textArray)):
        for j in range(len(textArray[i])):
            # textDict, posDict, entityDict
            word = textArray[i][j]
            tag = posArray[i][j]
            entity = entityArray[i][j]

            wordDict[entity] = wordDict.get(entity, {})
            wordDict[entity][word] = wordDict[entity].get(word, 0) + 1
            entSums[entity] = entSums.get(entity, 0) + 1

            tagDict[entity] = tagDict.get(entity, {})
            tagDict[entity][tag] = tagDict[entity].get(tag, 0) + 1

            if j >= 2:
                entity_one = entityArray[i][j-2]
                entity_two = entityArray[i][j-1]
                entity_three = entity
                entityDict[entity_one] = entityDict.get(entity_one, {})
                entityDict[entity_one][entity_two] = entityDict[entity_one].get(entity_two, {})
                entityDict[entity_one][entity_two][entity_three] = entityDict[entity_one][entity_two].get(entity_three, 0) + 1

    return entityDict, wordDict, tagDict, entSums
