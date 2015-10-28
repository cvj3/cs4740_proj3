import parse  # import main as parse_main
from predict import get_baseline_predictions

__author__ = "Alin Barsan, Curtis Josey"

if __name__ == "__main__":
	parse.main("data", "train.txt")
	predictions = get_baseline_predictions(parse.readTestData("data", "test.txt"))
	parse.write_predictions_to_file(predictions)
