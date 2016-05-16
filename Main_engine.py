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

	def edit_dict(self, param, word1, word2=False):
		

		dict_in = read_file(self.DICT_PATH)
		dict_list = dict_in.get_data()

		assert(isinstance(dict_list, list))
		assert(param in Dict_Param)

		if param == Dict_Param.add:
			if not word1 in dict_list:
				new_data = dict_list
				new_data.append(word1)
				write_file(self.DICT_PATH, new_data)

		elif param == Dict_Param.remove:

			if word1 in dict_list:
				new_data = dict_list
				del new_data[new_data.index(word1)]
				write_file(self.DICT_PATH, new_data)

		elif param == Dict_Param.change:
			if word1 in dict_list:
				if not word2 in dict_list:
					new_data = dict_list
					new_data[new_data.index(word1)] = word2
					write_file(self.DICT_PATH, new_data)

	def check_valid_input(self):
		pass


	def tmp_dic_handler(self):
		self.inputs = []
		
		while not self.inputs == None:
			self.inputs = input("Enter command then the word: ").split()

			if len(self.inputs) == 2:
				if self.inputs[0] == "add":
					self.edit_dict(Dict_Param.add, self.inputs[1])

				elif self.inputs[0] == "remove":
					self.edit_dict(Dict_Param.remove, self.inputs[1])

			elif self.inputs[0] == "change" and len(self.inputs) == 3:
					self.edit_dict(Dict_Param.change, self.inputs[1], self.inputs[2])

			if self.inputs[0] == "close":
				break


class main:

	def __init__(self):
	#	self.dict = dictionary()
	#	self.dict.tmp_dic_handler()
	
	


main()