import unittest
from enum import Enum
import os.path

class Dict_Param(Enum):
    add = 1
    remove = 2
    change = 3

class read_file:
    def __init__(self, path):
		#Save data from file in array and close file
        self.data = []
        with open(path, 'r') as file:
            for line in file:
                self.data.append(line.strip())	

    def get_data(self):
        #Return values of file as an array
        return self.data

class write_file:
    def __init__(self, path, new_data):
        #Replace data in file
        with open(path, 'w') as file:
            file.write("\n".join(new_data)) 

class dictionary:
    
    def __init__(self):
    	#Loads dictionary file into memory
        self.DICT_PATH = "Dictionary.txt"
        self.dict_in = read_file(self.DICT_PATH)
        self.dict_list = self.dict_in.get_data()

    def edit_dict(self, param, word1, word2=False):
        #Edits the dictionary add, remove and change *may be remove
        self.flag = False
        self.new_data = self.dict_list

        if (param == Dict_Param.add and
        	self.check_valid_input(word1)):

            if not word1 in self.new_data:
                self.new_data.append(word1)
                write_file(self.DICT_PATH, self.new_data)
                self.flag = True

        elif (param == Dict_Param.remove and
        	self.check_valid_input(word1)):

            if word1 in self.new_data:
                del self.new_data[self.new_data.index(word1)]
                write_file(self.DICT_PATH, self.new_data)
                self.flag = True
        
        elif (param == Dict_Param.change and
        	self.check_valid_input(word1) and
        	self.check_valid_input(word2)):

            if word1 in self.new_data:

                if not word2 in self.new_data:
                    self.new_data[self.new_data.index(word1)] = word2
                    write_file(self.DICT_PATH, self.new_data)
                    self.flag = True

        return self.flag

    def check_valid_input(self, input):
    	#Test if input is a valid word in terms of
    	#capitals, symbols, spaces and emptiness
        self.valid_flag = False
        
        if input.isalpha(): 
            self.valid_flag = True
        
        return self.valid_flag

    def sort_dict(self):
        pass

class main:

    def __init__(self):
        pass

    def check_user_input(self):
        pass
    
    def sort_dict(self):
        pass

    def select_ran_word(self):
        pass

    def tmp_start(self):
        pass

    def check_word(self):
        pass

class Test_dictionary(unittest.TestCase):
	#Tests the dictionary class
	@classmethod
	def setUpClass(cls):
		cls.dictionary = dictionary()

	def test_input_all_caps(self):
		self.assertFalse(
			self.dictionary.check_valid_input("LIFE"),
			"All values are capitals.Expected: False")

	def test_input_start_with_caps(self):
		self.assertFalse(
			self.dictionary.check_valid_input("Sacred"),
			"First letter is capital.Expected: False")

	def test_input_not_empty(self):
		self.assertFalse(
			self.dictionary.check_valid_input(""),
			"No Values.Expected: False")
		
	def test_input_not_int(self):
		self.assertFalse(
			self.dictionary.check_valid_input("42"),
			"All values are integers. Expected: False")

class temp_run_game:
	
	def __init__ (self):
		self.dict_list = dictionary()

	def run(self):
		self.inputs = []

		while True:

			self.inputs = input("Enter command then the word: ").split()

			if len(self.inputs) >= 2:

				#Remove not once check_valid_input is reliable
				if (not self.dict_list.check_valid_input(self.inputs[1])):
					pass

				elif self.inputs[0] == "add":
					if (not self.dict_list.edit_dict(Dict_Param.add, self.inputs[1])):
						print ("new word is invalid or already in the dictionary")

				elif self.inputs[0] == "remove":
					if (not self.dict_list.edit_dict(Dict_Param.remove, self.inputs[1])):
						print ("removing word is invalid or not in the dictionary")

				elif (self.inputs[0] == "change" and len(self.inputs) == 3 and
					self.dict_list.check_valid_input(self.inputs[1]) and
					self.dict_list.check_valid_input(self.inputs[2])):

						self.dict_list.edit_dict(Dict_Param.change, self.inputs[1], self.inputs[2])

			if self.inputs[0] == "close":
				break


if __name__ == "__main__":
	unittest.main()

	