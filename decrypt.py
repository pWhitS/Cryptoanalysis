import copy

ENGLISH_WORDS_FN = "english_words.txt"
# PLAINTEXT_FN = "plaintext_dictionary.txt"

class DecryptionScheme:
	def __init__(self,ciphertext):
		self.word_length_freq_map = {}
		self.english_words_by_length = {}
		self.ciphertext = ciphertext
		# list of words in ciphertext sorted by freq of words of the same length in dict
		self.sorted_ciphertext = [] 
		self.cipherword_positions = {}
		self.head = None
		self.key = Key()

		self.init_word_length_freq_map()
		self.read_english_words()
		self.sort_ciphertext()

	def decrypt(self):
		self.head = Word(self.sorted_ciphertext[0],0,self.key,None,self)
		# Word(master.sorted_ciphertext[self.cipherword_number+1],cipherword_number+1,key,self,master)
		self.head.decrypt()
		sorted_plainwords = []
		plainwords = [None for i in range(len(self.sorted_ciphertext))]
		curr = self.head
		while (curr != None):
			if curr.plainword is None:
				raise Exception("A cipherword was not mapped. Our mapping failed :(")
			else:
				sorted_plainwords.append(curr.plainword)
			if curr.next == None:
				self.key = curr.key
			curr = curr.next
		if len(sorted_plainwords) < len(self.sorted_ciphertext):
			raise Exception("Enough words were not decrypted. Our mapping failed :(")
		for i in range(len(self.sorted_ciphertext)):
			cipherword = self.sorted_ciphertext[i]
			plainword = sorted_plainwords[i]
			plainwords[self.cipherword_positions[str(cipherword)]] = plainword
		return " ".join(plainwords)

	def print_key(self):
		print "Letter to Num:"
		print self.key.let_to_num
		print "Num to LEtter:"
		print self.key.num_to_let

	def init_word_length_freq_map(self):
		self.word_length_freq_map[1] = 1
		self.word_length_freq_map[2] = 140
		self.word_length_freq_map[3] = 853
		self.word_length_freq_map[4] = 3130
		self.word_length_freq_map[5] = 6919
		self.word_length_freq_map[6] = 11492
		self.word_length_freq_map[7] = 16882
		self.word_length_freq_map[8] = 19461
		self.word_length_freq_map[9] = 16693
		self.word_length_freq_map[10] = 11882
		self.word_length_freq_map[11] = 8374
		self.word_length_freq_map[12] = 5812
		self.word_length_freq_map[13] = 3676
		self.word_length_freq_map[14] = 2102
		self.word_length_freq_map[15] = 1159
		self.word_length_freq_map[16] = 583
		self.word_length_freq_map[17] = 229
		self.word_length_freq_map[18] = 107
		self.word_length_freq_map[19] = 39
		self.word_length_freq_map[20] = 29
		self.word_length_freq_map[21] = 11
		self.word_length_freq_map[22] = 4
		self.word_length_freq_map[23] = 2
		# self.word_length_freq_map[24] = 0 # no need to include words with freq 0
		self.word_length_freq_map[25] = 1
		# self.word_length_freq_map[26] = 0 # no need to include words with freq 0
		# self.word_length_freq_map[27] = 0 # no need to include words with freq 0
		self.word_length_freq_map[28] = 1

	def read_english_words(self):
		fileobj = open(ENGLISH_WORDS_FN, "r")
		for line in fileobj:
			word = line.strip()
			len_word = len(word)
			if len_word not in self.english_words_by_length:
				self.english_words_by_length[len_word] = []
			self.english_words_by_length[len_word].append(word)
		fileobj.close()

	def sort_ciphertext(self):
		cipher_words = self.ciphertext.split(" ")
		cipher_words = [word.split(",") for word in cipher_words]
		for word in cipher_words:
			for i in range(len(word)):
				word[i] = int(word[i])
		i = 0
		for cipherword in cipher_words:
			self.cipherword_positions[str(cipherword)] = i
			i += 1
		self.sorted_ciphertext = sorted(cipher_words, key=lambda word: self.word_length_freq_map[len(word)])
		# print "len" + str(len(self.sorted_ciphertext[0]))

	def print_sorted_ciphertext(self):
		print self.sorted_ciphertext

class Word:

	def __init__(self,cipherword,cipherword_number,key,prev,master):
		self.cipherword = cipherword
		self.cipherword_number = cipherword_number
		self.source_key = key
		self.key = copy.deepcopy(key)
		self.prev = prev
		self.master = master
		self.next = None
		self.plainword = None
		self.possible_guesses = None

	def decrypt(self):
		self.filter()
		if len(self.possible_guesses) == 0:
			raise KeyMappingException("Current mapping allows for no possible guess")
		# elif len(self.possible_guesses) == 1:
		# 	word = self.possible_guesses[0]
		# 	for i in range(len(cipherword)):
		# 		if not self.key.number_is_mapped(self.cipherword[i]):
		# 			self.key.add_map(cipherword[i],word[i])
		# 	self.plainword = word
		# 	self.next = Word(master.sorted_ciphertext[self.cipherword_number+1],cipherword_number+1,key,self,master)
		else:
			# print self.possible_guesses
			# print "num guesses" + str(len(self.possible_guesses))
			for word in self.possible_guesses:
				# print word
				try:
					# print self.cipherword
					# print word
					for i in range(len(self.cipherword)):
						if not self.key.number_is_mapped(self.cipherword[i]):
							self.key.add_map(self.cipherword[i],word[i])
					self.plainword = word
					# print "\n******\n"
					# print self.plainword
					# if self.prev:
					# 	print self.prev.plainword
					# 	if self.prev.prev:
							# print self.prev.prev.plainword
					# print "\n******\n"
					if (self.cipherword_number) < (len(self.master.sorted_ciphertext) - 1):
						# print "NEXT WORD: {0}".format(str(self.master.sorted_ciphertext[self.cipherword_number+1]))
						self.next = Word(self.master.sorted_ciphertext[self.cipherword_number+1],self.cipherword_number+1,self.key,self,self.master)
						# print "***** >>>>> ENTERING WORD {0} -> {1}".format(self.cipherword_number+1,str(self.master.sorted_ciphertext[self.cipherword_number+1]))
						self.next.decrypt()
						# print "***** >>>>> RETURNING TO WORD {0} -> {1}".format(self.cipherword_number,str(self.cipherword))
				except KeyMappingException as e:
					# print "***** >>>>> RETURNING TO WORD {0} -> {1}".format(self.cipherword_number,str(self.cipherword))
					# print "EXCEPTION: " + word
					self.plainword = None
					self.next = None
					# print "\n\n\nHERE ARE THE KEYS:\n\tSOURCE:\n\t\t{0}\n\n\tOLD:\n\t\t{1}\n\n\n".format(str(self.key.let_to_num),str(self.source_key.let_to_num))
					self.key = copy.deepcopy(self.source_key)
					continue
				else:
					break				
			if self.plainword == None:
				# print self.cipherword_number
				# print self.key.let_to_num
				raise KeyMappingException("All possible plainwords for cipherword {0} have been tried".format(str(self.cipherword)))

	def filter(self):
		sublist = self.master.english_words_by_length[len(self.cipherword)]
		# print "**** FILTERING WORD: {0}".format(str(self.cipherword))
		# if self.cipherword_number == 1:
		# 	CIPHERWORD1 = True
		# else:
		# 	CIPHERWORD1 = False
		# print "WORD NUM: {0}".format(self.cipherword_number)
		# print "SUBLIST:"
		# print "\tLENGTH: {0}".format(len(sublist))
		# print self.key.let_to_num
		# print "\tSELF: {0}".format(str(sublist))
		self.possible_guesses = []
		for word in sublist:
			good_word = True
			for i in range(len(self.cipherword)):
				# if CIPHERWORD1 and word == "abandonments":
				# 	print self.key.number_is_mapped(self.cipherword[i])
				# 	print self.cipherword[i]
				# 	print word[i]
				# 	print self.key.mapping_is_correct(word[i],self.cipherword[i])
				if word[i] == "'":
					good_word = False
					break
				if self.key.number_is_mapped(self.cipherword[i]):
					if not self.key.mapping_is_correct(word[i],self.cipherword[i]):
						good_word = False
						break
			if good_word:
				self.possible_guesses.append(word)
		# print "GUESSES:"
		# print "\tLENGTH: {0}".format(len(self.possible_guesses))
		# print "\tSELF: {0}".format(str(self.possible_guesses))





	# def decrypt_word(self):

class Key:
	# num_to_let = []
	# let_to_num = {}
	# letter_count = {}
	# letter_freq_map = {}

	def __init__(self):
		self.num_to_let = []
		self.let_to_num = {}
		self.letter_count = {}
		self.letter_freq_map = {}
		self.init_letter_freq()
		self.init_num_let_mappings()

	def add_map(self,number,letter):
		# if letter == 'b':
			# print "LETTER b: {0}".format(number)
		if self.letter_count[letter] == self.letter_freq_map[letter]:
			# print "too many mapped: {0}, {1}".format(number,letter)
			# print self.let_to_num
			raise KeyMappingException("The letter {0} has already been mapped by {1} numbers, the max number of times".format(letter,self.letter_count[letter]))
		if self.number_is_mapped(number):
			# print "number alredy mapped"
			raise KeyMappingException("The number {0} has already been mapped to letter {1}".format(number,letter))
		self.num_to_let[number] = letter
		self.let_to_num[letter].append(number)
		self.letter_count[letter] += 1

	def number_is_mapped(self,number):
		return self.num_to_let[number] is not None

	def mapping_is_correct(self,letter,number):
		return letter == self.num_to_let[number]

	def init_num_let_mappings(self):
		letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		for letter in letters:
			self.let_to_num[letter] = []
			self.letter_count[letter] = 0

		for i in range(103):
			self.num_to_let.append(None)

	def deepcopy_key(self):
		new_key = Key()
		for i in range(len(self.num_to_let)):
			if self.num_to_let[i]:
				new_key.add_map(i,self.num_to_let[i])
		return new_key

	def init_letter_freq(self):
		self.letter_freq_map["a"] = 8
		self.letter_freq_map["b"] = 1
		self.letter_freq_map["c"] = 3
		self.letter_freq_map["d"] = 4
		self.letter_freq_map["e"] = 13
		self.letter_freq_map["f"] = 2
		self.letter_freq_map["g"] = 2
		self.letter_freq_map["h"] = 6
		self.letter_freq_map["i"] = 7
		self.letter_freq_map["j"] = 1
		self.letter_freq_map["k"] = 1
		self.letter_freq_map["l"] = 4
		self.letter_freq_map["m"] = 2
		self.letter_freq_map["n"] = 7
		self.letter_freq_map["o"] = 8
		self.letter_freq_map["p"] = 2
		self.letter_freq_map["q"] = 1
		self.letter_freq_map["r"] = 6
		self.letter_freq_map["s"] = 6
		self.letter_freq_map["t"] = 9
		self.letter_freq_map["u"] = 3
		self.letter_freq_map["v"] = 1
		self.letter_freq_map["w"] = 2
		self.letter_freq_map["x"] = 1
		self.letter_freq_map["y"] = 2
		self.letter_freq_map["z"] = 1

class KeyMappingException(Exception):
	pass

def main():
	# ct = raw_input(">>> Enter the ciphertext: ")
	# ds = DecryptionScheme("98,23,5,23 34,23,56,34 34,11,23")
	ds = DecryptionScheme("78,11,65,60,11,26,12 69,61,93,11,37 8,63,31,6,74,91 48,42,31,33,92,82 9,63,4,78,86,2,48 69,37,42,48,39,69 58,65,55,18,99,69,50,61,78,40,96,21 80,37,72,45,50,48,22,76 63,95,85,78,89,76,39,69,69,45,55,31 93,54,14,17,74,8,42,12,14,41,58,31 55,42,31,33,92,82,33,40,76,84,80 10,63,48,50,100 28,12,41,86,63,72,42,0,50,41,102,24,74 88,72,19,52,8,50,27,72 95,54,72,24,82,40,80,91,4,56,88 72,16,82,44,54,82 6,60,88,33,74,0,99 69,67,48,100,69,93,80 76,17,80,21,2,74,10,33 69,4,72,0,69,28,86,82 31,74,6,87,95,43,84,61,94,78 11,61,72,21,82,69,63,54,14,20,60,87 69,100,72,65,52,23,92,27,72 8,76,22,96,26,90,17,14 69,80,100,9,35,63,54,22,94,72,65,82,44,80 82,9,61,94,87,44,54,31,80 6,48,52,44,31,35,91,45,50,100 22,54,14,61,80,10,67,69,25,78 11,100,2,57,67,78,41,82 47,0,100,4,47,16,72 35,6,47,26 97,41,48,50,40,6,52 8,48,94,60,89,26,14 39,56,9,67,52,69,74,18,78,80,45,8,42,50,39,89,100 50,4,10,18,74 10,93,52,71,93,6,88 2,58,45,48,42,59,22 0,31,45,50,19,59,23,82,78 2,10,6,12,24,52,28 61,8,80,88,0,11,48,18 89,63,65,86,37,69,45,10,47 59,65,56,12,45,78,92,76,39,8,94,84,40,65,59 74,18,8,95,47,26,80 10,61,58,10,25,74,91,39,102,22,78 40,57,12,95,82,84,74,40,4,50,39,78,89 69,48,17,59,39,69,63,87,16,57,84,39,6,72,100 82,97,0,31,52,27,60 47,20,96,39,50,82 14,74,21,12,31,27 63,80,91,22,59,82,41,8,50,21 6,91,2,96,43,78,92,42,9")
	# ds = DecryptionScheme("12,41,82,22,80,85,4,8,48,43,80,52,27,59,85,6,74,45,4,57,44,78,52")
	# ds = DecryptionScheme("9,63,94,60,92,26,72,11,48,2,80,82,42,29,39,9,0,91,40,67,59,78 0,56,88,45,12,42,78,17,82,84,4,8,48,44,82,33,52,24,55,86,0,72,41,6,60,40,82,52 12,41,82,22,80,85,4,8,48,43,80,52,27,59,85,6,74,45,4,57,44,78,52")
	# ds = DecryptionScheme("58,65,55,18,99,69,50,61,78,40,96,21")
	plain = ds.decrypt()
	print plain
	ds.print_key()
	# sk = Key()
	# nk = copy.deepcopy(sk)
	# nk.add_map(12,'a')
	# import IPython; IPython.embed()

if __name__ == "__main__":
	main()