import unittest
import smell_datamine_multiprocessing

class SmellCategoryTest(unittest.TestCase):
	def test_sentence_with_multiple_smell_type(self):
	    sentence = "The dead bodies smell of lavatories."
	    smell_data_mine = smell_datamine_multiprocessing.SmellDataMine()
	    result = smell_data_mine.categorise_sentence(sentence)
	    self.assertEqual({"decomposition", "school"}, result)

	def test_sentence_with_multiple_words_for_same_smell_type(self):
	    sentence = "The dead bodies were dead like very dead seriously."
	    smell_data_mine = smell_datamine_multiprocessing.SmellDataMine()
	    result = smell_data_mine.categorise_sentence(sentence)
	    self.assertEqual({"decomposition"}, result)

	def test_sentence_with_no_smell_types(self):
	    sentence = "Kittens are fluffy."
	    smell_data_mine = smell_datamine_multiprocessing.SmellDataMine()
	    result = smell_data_mine.categorise_sentence(sentence)
	    self.assertEqual(set(), result)

	def test_sentence_with_multiple_words_for_different_smell_type(self):
	    sentence = "The dead bodies were found and excrement as well."
	    smell_data_mine = smell_datamine_multiprocessing.SmellDataMine()
	    result = smell_data_mine.categorise_sentence(sentence)
	    self.assertEqual({"decomposition", "waste_excrement", "animal"}, result)

	def test_tokenize_to_sentence(self):
		sentence = "Kittens are fluffy. I like ice cream."
		result = smell_datamine_multiprocessing.tokenize_to_sentence(sentence)
		self.assertEqual(["Kittens are fluffy.", "I like ice cream."], result)

	# def test_process_sample_file_1(self):
	# 	path = "Hogwarts.1915.x1234.txt"
	# 	smell_data_mine = smell_datamine_multiprocessing.SmellDataMine()
	# 	smell_data_mine.process_file(path, 1915, "Hogwards")
	# 	self.assertEqual([smell_datamine_multiprocessing.Smell('Hogwards', 'waste_excrement', 'They smell like dung.', 1915)], smell_data_mine.results)
	# 	self.assertEqual([], smell_data_mine.uncategorised)

if __name__ == '__main__':
	unittest.main()
