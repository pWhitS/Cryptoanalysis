# Author: Fernando Maymi, Patrick Whitsell, Casey McGinley
# Class: CS-GY 6903 Applied Cryptography
# Instructor: Prof. Giovanni Di Crescenzo 
# Project 1: Permutation Cipher Decryption

import copy
import argparse
import sys

ENGLISH_WORDS_FN = "english_words.txt"
VERBOSE = False
# PLAINTEXT_FN = "plaintext_dictionary.txt"

# Main class which organizes the recursive decryption process
class DecryptionScheme:

	def __init__(self,ciphertext):
		self.english_words_by_length = {} # word length frequencies in dictionary
		self.ciphertext = ciphertext # the ciphertext
		# list of words in ciphertext sorted by freq of words of the same length in dict
		self.sorted_ciphertext = []  # the ciphertext sorted by longest cipherwords first
		self.cipherword_positions = {} # the original positions of each ciphertext word
		self.head = None # the head of the recursive linked-list-like data structure Word
		self.key = Key() # create new blank key

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

	# decrypts a single word based on the key
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

		if VERBOSE:
			MESSAGE_SET = False

		# if there are no possible guesses, raise our custom exception (which would be caught by the caller)
		if len(self.possible_guesses) == 0:
			raise KeyMappingException("Current mapping allows for no possible guess")
		else:
			if VERBOSE:
				guess_num = 0

			# cycle over the possible guesses determined by filter()
			for word in self.possible_guesses:
				if VERBOSE:
					guess_num += 1

				# we use a try-catch to catch any instances of our custom exception, which might be thrown by
				# key.add_map() or next.decrypt()
				try:
					# if the number hasn't already been mapped, add it to our key (note that words with conflicting mappings were
				    # already taken care of by filter())
					for i in range(len(self.cipherword)):
						if not self.key.number_is_mapped(self.cipherword[i]):
							self.key.add_map(self.cipherword[i],word[i])
					self.plainword = word

					if VERBOSE:
						if self.cipherword_number == 0:
							print ""
						message = "WORD #{0} - {1}/{2}: {3} <---> ".format(self.cipherword_number, guess_num,len(self.possible_guesses), word)
						MESSAGE_SET = True
						sys.stdout.write(message)

					# if we aren't on the last ciphertext word, setup and decrypt the next ciphertext word
					if (self.cipherword_number) < (len(self.master.sorted_ciphertext) - 1):
						self.next = Word(self.master.sorted_ciphertext[self.cipherword_number+1],self.cipherword_number+1,self.key,self,self.master)
						self.next.decrypt()
				# raised whenever a conflict in the key mapping is found; we fail gracefully and guess the next word
				except KeyMappingException as e:
					if VERBOSE:
						if MESSAGE_SET:
							sys.stdout.write("\b" * (len(message)))
						MESSAGE_SET = False

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
		sublist = sorted(sublist, key=lambda word: self.scoreWord(word,self.key.letter_freq_map), reverse=True)
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

	# returns a numeric score for a given word based on the sum of the numbers they are mapped to as determined by letVals; we use
	# this to return sums of the frequencies for all letters in a given word, which we use to determine the order of our guesses
	def scoreWord(self, word, letVals):
	    score = 0
	    for letter in word:
	    	if letter == "'":
	    		continue
	    	score += letVals[letter]
	    return score

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

	# decrypts a single number based on the key; if the number hasn't been mapped yet, we find the first "mappable" letter and map it
	def decrypt_number(self, number):
		if self.number_is_mapped(number):
			return self.num_to_let[int(number)]
		else:
			for letter in self.let_to_num:
				if self.letter_count[letter] < self.letter_freq_map[letter]:
					self.add_map(number,letter)
					return letter

	# returns a Boolean reflecting whether or not the number has been mapped yet
	def number_is_mapped(self,number):
		return self.num_to_let[int(number)] is not None

	# returns a Boolean reflecting whether mapping the given letter and number results in a conflict with existing mappings
	def mapping_is_correct(self,letter,number):
		return letter == self.num_to_let[int(number)]

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

# used to perform our fast and highly specific anlysis for Part 1 base don the 5 known plaintexts
class InitialAnalysis:

	def __init__(self, ctext):
		self.key = Key()
		self.plaintext = ""
		self.ciphertext = ctext

		self.p1 = "sconced pouch bogart lights coastal philip nonexplosive shriller outstripping underbidding nightshirts colly editorializer trembler unresistant resins anthrax polypus research parapets gratuitous corespondent pyrometer breveted psychoneurosis scoutings almightily endoscopes cyanosis kayaker hake william blunted incompressibility lacer cumquat aniline agileness academe obstacle toothpick nondistribution rebukes concertizes industrialist plenipotentiary swagmen kevils dredge ostensible atavistic p"
		self.p2 = "revelation revering rightest impersonalize juliennes scientists reemphasizing propose crony bald pampering discharged lincoln authoresses interacted laked bedmaker intolerably beltlines warningly worldliness serologic bottom guessed hangup vitiates snaky polypous manifolding sweatshirt divisiveness decapitation musketry versers pizzas aperies reorganizes fender presentations thereuntil fly entrapped causewayed shaped freemasonry nudging efflorescence hydrated zazen exegeses fracas unprogressivel"
		self.p3 = "boca ingestion financed indexer generalships boldfaces boughed tesla videotext expiation brasil kinglets duality rattlesnakes mailability valvelet whimperingly corralled stench fatal inapplicably uncourageous bubblers req jesse foetor bulgaria hueless pickwicks intrans gargles purgations subvarieties pettier caste decongestive replanned continual bribed pirog learning currier careers rustling swankily onetime prearranges stowage responder inwrapped coign concubines gyrus delta tripled sleetier m"
		self.p4 = "allocated demonstration cocoanuts imprecisions mikado skewer ennobled cathect universalizes lucidity soldierly calor narthexes jiggling mutinousness relight mistook electra ogles chirk unsympathetic indorsed theomania gaper moths aerospace riboflavin sensorium teariest luckiest dither subparts purslane gloam dictatory conversed confides medullary fatsos barked yank chained changes magicians movables ravenousness dipsomaniac budded windjammers stayers dixie tepidities desexualization boodled dile"
		self.p5 = "shellackers ballets unselfishly meditatively titaness highballed serenaders ramshorns bottlenecks clipsheet unscriptural empoisoned flocking kantians ostensibilities heigh hydrodynamics qualifier million unlading distributed crinkliest conte germ certifier weaklings nickeled watson cutis prenticed debauchery variously puccini burgess landfalls nonsecular manipulability easterlies encirclements nescient imperceptive dentally sudsers reediness polemical honeybun bedrock anklebones brothering narks"
		self.plist = [self.p1, self.p2, self.p3, self.p4, self.p5]

	#compares number of words in the ciphertext to the plaintexts
	#removes plaintexts from the plist list if it doesn't match 
	def compareNumWords(self):
		num_cipher_words = len(self.ciphertext.split(" "))
		i = 0
		bound = len(self.plist)

		while i < bound:
			if num_cipher_words != len(self.plist[i].split(" ")):
				del self.plist[i]
				bound -= 1	
				continue
			i += 1

	#compares length of words in the ciphertext to the plaintexts
	#removes plaintexts from the plist list if it doesn't match 
	def compareWordLengths(self):
		cipherList = self.ciphertext.split(" ")
		cipher_len_words_list = []

		for cword in cipherList:
			cipher_len_words_list.append(len(cword.split(",")))

		i = 0
		bound = len(self.plist)
		while i < bound:
			plain_len_words_list = []
			temp = self.plist[i].split(" ")

			for pword in temp:
				plain_len_words_list.append(len(pword))

			if plain_len_words_list != cipher_len_words_list:
				del self.plist[i]
				bound -= 1
				continue
			i += 1

	#Creates the key mapping for the chosen plaintext
	#If the mapping is 'wrong' then the initial analysis has failed
	#This method assumes only one plaintext is left
	def checkKeyMapping(self):
		plaintext = self.plist[0].replace(" ", "")
		cipherwords = self.ciphertext.split(" ")
		cipherletters = []

		for word in cipherwords:
			cipherletters += word.split(",")

		for i in range(0, len(plaintext)):
			if self.key.number_is_mapped(int(cipherletters[i])):
				continue

			try:
				self.key.add_map(int(cipherletters[i]), plaintext[i])
			except KeyMappingException, kme:
				return False

		return True


	#Performs the analysis technique of checking plaintexts against the plaintext dictionary
	#If analysis fails, moves onto the second analysis technique
	def initAnalysis(self):
		self.compareNumWords()
		if len(self.plist) == 0:
			return False

		self.compareWordLengths()
		if len(self.plist) == 0:
			return False

		#At this point its only possible for there to be one plaintext
		if self.checkKeyMapping() == False:
			return False

		return self.plist[0]

<<<<<<< HEAD
# returns the first n-1 words of the ciphertext as a list, and the last word as a separate value
=======

>>>>>>> hotfix-scoreWord
def removeLastWord(ctext):
	clist = ctext.split(" ")
	lword = clist[len(clist)-1]
	clist = clist[:-1]
	return " ".join(clist), lword

# setup the argument parser
def parse_args():
	parser = argparse.ArgumentParser(description='Decryption Script: a solution for decrypting the ciphertexts for Project 1 in CS-GY 6903 Applied Cryptography; Team: Fernando Maymi, Patrick Whitsell and Casey McGinley')
	parser.add_argument("-v", "--verbose", action="store_true", help="Outputs decryption attempts to stdout; useful for debugging")
	parser.add_argument("-s", "--supress_naive_analysis", action="store_true", help="Suppresses the use of our InitialAnalysis class entirely")
	return parser.parse_args()

# execute the script
def main():
	global VERBOSE
	use_second_analysis = False # this flag indicates that the 2nd generic analysis method should be used
	args = parse_args()
	if args.verbose:
		VERBOSE = True # this flag sets up verbose output for debugging
	if args.supress_naive_analysis:
		use_second_analysis = True # by setting this to True here, we don't even bother trying the InitialAnalysis for the highly specifc 5 
								   # plaintexts; we just skip to the generic analysis DecryptionScheme

	ciphertext = raw_input(">> Enter the ciphertext: ")

	if not use_second_analysis:
		#analysis for part 1
		ia = InitialAnalysis(ciphertext)
		plaintext = ia.initAnalysis()
		if plaintext != False:
			print "\nMy plaintext guess is: "
			print plaintext
		else:
			# if the InitialAnalysis fails, try the 2nd analysis
			use_second_analysis = True

	if use_second_analysis:
		#analysis for part 2
		ciphertext, lastword = removeLastWord(ciphertext)

		ds = DecryptionScheme(ciphertext)
		plaintext = ds.decrypt()
		lword =  ds.decryptSingleWord(lastword)

		print "\nMy plaintext guess is: "
		print plaintext, lword

if __name__ == "__main__":
	main()
