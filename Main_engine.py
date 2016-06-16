"""
	Created by: Takumi Iwasa
	Date: 		17/05/2016
	
"""
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
        #Save data from file at path into an array and closes file
        self.data = []
        with open(path, 'r') as file:
            for line in file:
                self.data.append(line.strip())	

    def get_data(self):
        #Return the data of the file as an array of strings
        return self.data

class write_file:
    def __init__(self, path, new_data):
        #Replace data in file with new_data into path
        with open(path, 'w') as file:
            file.write("\n".join(new_data)) 

class dictionary:
    
    def __init__(self):
        #Loads dictionary file into an array
        self.DICT_PATH = "Dictionary.txt"
        self.dict_list = read_file(self.DICT_PATH).get_data()

    def edit_dict(self, param, word1, word2=False):
        #Edits the dictionary add, remove and change *may be remove
        #Returns false if the input are invalid
        flag = False
        self.new_data = self.dict_list

        #Adds the word into the dictionary if valid and new
        if (param == Dict_Param.add and
            self._check_valid_input(word1)):

            if not word1 in self.new_data:
                self.new_data.append(word1)
                write_file(self.DICT_PATH, self.new_data)
                flag = True

        #Removes the word if in the dictionary
        elif (param == Dict_Param.remove and
            self._check_valid_input(word1)):

            if word1 in self.new_data:
                del self.new_data[self.new_data.index(word1)]
                write_file(self.DICT_PATH, self.new_data)
                flag = True
        
        #Edits the word by removing the old word and adding the new word if valid
        elif (param == Dict_Param.change and
            self._check_valid_input(word1) and
            self._check_valid_input(word2)):

            if word1 in self.new_data:

                if not word2 in self.new_data:
                    self.new_data[self.new_data.index(word1)] = word2
                    write_file(self.DICT_PATH, self.new_data)
                    flag = True
        self.dict_list = self.new_data

        return flag

    def _check_valid_input(self, input):
        #Test if input is a valid word in terms of
        #capitals, symbols, spaces and if any value is present
        flag = False
        
        if (input.isalpha() and input.islower()): 
            flag = True
    
        return flag

    def _sort_dict(self):
        #Checks the words in the file and choices only valid characters
        self.dict_sorted =[]
        for word in self.dict_list:
            if self._check_valid_input(word):
                self.dict_sorted.append(word)
        
    def return_dictionary(self):
        #Sorts the dictionary and then returns as an array of strings
        self._sort_dict()
        return self.dict_sorted

class game_logic:

    def __init__(self):
        self.OPTION_PATH = "Data.txt"
        self.option_file = read_file(self.OPTION_PATH)
        self.raw_option = self.option_file.get_data()
        self.option = {}
        self.arrange_options()
        self.dictionary = dictionary()

    def arrange_options(self):
        #Reads the options from the text file into the dictionary option
        for param in self.raw_option:
            self.split_option = param.split(":")
            self.option[self.split_option[0]] = self.split_option[1].strip()

    def check_user_input(self, guess):
        flag = False
        if (len(guess) == 1 and
            guess.isalpha()):
            flag = True
        return flag

    def _check_user_input(self, guess):
        #Returns true if the user input is a single character
        #If not returns false
        flag = False
        if (len(guess) == 1 and
            guess.isalpha() and
            guess.islower()):
            flag = True
        return flag

    def is_guessed(self, guess):
        #Returns true if character has been guessed
        flag = False
        if self._check_user_input(guess):
            if self.guess_char[guess]:
                flag = True
        return flag

    def check_word(self, guess):
        #Checks if the character is within the word returning a boolean
        #Returns true if guess is contained in word
        #Returns false if not
        flag = False

        if (not self.is_guessed(guess)):
            self.guess_char[guess] = True
            if (guess in self.cur_word):
                flag = True
                new_word = list(self.mys_word)
                for i, letter in enumerate(self.cur_word):
                    if (guess == letter):
                        new_word[2*i] = letter
                    self.mys_word = "".join(new_word)
            else:
                self.guess_counter += 1
        return flag

    def _sort_dict(self):
        #Sort the dictionary to only contain words of certain length
        #Depending on the options or difficulty
        for word in self.dictionary.return_dictionary():
            if (str(len(word)) == str(self.option["Word_length"])):
                self.dict_statified.append(word)

    def start(self):
        #Temporary game initialize function
        self._init_values()

    def _init_values(self):
        #Initialize all variables for a new game
        #Dictionary of each character in the alphabet
        self.guess_counter = 0
        
        #Re-sorts the dictionary using current value in option
        self.dict_statified = []
        self._sort_dict()
        
        #Selects a random word from dictionary and make a string with '_' followed
        #with a space
        self.cur_word = random.choice(self.dict_statified)
        self.mys_word = "_ " * (len(self.cur_word))
        
        #Creates a dictionary that contains all the lower case alphabet which
        #indicates whether a letter has been guessed
        self.guess_char = {}
        for i in range(26):
            self.guess_char[chr(97+i)] = False

    def get_mystery_word(self):
        #Return mystery word as string
        return self.mys_word

    def is_win(self):
        #Returns True if no _ are present in the mystery word
        flag = False
        if self.guess_counter <= int(self.option['Max_guess']):
            if ('_' not in self.mys_word):
                flag = True
        return flag

    def is_lose(self):
        #Returns True if a '_' is present and guess_counter is greater than Max_guess
        flag = False
        if (self.guess_counter >= int(self.option['Max_guess'])):
            if ('_' in self.mys_word):
                flag = True
        return flag

    def get_guessed_char(self):
        #Returns the dictionary containing whether a character has been guessed
        return self.guess_char

    def return_options(self, key):
        return_value = False
        if (key in self.option):
            return_value = self.option[key]
        return return_value

    def change_options(self, key, value):
        flag = False
        if key in self.option:
            self.option[key] = value
            self.update_options()
            flag = True
        return flag

    def update_options(self):
        data = []
        for key, value in self.option.items():
            data.append('{}: {}'.format(key, value))
        write_file(self.OPTION_PATH, data)

    def return_count(self):
        return self.guess_counter


#Class for testing classes in a command-line interface
class temp_run_game:
	
    def __init__ (self):
        self.dict_list = dictionary()
        self.test_run_ascii_game()

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

    def test_run_ascii_game(self):
        game = game_logic()
        game.start()
        game.update_options()
        while True:
			
            if (game.is_win()):
                print ('You won!')
                break
            elif (game.is_lose()):
                print ('You lose. The word was: {}'.format(game.cur_word))
                break

            print ('\n', game.get_mystery_word())
            usr_input = input("Guess a character: ")
            if (usr_input == "exit"):
                break
            valid_input = game.check_user_input(usr_input)
            is_guessed = game.is_guessed(usr_input)
            in_word = game.check_word(usr_input)
            if (not valid_input):
                print ("{} is not a valid character".format(usr_input))
            elif (is_guessed):
                print ("{} is already guessed".format(usr_input))
            elif (not in_word):
                print ("{} is not in word".format(usr_input))
            elif (in_word):
                print ("{} in word".format(usr_input))


if __name__ == "__main__":
    temp_run_game()
