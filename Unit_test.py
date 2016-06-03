import unittest
from Main_engine import *
class Test_dictionary(unittest.TestCase):
    #Tests the dictionary class
    @classmethod
    def setUpClass(cls):
        cls.dictionary = dictionary()

    def test_input_all_caps(self):
        self.assertFalse(
            self.dictionary._check_valid_input("LIFE"),
            "All values are capitals.Expected: False")

    def test_input_starts_with_caps(self):
        self.assertFalse(
            self.dictionary._check_valid_input("Sacred"),
            "First letter is capital.Expected: False")

    def test_input_is_empty(self):
        self.assertFalse(
            self.dictionary._check_valid_input(""),
            "No Values.Expected: False")
        
    def test_input_not_str(self):
        self.assertFalse(
            self.dictionary._check_valid_input("42"),
            "All values are integers. Expected: False")

    def test_input_has_punctuation(self):
        self.assertFalse(
            self.dictionary._check_valid_input("rock'n'roll"),
            "Punctuation in word. Expected: False")

class Test_game_logic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = game_logic()
        cls.main.start()
    #Tests accuracy of legal input
    def test_input_is_upper(self):
        self.assertFalse(
            self.main._check_user_input("A"),
            "Input is capital. Expected: False")

    def test_input_is_int(self):
        self.assertFalse(
            self.main._check_user_input("2"),
            "Input is an integer not an alphabet. Expected: False")

    def test_input_is_punctuation(self):
        self.assertFalse(
            self.main._check_user_input("$"),
            "Input is punctuation not an alphabet. Expected: False")

    def test_input_len_not_one(self):
        self.assertFalse(
            self.main._check_user_input("as"),
            "Input is longer than one. Expected: False")
    #tests all the alphabet is valid 
    def test_valid_input(self):
        for i in range(26):
            self.assertTrue(
            self.main._check_user_input(chr(97+i)),
            "{} is valid. Expected: True".format(chr(97+i)))

    def test_word_hello(self):
        self.main.start()
        self.main.cur_word = "hello"
        self.main.mys_word = "_ " * (len(self.main.cur_word))
        self.assertFalse(
            self.main.is_win(),
            "Player should not have won. Expected: False")
        test_chr = 'h'
        self.assertEqual(
            self.main.check_word(test_chr),
            2,
            "{0} is in {1}. Expected: 2".format(test_chr, self.main.cur_word))
        self.assertFalse(
            self.main.is_win(),
            "Player should not have won. Expected: False")
        test_chr = 'e'
        self.assertEqual(
            self.main.check_word(test_chr),
            2,
            "{0} is in {1}. Expected: 2".format(test_chr, self.main.cur_word))
        self.assertFalse(
            self.main.is_win(),
            "Player should not have won. Expected: False")
        test_chr = 'l'
        self.assertEqual(
            self.main.check_word(test_chr),
            2,
            "{0} is in {1}. Expected: 2".format(test_chr, self.main.cur_word))
        self.assertFalse(
            self.main.is_win(),
            "Player should not have won. Expected: False")
        test_chr = 'o'
        self.assertEqual(
            self.main.check_word(test_chr),
            2,
            "{0} is in {1}. Expected: 2".format(test_chr, self.main.cur_word))
        self.assertTrue(
            self.main.is_win(),
            "Player should have won. Expected: True")
        

    def test_word_world(self):
        self.main.start()
        self.main.cur_word = "world"
        self.main.mys_word = "_ " * (len(self.main.cur_word))
        test_chr = 'a@ds4'
        self.assertEqual(
            self.main.check_word(test_chr),
            0,
            "{0} is not a valid input. Expected: 0".format(test_chr))
        test_chr = 's'
        self.assertEqual(
            self.main.check_word(test_chr),
            1,
            "{0} is not in {1}. Expected: 1".format(test_chr, self.main.cur_word))
        test_chr = 'w'
        self.assertEqual(
            self.main.check_word(test_chr),
            2,
            "{0} is in {1}. Expected: 2".format(test_chr, self.main.cur_word)) 


    #template for testing specific words
    """def test_word_(self):
        self.main.start()
        self.main.cur_word = ""
        self.main.mys_word = "_ " * (len(self.main.cur_word))
        test_chr = ''
        self.assertEqual(
            self.main.check_word(test_chr),
            0,
            "{0} is not a valid input. Expected: 0".format(test_chr))
        test_chr = ''
        self.assertEqual(
            self.main.check_word(test_chr),
            1,
            "{0} is not in {1}. Expected: 1".format(test_chr, self.main.cur_word))
        test_chr = ''
        self.assertEqual(
            self.main.check_word(test_chr),
            2,
            "{0} is in {1}. Expected: 2".format(test_chr, self.main.cur_word))    
        self.assertFalse(
            self.main.is_win(),
            "Player should not have won. Expected: False")
        self.assertTrue(
            self.main.is_win(),
            "Player should have won. Expected: True")

    """


if __name__ == "__main__":
    unittest.main()