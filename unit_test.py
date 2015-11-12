from common import *
from config import *
from parse_bigram import prepareUnitTestData, writeUnitTestFile, \
    scoreUnitTestResults, readTestDataBaseline
from predict_bigram import get_baseline_predictions
if BIGRAM:
    from parse_bigram import main
    from predict_bigram import get_hmm_predictions
else:
    from parse_trigram import main
    from predict_trigram import get_hmm_predictions


__author__ = "Alin Barsan, Curtis Josey"


if __name__ == "__main__":
    # main("data", "train.txt")
    # capture start time for metrics
    start("")
    tests, expected_results = prepareUnitTestData("data", TRAIN_FILENAME, 3000)
    writeUnitTestFile(tests)
    predictions = get_hmm_predictions(tests)
    end("\nRan %d Tests" % len(tests))

    print "\nHMM RESULTS"
    scoreUnitTestResults(predictions, expected_results)
    predictions_baseline = get_baseline_predictions(
        readTestDataBaseline("data", "large_unit_test.txt"))

    print "\nBASELINE RESULTS"
    scoreUnitTestResults(predictions_baseline, expected_results)
