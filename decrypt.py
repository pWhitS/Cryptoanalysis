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


	def decryptSingleWord(self, lword):
		ptext = ""
		nums = lword.split(",")

		for n in nums:
			ptext += self.key.decrypt_number(int(n))

		return ptext


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
		else:
			for word in self.possible_guesses:
				try:
					for i in range(len(self.cipherword)):
						if not self.key.number_is_mapped(self.cipherword[i]):
							self.key.add_map(self.cipherword[i],word[i])
					self.plainword = word
					if (self.cipherword_number) < (len(self.master.sorted_ciphertext) - 1):
						self.next = Word(self.master.sorted_ciphertext[self.cipherword_number+1],self.cipherword_number+1,self.key,self,self.master)
						self.next.decrypt()
				except KeyMappingException as e:
					self.plainword = None
					self.next = None
					self.key = copy.deepcopy(self.source_key)
					continue
				else:
					break				
			if self.plainword == None:
				raise KeyMappingException("All possible plainwords for cipherword {0} have been tried".format(str(self.cipherword)))

	def filter(self):
		sublist = self.master.english_words_by_length[len(self.cipherword)]
		self.possible_guesses = []
		for word in sublist:
			good_word = True
			for i in range(len(self.cipherword)):
				if word[i] == "'":
					good_word = False
					break
				if self.key.number_is_mapped(self.cipherword[i]):
					if not self.key.mapping_is_correct(word[i],self.cipherword[i]):
						good_word = False
						break
			if good_word:
				self.possible_guesses.append(word)

class Key:

	def __init__(self):
		self.num_to_let = []
		self.let_to_num = {}
		self.letter_count = {}
		self.letter_freq_map = {}
		self.init_letter_freq()
		self.init_num_let_mappings()

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


class InitialAnalysis:

	def __init__(self, ctext):
		self.key = Key()
		self.plaintext = ""
		self.ciphertext = ctext

		p1 = "sconced pouch bogart lights coastal philip nonexplosive shriller outstripping underbidding nightshirts colly editorializer trembler unresistant resins anthrax polypus research parapets gratuitous corespondent pyrometer breveted psychoneurosis scoutings almightily endoscopes cyanosis kayaker hake william blunted incompressibility lacer cumquat aniline agileness academe obstacle toothpick nondistribution rebukes concertizes industrialist plenipotentiary swagmen kevils dredge ostensible atavistic p"
		p2 = "revelation revering rightest impersonalize juliennes scientists reemphasizing propose crony bald pampering discharged lincoln authoresses interacted laked bedmaker intolerably beltlines warningly worldliness serologic bottom guessed hangup vitiates snaky polypous manifolding sweatshirt divisiveness decapitation musketry versers pizzas aperies reorganizes fender presentations thereuntil fly entrapped causewayed shaped freemasonry nudging efflorescence hydrated zazen exegeses fracas unprogressivel"
		p3 = "boca ingestion financed indexer generalships boldfaces boughed tesla videotext expiation brasil kinglets duality rattlesnakes mailability valvelet whimperingly corralled stench fatal inapplicably uncourageous bubblers req jesse foetor bulgaria hueless pickwicks intrans gargles purgations subvarieties pettier caste decongestive replanned continual bribed pirog learning currier careers rustling swankily onetime prearranges stowage responder inwrapped coign concubines gyrus delta tripled sleetier m"
		p4 = "allocated demonstration cocoanuts imprecisions mikado skewer ennobled cathect universalizes lucidity soldierly calor narthexes jiggling mutinousness relight mistook electra ogles chirk unsympathetic indorsed theomania gaper moths aerospace riboflavin sensorium teariest luckiest dither subparts purslane gloam dictatory conversed confides medullary fatsos barked yank chained changes magicians movables ravenousness dipsomaniac budded windjammers stayers dixie tepidities desexualization boodled dile"
		p5 = "shellackers ballets unselfishly meditatively titaness highballed serenaders ramshorns bottlenecks clipsheet unscriptural empoisoned flocking kantians ostensibilities heigh hydrodynamics qualifier million unlading distributed crinkliest conte germ certifier weaklings nickeled watson cutis prenticed debauchery variously puccini burgess landfalls nonsecular manipulability easterlies encirclements nescient imperceptive dentally sudsers reediness polemical honeybun bedrock anklebones brothering narks"


	def initAnalysis(self):
		cipherList = self.ciphertext.split(" ")
		l1 = len(self.p1.split(" ")[0])
		l2 = len(self.p2.split(" ")[0])
		l3 = len(self.p3.split(" ")[0])
		l4 = len(self.p4.split(" ")[0])
		l5 = len(self.p5.split(" ")[0])

		firstword = cipherList[0]
		fwlen = len(firstword.split(","))

		if fwlen == l1:
			self.plaintext = p1
		elif fwlen == l2:
			self.plaintext = p2
		elif fwlen == l3:
			self.plaintext = p3
		elif fwlen == l4:
			self.plaintext = p4
		elif fwlen == l5:
			self.plaintext = p5
		else: 
			return False

		return True


	def buildKeyMapping(self):
		pass



def removeLastWord(ctext):
	clist = ctext.split(" ")
	lword = clist[len(clist)-1]
	clist = clist[:-1]
	return " ".join(clist), lword


def main():
	ciphertext = raw_input(">> Enter the ciphertext: ")


	ciphertext, lastword = removeLastWord(ciphertext)
	print "\n" + ciphertext + "\n" + lastword

	ds = DecryptionScheme(ciphertext)
	plaintext = ds.decrypt()
	lword =  ds.decryptLastWord(lastword)

	print "\nMy plaintext guess is: "
	print plaintext, lword
	# ds.print_key()

if __name__ == "__main__":
	main()
