from enum import Enum
import os.path

class Dict_Param(Enum):
    add = 1
    remove = 2
    change = 3

class read_file:
    def __init__(self, path):

        #Test the path is valid
        assert(isinstance(path,str))
        assert(os.path.isfile(path))

        #Save data from file in array and exit file
        self.data = []
        with open(path, 'r') as file:
            for line in file:
                self.data.append(line.strip())	

    #Return values of file
    def get_data(self):
        return self.data

class write_file:
    def __init__(self, path, new_data):

        #Test path and new data is valid		
        assert(isinstance(path,str))
        assert(isinstance(new_data, list))

        #Replace data in file
        with open(path, 'w') as file:
            file.write("\n".join(new_data)) 

class dictionary:
    def __init__(self):
        self.DICT_PATH = "Dictionary.txt"
        self.dict_in = read_file(self.DICT_PATH)
        self.dict_list = self.dict_in.get_data()

    def edit_dict(self, param, word1, word2=False):
        self.flag = False
        self.new_data = self.dict_list

        assert(isinstance(self.new_data, list))
        assert(param in Dict_Param)

        if param == Dict_Param.add and self.check_valid_input(word1):
            if not word1 in self.new_data:
                self.new_data.append(word1)
                write_file(self.DICT_PATH, self.new_data)
                self.flag = True

        elif param == Dict_Param.remove and self.check_valid_input(word1):
            if word1 in self.new_data:
                del new_data[new_data.index(word1)]
                write_file(self.DICT_PATH, self.new_data)
                self.flag = True
        
        elif param == Dict_Param.change and self.check_valid_input(word1) and self.check_valid_input(word2):
            if word1 in self.new_data:
                if not word2 in self.new_data:
                    self.new_data[new_data.index(word1)] = word2
                    write_file(self.DICT_PATH, self.new_data)
                    self.flag = True
        return self.flag

    def check_valid_input(self, input):

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




if __name__ == "__main__":
	
    inputs = []
    dict_list = dictionary()

    while not inputs == None:
        
        inputs = input("Enter command then the word: ").split()

        if len(inputs) == 2:
        
            if dict_list.check_valid_input(inputs[1]):
                pass
            
            elif inputs[0] == "add":
                dict_list.edit_dict(Dict_Param.add, inputs[1])

            elif inputs[0] == "remove":
                dict_list.edit_dict(Dict_Param.remove, inputs[1])

        elif inputs[0] == "change" and len(inputs) == 3:
            if dict_list.check_valid_input(inputs[1]) and dict_list.check_valid_input(inputs[2]):
                dict_list.edit_dict(Dict_Param.change, inputs[1], inputs[2])

        if inputs[0] == "close":
            break