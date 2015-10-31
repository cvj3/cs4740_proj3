from config import *
from parse_bigram import readTestData
if BIGRAM: 
    from parse_bigram import main
    from predict_bigram import get_hmm_predictions
else:
    from parse_trigram import main
    from predict_trigram import get_hmm_predictions
from common import *


__author__ = "Alin Barsan, Curtis Josey"

if __name__ == "__main__":
    main("data", "train.txt")

    start("Start Parsing Test Data")
    tests = readTestData("data", "test.txt")
    end("Finished Parsing Test Data")

    start("Start Generating Predictions")
    predictions = get_hmm_predictions(tests)
    end("Finished Generating Predictions")

    start("Start Writing Predictions")
    write_predictions_to_file(predictions, "trigram-add-one-always-no-end-scaling.csv")
