import parse  # import main as parse_main
from predict import get_baseline_predictions
from common import *

__author__ = "Alin Barsan, Curtis Josey"

if __name__ == "__main__":
	parse.main("data", "train.txt")
	predictions = get_baseline_predictions(parse.readTestDataBaseline("data", "test.txt"))
	write_predictions_to_file(predictions)