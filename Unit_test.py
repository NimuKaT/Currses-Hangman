import unittest
from Main_engine import *
class Test_dictionary(unittest.TestCase):
    #Tests the dictionary class
    @classmethod
    def setUpClass(cls):
        cls.dictionary = dictionary()

    def test_input_all_caps(self):
        self.assertFalse(
            self.dictionary.check_valid_input("LIFE"),
            "All values are capitals.Expected: False")

    def test_input_starts_with_caps(self):
        self.assertFalse(
            self.dictionary.check_valid_input("Sacred"),
            "First letter is capital.Expected: False")

    def test_input_is_empty(self):
        self.assertFalse(
            self.dictionary.check_valid_input(""),
            "No Values.Expected: False")
        
    def test_input_not_str(self):
        self.assertFalse(
            self.dictionary.check_valid_input("42"),
            "All values are integers. Expected: False")

    def test_input_has_punctuation(self):
        self.assertFalse(
            self.dictionary.check_valid_input("rock'n'roll"),
            "Punctuation in word. Expected: False")

class Test_main(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = main()


if __name__ == "__main__":
    unittest.main()