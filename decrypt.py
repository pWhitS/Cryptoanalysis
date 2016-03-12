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
		self.head = None
		self.key = None

		self.init_word_length_freq_map()
		self.read_english_words()
		self.sort_ciphertext()

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
		self.sort_ciphertext = sorted(cipher_words, key=lambda word: self.word_length_freq_map[len(word)])

	def print_sorted_ciphertext(self):
		print self.sort_ciphertext

class Word:

	def __init__(self,cipherword,cipherwords_map,key,prev,master):
		self.cipherword = cipherword
		self.word_map = copy.deepcopy(cipherwords_map)
		self.key = copy.deepcopy(key)
		self.prev = prev
		self.master = master
		self.next = None
		self.plainword = None
		self.possible_guesses = None

	def filter(self):
		sublist = self.master.english_words_by_length[len(self.cipherword)]


	# def decrypt_word(self):

class Key:
	num_to_let = None
	let_to_num = None
	letter_count = None
	letter_freq_map = None

	def __init__(self):
		self.init_letter_freq()

	def add_map(self,number,letter):
		if self.letter_count[letter] == self.letter_freq_map[letter]:
			raise KeyMappingException("{0} has already been mapped by {1} numbers, the max number of times".format(letter,self.letter_count[letter]))

		num_to_let[number] = letter
		let_to_num[letter].append(number)

	def letter_mapped(self,letter):
		pass

	def is_number_mapped(self,number):
		return num_to_let[number] is None


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
	ds = DecryptionScheme("98,23,5,23 34,23,56,34 34,11,23")
	ds.print_sorted_ciphertext()

if __name__ == "__main__":
	main()