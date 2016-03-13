import copy
import random
import sys

ENGLISH_WORDS_FN = "english_words.txt"
# PLAINTEXT_FN = "plaintext_dictionary.txt"

# Main class which organizes the recursive decryption process
class DecryptionScheme:

	def __init__(self,ciphertext):
		self.word_length_freq_map = {} # letter frequencies
		self.english_words_by_length = {} # word length frequencies in dictionary
		self.ciphertext = ciphertext # the ciphertext
		# list of words in ciphertext sorted by freq of words of the same length in dict
		self.sorted_ciphertext = []  # the ciphertext sorted by longest cipherwords first
		self.cipherword_positions = {} # the original positions of each ciphertext word
		self.head = None # the head of the recursive linked-list-like data structure Word
		self.key = Key() # create new blank key

		self.init_word_length_freq_map() # setup letter frequency map
		self.read_english_words() # read in the words from the English dictionary
		self.sort_ciphertext() # sort the words of the ciphertext by length (longest first)

	# decrypts ciphertext
	def decrypt(self):
		# Initialize the head of our linked-list-like decrypter
		self.head = Word(self.sorted_ciphertext[0],0,self.key,None,self)
		# start decryption
		self.head.decrypt()

		sorted_plainwords = []
		plainwords = [None for i in range(len(self.sorted_ciphertext))]

		# cycle through the linked Word instances to get each plaintext word
		curr = self.head
		while (curr != None):
			# this exception should not be raised; it was more for testing purposes
			if curr.plainword is None:
				raise Exception("A cipherword was not mapped. Our mapping failed :(")
			else:
				sorted_plainwords.append(curr.plainword)
			if curr.next == None:
				self.key = curr.key
			curr = curr.next

		# another exception that should only have been raised during testing
		if len(sorted_plainwords) < len(self.sorted_ciphertext):
			raise Exception("Enough words were not decrypted. Our mapping failed :(")

		# the plaintext words are currently sorted by length; we use cipherword_positions to put them back in the correct order
		for i in range(len(self.sorted_ciphertext)):
			cipherword = self.sorted_ciphertext[i]
			plainword = sorted_plainwords[i]
			plainwords[self.cipherword_positions[str(cipherword)].pop()] = plainword

		# return the plaintext
		return " ".join(plainwords)

	def decryptSingleWord(self, lword):
		ptext = ""
		nums = lword.split(",")

		for n in nums:
			ptext += self.key.decrypt_number(int(n))

		return ptext

	# a function mainly used during debugging; just prints the letter-to-number mapping of the key
	def print_key(self):
		print "Letter to Num:"
		print self.key.let_to_num
		print "Num to LEtter:"
		print self.key.num_to_let

	# sets up the dictionary for the frequencies of each word of a given length in english_words.txt
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

	# reads in the words from english_words.txt and places them into a dictionary mapping length to a list of corresponding words
	def read_english_words(self):
		fileobj = open(ENGLISH_WORDS_FN, "r")
		for line in fileobj:
			word = line.strip()
			len_word = len(word)
			if len_word not in self.english_words_by_length:
				self.english_words_by_length[len_word] = []
			self.english_words_by_length[len_word].append(word)
		fileobj.close()

	# sorts the ciphertext words by length (longest first)
	def sort_ciphertext(self):
		cipher_words = self.ciphertext.split(" ")
		cipher_words = [word.split(",") for word in cipher_words]
		for word in cipher_words:
			for i in range(len(word)):
				word[i] = int(word[i])
		i = 0
		for cipherword in cipher_words:
			if str(cipherword) not in self.cipherword_positions:
				self.cipherword_positions[str(cipherword)] = []
			self.cipherword_positions[str(cipherword)].append(i)
			i += 1
		self.sorted_ciphertext = sorted(cipher_words, key=lambda word: len(word), reverse=True)

# this is the recursive class used in our decryption strategy; it utilizes linked-list style structure;
# each instance decrypts a single ciphertext word and then creates the next Word instance to decrypt the
# next ciphertext word in a recursive manner
class Word:

	def __init__(self,cipherword,cipherword_number,key,prev,master):
		self.cipherword = cipherword # the ciphertext word
		self.cipherword_number = cipherword_number # the ciphertext word's index in DecryptionScheme.sorted_ciphertext
		self.source_key = key # a copy by reference to the given key
		self.key = copy.deepcopy(key) # a copy by value to the original key
		self.prev = prev # a reference to the previous Word instance; None if this is the head
		self.master = master # a reference to the DecryptionScheme instance
		self.next = None # a reference to the next Word instance; None if this is the tail
		self.plainword = None # the decrypted plaintext word
		self.possible_guesses = None # the list of possible guesses for the given key and ciphertext word

	# decrypts cipherword and sets up the next Word for decryption
	def decrypt(self):
		# filter the list of possible guesses
		self.filter()

		# MESSAGE_SET = False

		# if there are no possible guesses, raise our custom exception (which would be caught by the caller)
		if len(self.possible_guesses) == 0:
			raise KeyMappingException("Current mapping allows for no possible guess")
		else:
			# guess_num = 0

			# cycle over the possible guesses determined by filter()
			for word in self.possible_guesses:
				# guess_num += 1

				# we use a try-catch to catch any instances of our custom exception, which might be thrown by
				# key.add_map() or next.decrypt()
				try:
					# if the number hasn't already been mapped, add it to our key (note that words with conflicting mappings were
				    # already taken care of by filter())
					for i in range(len(self.cipherword)):
						if not self.key.number_is_mapped(self.cipherword[i]):
							self.key.add_map(self.cipherword[i],word[i])
					self.plainword = word

					# if self.cipherword_number == 0:
						# print ""
					# message = "WORD #{0} - {1}/{2}: {3} <---> ".format(self.cipherword_number, guess_num,len(self.possible_guesses), word)
					# MESSAGE_SET = True
					# sys.stdout.write(message)

					# if we aren't on the last ciphertext word, setup and decrypt the next ciphertext word
					if (self.cipherword_number) < (len(self.master.sorted_ciphertext) - 1):
						self.next = Word(self.master.sorted_ciphertext[self.cipherword_number+1],self.cipherword_number+1,self.key,self,self.master)
						self.next.decrypt()
				# raised whenever a conflict in the key mapping is found; we fail gracefully and guess the next word
				except KeyMappingException as e:
					# if MESSAGE_SET:
						# sys.stdout.write("\b" * (len(message)))
					# MESSAGE_SET = False

					# if a conflict was found with the last guess, remove the plainword setting (if any), the reference to next (if any)
					# and revert the key to the key given when this instance was created (this is why we have source_key and key, to
				    # allow us to easily undo mappings than turn out to be wrong)
					self.plainword = None
					self.next = None
					self.key = copy.deepcopy(self.source_key)
					continue
				# if no exception was raised, we've found a legitimate potential decryption
				else:
					break		
			if self.plainword == None:
				raise KeyMappingException("All possible plainwords for cipherword {0} have been tried".format(str(self.cipherword)))

	# filters the list of possible guesses for the given cipherword based on words of the same length in english_words.txt
	def filter(self):
		# get all words of matching length
		sublist = self.master.english_words_by_length[len(self.cipherword)]
		# sort the words by their "scoreWord" value; see scoreWord() below for details
		sublist = sorted(sublist, key=lambda word: scoreWord(word,self.key.letter_freq_map), reverse=True)
		self.possible_guesses = []
		for word in sublist:
			good_word = True
			for i in range(len(self.cipherword)):
				# we ignore the case of words with apostrophes since the case was not explained in the Project1 assignment criteria
				if word[i] == "'":
					good_word = False
					break
				# if a number is already mapped and the mapping resulting from this guess is incorrect, rule it out as a possible guess
				if self.key.number_is_mapped(self.cipherword[i]):
					if not self.key.mapping_is_correct(word[i],self.cipherword[i]):
						good_word = False
						break
			# if the word had no conflicting mappings, append it to the list of guesses
			if good_word:
				self.possible_guesses.append(word)

# a simple class to maintain the partial (possibly complete) key we develop through decryption
class Key:

	def __init__(self):
		self.num_to_let = [] # maps cipher characters (numbers) to the plaintext characters (English lower-case letters)
		self.let_to_num = {} # maps plainext character to the lit of ciphertext characters
		self.letter_count = {} # maintains a count of how many numbers have been mapped to each letter so we know when a conflict arises
		self.letter_freq_map = {} # a map of the letter frequencies
		self.init_letter_freq() # initialize the letter freq map
		self.init_num_let_mappings() # initialize the num_to_let, let_to_num and letter_count mappings

	# adds a mapping to the key between a given number and letter; raises KeyMappingException if there is a conflict
	def add_map(self,number,letter):
		if self.letter_count[letter] == self.letter_freq_map[letter]:
			raise KeyMappingException("The letter {0} has already been mapped by {1} numbers, the max number of times".format(letter,self.letter_count[letter]))
		if self.number_is_mapped(number):
			raise KeyMappingException("The number {0} has already been mapped to letter {1}".format(number,letter))
		self.num_to_let[number] = letter
		self.let_to_num[letter].append(number)
		self.letter_count[letter] += 1

	def decrypt_number(self, number):
		return self.num_to_let[int(number)]

	# returns a Boolean reflecting whether or not the number has been mapped yet
	def number_is_mapped(self,number):
		return self.num_to_let[number] is not None

	# returns a Boolean reflecting whether mapping the given letter and number results in a conflict with existing mappings
	def mapping_is_correct(self,letter,number):
		return letter == self.num_to_let[number]

	# sets up the mappings for num_to_let, let_to_num and letter_count def init_num_let_mappings(self):
	def init_num_let_mappings(self):
		letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		for letter in letters:
			self.let_to_num[letter] = []
			self.letter_count[letter] = 0

		for i in range(103):
			self.num_to_let.append(None)

	# setup the letter frequency map
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

# a basic extension of the Exception class that expresses our specific circumstances
class KeyMappingException(Exception):
	pass

# returns a numeric score for a given word based on the sum of the numbers they are mapped to as determined by letVals; we use
# this to return sums of the frequencies for all letters in a given word, which we use to determine the order of our guesses
def scoreWord(word, letVals):
    score = 0
    for letter in word:
        if letter not in letVals:
            pass
        else:
            score += letVals[letter]
    return score

def removeLastWord(ctext):
	clist = ctext.split(" ")
	lword = clist[len(clist)-1]
	clist = clist[:-1]
	return " ".join(clist), lword

# execute the script
def main():
	ciphertext = raw_input(">> Enter the ciphertext: ")
	ciphertext, lastword = removeLastWord(ciphertext)

	ds = DecryptionScheme(ciphertext)
	plaintext = ds.decrypt()
	lword =  ds.decryptSingleWord(lastword)

	print "\nMy plaintext guess is: "
	print plaintext, lword

if __name__ == "__main__":
	main()
