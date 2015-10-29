import parse  # import main as parse_main
from predict import get_baseline_predictions, get_hmm_predictions
from common import *
from config import *

__author__ = "Alin Barsan, Curtis Josey"

if __name__ == "__main__":
	parse.main("data", "train.txt")
	#predictions = get_baseline_predictions(parse.readTestDataBaseline("data", "test.txt"))

    start("Start Parsing Test Data")
    tests = parse.readTestData("data", TEST_FILENAME)
    end("Finished Parsing Test Data")

    start("Start Generating Predictions")
    predictions = get_hmm_predictions(tests)
    end("Finished Generating Predictions")

    start("Start Writing Predictions")
    write_predictions_to_file(predictions)
    end("Finished Writing Predictions")
