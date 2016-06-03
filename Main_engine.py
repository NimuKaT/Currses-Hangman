import unittest
from enum import Enum
import os.path
import random

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
        flag = False
        self.new_data = self.dict_list

        if (param == Dict_Param.add and
        	self.check_valid_input(word1)):

            if not word1 in self.new_data:
                self.new_data.append(word1)
                write_file(self.DICT_PATH, self.new_data)
                flag = True

        elif (param == Dict_Param.remove and
        	self.check_valid_input(word1)):

            if word1 in self.new_data:
                del self.new_data[self.new_data.index(word1)]
                write_file(self.DICT_PATH, self.new_data)
                flag = True
        
        elif (param == Dict_Param.change and
        	self.check_valid_input(word1) and
        	self.check_valid_input(word2)):

            if word1 in self.new_data:

                if not word2 in self.new_data:
                    self.new_data[self.new_data.index(word1)] = word2
                    write_file(self.DICT_PATH, self.new_data)
                    flag = True
        self.dict_list = self.new_data

        return flag

    def check_valid_input(self, input):
    	#Test if input is a valid word in terms of
    	#capitals, symbols, spaces and emptiness
        flag = False
        
        if (input.isalpha() and input.islower()): 
            flag = True
        
        return flag

    def sort_dict(self):
        #checks the words in the file and choices only valid characters
        self.dict_sorted =[]
        for word in self.dict_list:
            if self.check_valid_input(word):
                self.dict_sorted.append(word)
        
    def return_dictionary(self):
        #returns array of valid words
        self.sort_dict()
        return self.dict_sorted

class main:

    def __init__(self):
        self.OPTION_PATH = "Data.txt"
        self.option_file = read_file(self.OPTION_PATH)
        self.raw_option = self.option_file.get_data()
        self.option = {}
        self.arrange_options()
        self.dictionary = dictionary()
        self.init_values()
        self.tmp_start()

    def arrange_options(self):
        for param in self.raw_option:
            self.split_option = param.split(":")
            self.option[self.split_option[0]] = self.split_option[1].strip()

    def check_user_input(self, guess):
        flag = False
        if (len(guess) == 1):
            if self.guess_char[guess] == False:
                self.check_word(guess)
                self.guess_char[guess] = True
                flag = True
        return flag

    def check_word(self, guess):
        flag = False
        if (guess in self.cur_word):
            flag = True
            new_word = list(self.mis_word)
            for i, letter in enumerate(self.cur_word):
                if (guess == letter):
                    new_word[2*i] = letter
            self.mis_word = "".join(new_word)
        return flag


    def sort_dict(self):
        #Sort the dictionary to only contain words of certain length
        #depending on the options or difficulty
        for word in self.dictionary.return_dictionary():
            if (str(len(word)) == str(self.option["Word_length"])):
                self.dict_statified.append(word)

    def tmp_start(self):
        self.init_values()
        print (self.mis_word)
        self.check_word('a')
        print (self.mis_word)

    def init_values(self):
        #initialise all variables for a new game
        self.dict_statified = []
        self.sort_dict()
        self.cur_word = random.choice(self.dict_statified)
        self.mis_word = "_ " * len(self.cur_word)
        print(self.cur_word)
        self.guess_char = {}
        for i in range(26):
            self.guess_char[chr(97+i)] = False






class temp_run_game:
	
	def __init__ (self):
		self.dict_list = dictionary()

	def test_run_dict_edit(self):
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

				elif (self.inputs[0] == "change" and
                 len(self.inputs) == 3 and
					self.dict_list.check_valid_input(self.inputs[1]) and
					self.dict_list.check_valid_input(self.inputs[2])):

						self.dict_list.edit_dict(Dict_Param.change, self.inputs[1], self.inputs[2])

			if self.inputs[0] == "close":
				break

if __name__ == "__main__":
    main()
