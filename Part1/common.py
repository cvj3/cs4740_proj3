import datetime
# cache system time prior to running code block
def start(message):
    global TIMER
    print "\n" + message
    TIMER = datetime.datetime.now()


# output current time - start time with debug msg
def end(message):
    global TIMER
    end = datetime.datetime.now()
    print "\n" + message + " in %s seconds.\n" % str((end-TIMER).seconds)
    TIMER = None

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