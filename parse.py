import os
# import sys


__author__ = "Alin Barsan, Curtis Josey"


# param1 = path, param2 = filename
def main(param1, param2):
    # Read and Parse XML
    textArray, posArray, entityArray = readData(param1, param2, False)

    # build Data
    combinedDict, wordDict, tagDict = buildData(textArray, posArray, entityArray)

    # Write out to a dictionary file (lib/data.py)
    writeData('data', 'combined.py', 'combinedDict', combinedDict)
    writeData('data', 'word.py', 'wordDict', wordDict)
    writeData('data', 'tag.py', 'tagDict', tagDict)

def readData(path, filename, verboseMode=False):
    textArray = []
    posArray = []
    entityArray = []

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path + '/' + filename)

    # loop until done
    with open(filename) as f:
        iLoop = 0
        # read / parse 3 lines at a time
        for line in f:
            iLoop += 1
            if iLoop == 3: line = line.replace("I-", "").replace("B-", "")
            line = line.strip().split() #split with no args splits on whitespace.  Train is tab deliminated.  Test is not.
            if iLoop == 1:
                textArray += line
            elif iLoop == 2:
                posArray += line
            else:
                entityArray += line
                iLoop = 0

                # verify all three arrays are equal size, else throw error
                if (len(textArray) != len(posArray)) or \
                        (len(textArray) != len(entityArray)):
                    raise Exception("readline error; array size mismatch! " + str(line))

    # return arrays
    return textArray, posArray, entityArray

def readTestData(path, filename, verboseMode=False):
    textArray, posArray, positionArray = readData(path, filename, verboseMode)
    tests = []
    for i in range(len(textArray)):
        tests.append((textArray[i], posArray[i], positionArray[i]))
    return tests

# build data into dictionary objects
def buildData(textArray, posArray, entityArray):
    combinedDict = dict()
    wordDict = dict()
    tagDict = dict()

    for i in range(len(textArray)):
        # textDict, posDict, entityDict
        word = textArray[i]
        tag = posArray[i]
        entity = entityArray[i]
        combined = word + "|" + tag

        wordDict[word] = wordDict.get(word, {})
        wordDict[word][entity] = wordDict[word].get(entity, 0) + 1

        tagDict[tag] = tagDict.get(tag, {})
        tagDict[tag][entity] = tagDict[tag].get(entity, 0) + 1

        combinedDict[combined] = combinedDict.get(combined, {})
        combinedDict[combined][entity] = combinedDict[combined].get(entity, 0) + 1

    return combinedDict, wordDict, tagDict


# write dataset to dictionary object file
def writeData(path, filename, varname, dictionaryObject, verboseMode=False):
    f = open(path + "/" + filename, "w")
    output = str(dictionaryObject).replace("{", "{\n\t").replace("}", "\n}").replace("},\n\t", "},\n").replace("\t", "", 1)
    # No longer replacing space after comma with newline since it messes up strings containing commas
    # As a result, generated .py files are less readable.
    output = varname + ' = ' + output
    f.write(output)
    f.close()

def write_predictions_to_file(predictions, filename="results.csv"):
    output = "Type,Prediction"
    terms = ["PER", "LOC", "ORG", "MISC"]
    for term in terms:
        output += "\n" + term + ","
        spree = False
        for i in range(len(predictions[term])-1):
            c = predictions[term][i]
            n = predictions[term][i+1]
            if not spree: output += c + "-"
            if int(n) == (int(c) + 1):
                spree = True
            else:
                spree = False
                output += c + " "
    f = open("results/" + filename, "w")
    f.write(output)
    f.close()
