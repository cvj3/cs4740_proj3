import os
import string
from common import writeData
# import sys


__author__ = "Alin Barsan, Curtis Josey"


# param1 = path, param2 = filename
def main(param1, param2):
    # Read and Parse XML
    textArray, posArray, entityArray, startEnt, endEnt = \
        readData(param1, param2, False)

    # build Data
    baseCombinedDict, baseWordDict, baseTagDict, entityDict, \
        combined, word, tag = \
        buildData(textArray, posArray, entityArray)

    # Write out to a dictionary file (lib/data.py)
    writeData('data', 'base_combined.py', 'combinedDict', baseCombinedDict)
    writeData('data', 'base_words.py', 'wordDict', baseWordDict)
    writeData('data', 'base_tagged.py', 'tagDict', baseTagDict)
    writeData('data', 'entity.py', 'entityDict', entityDict)
    writeData('data', 'combined.py', 'combinedDict', combined)
    writeData('data', 'words.py', 'wordDict', word)
    writeData('data', 'tagged.py', 'tagDict', tag)
    writeData('data', 'start_entity.py', 'startEnt', startEnt)
    writeData('data', 'end_entity.py', 'endEnt', endEnt)


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

            # if iLoop == 3: line = line.replace("I-", "").replace("B-", "")
            # split with no args accomodates 'whitespace' (tabs or spaces)
            line = line.strip().split()
            if iLoop == 1:
                # words
                textArray += line
            elif iLoop == 2:
                # preprocess punctuation
                for i in range(len(line)):
                    if line[i] in string.punctuation:
                        line[i] = "."
                # part of speech
                posArray += line
            else:
                # preprocess punctuation
                for i in range(len(line)):
                    if line[i] in string.punctuation:
                        line[i] = "O`"
                # entity type / set
                entityArray += line
                startEnt[line[0]] = startEnt.get(line[0], 0) + 1
                endEnt[line[-1]] = endEnt.get(line[-1], 0) + 1
                iLoop = 0

                # verify all three arrays are equal size, else throw error
                if (len(textArray) != len(posArray)) or \
                        (len(textArray) != len(entityArray)):
                    raise Exception("training err: array mismatch! " + str(line))

    # return arrays
    return textArray, posArray, entityArray, startEnt, endEnt


def readTestDataBaseline(path, filename, verboseMode=False):
    textArray, posArray, positionArray = readData(path, filename, verboseMode)
    tests = []
    for i in range(len(textArray)):
        tests.append((textArray[i], posArray[i], positionArray[i]))
    return tests


def readTestData(path, filename, verboseMode=False):
    tests = []

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path + '/' + filename)

    # loop until done
    with open(filename) as f:
        iLoop = 0
        # read / parse 3 lines at a time
        test = []
        # first element of test is list of word tokens
        # second element of test is list of pos tags
        # third element of test is list of positions
        for line in f:
            iLoop += 1
            # split with no args accomodates 'whitespace' (tabs or spaces)
            line = line.strip().split()
            if iLoop == 2:
                # pre-process [part of speech]: convert punct to "."
                for i in range(len(line)):
                    if line[i] in string.punctuation:
                        print line[i]
                        line[i] = "."
                        print line[i]
                print line
            test.append(line)
            if iLoop == 3:
                tests.append((test[0], test[1], test[2]))
                test = []
                iLoop = 0

    return tests


# build data into dictionary objects
def buildData(textArray, posArray, entityArray):
    bcombinedDict = dict()
    bwordDict = dict()
    btagDict = dict()
    entityDict = dict()
    combinedDict = dict()
    wordDict = dict()
    tagDict = dict()

    for i in range(len(textArray)):
        # textDict, posDict, entityDict
        word = textArray[i]
        tag = posArray[i]
        entity = entityArray[i]
        combined = word + "|" + tag

        bwordDict[word] = bwordDict.get(word, {})
        bwordDict[word][entity] = bwordDict[word].get(entity, 0) + 1

        btagDict[tag] = btagDict.get(tag, {})
        btagDict[tag][entity] = btagDict[tag].get(entity, 0) + 1

        bcombinedDict[combined] = bcombinedDict.get(combined, {})
        bcombinedDict[combined][entity] = bcombinedDict[combined].get(entity, 0) + 1

        wordDict[entity] = wordDict.get(entity, {})
        wordDict[entity][word] = wordDict[entity].get(word, 0) + 1

        tagDict[entity] = tagDict.get(entity, {})
        tagDict[entity][tag] = tagDict[entity].get(tag, 0) + 1

        combinedDict[entity] = combinedDict.get(entity, {})
        combinedDict[entity][combined] = combinedDict[entity].get(combined, 0) + 1

        if i >= 1:
            entity_prev = entityArray[i-1]
            entityDict[entity_prev] = entityDict.get(entity_prev, {})
            entityDict[entity_prev][entity] = entityDict[entity_prev].get(entity, 0) + 1

    return bcombinedDict, bwordDict, btagDict, entityDict, combinedDict, wordDict, tagDict
