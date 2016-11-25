import unittest
import smell_datamine_categorized

def test_sentence_with_multiple_smell_type(self):
    sentence = "The dead bodies smell of lavatories."
    result = smell_datamine_categorized.find_smell_type(sentence)
    self.asserEqual(["decomposition", "school"], result)
    self.asserEqual("decomposition", result)

if __name__ == '__main__':
	unittest.main()