import os
import sys


__author__ = "Alin Barsan, Curtis Josey"


# param1 = path, param2 = filename
def main(param1, param2):
    # Read and Parse XML
    textArray, posArray, entityArray = readData(param1, param2, False)

    # Write out to a dictionary file (lib/data.py)
    # writeData(param1, param2, wsdData)

    quit()


def readData(path, filename, verboseMode=False):
    textArray = []
    posArray = []
    entityArray = []

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path + '/' + filename)

    # loop until done
    with open(filename) as f:
        textBuffer = ""
        posBuffer = ""
        entityBuffer = ""

        # read / parse 3 lines at a time
        textBuffer = f.readlines()
        posBuffer = f.readlines()
        entityBuffer = f.readlines()

        textLine = []
        posLine = []
        entityLine = []

        # split on tab, append to array
        textLine = textBuffer.split("\t")
        posLine = posBuffer.split("\t")
        entityLine = entityBuffer.split("\t")

        print textLine
        print posLine
        print entityLine

        # verify all three arrays are equal in element size, else throw error
        if (len(textLine) != len(posLine)) or \
                (len(textLine) != len(entityLine)):
            raise Exception("readline error; array size mismatch!")

        textArray.append(textLine)
        posArray.append(posLine)
        entityArray.append(entityLine)

    # return arrays
    return textArray, posArray, entityArray
