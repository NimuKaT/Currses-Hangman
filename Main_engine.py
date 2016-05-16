class read_file():
	def __init__(self, path):
		
		
		self.file = open(path, "r")
		self.data = []
		
		for line in self.file:
			self.data.append(line)		
	
	def get_data(self):
		return self.data

	def close(self):
		self.__del__()
	
	def __del__(self):
		pass
	
class main():
	def __init__(self):
		dict = read_file("Dictionary.txt")
		print(dict.get_data())
		dict.close()
		print(dict.get_data())

	
	def launch(self):
		pass
	
	def check_valid_input(self):
		pass
	
	