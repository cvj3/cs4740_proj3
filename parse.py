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

    quit()


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
            line = line.strip().split("\t")
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
                    raise Exception("readline error; array size mismatch!")

    # return arrays
    return textArray, posArray, entityArray


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
