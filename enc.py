
gCIPHER_MIN = 0
gCIPHER_MAX = 102


class CEncryptionScheme:
	
	def __init__(self):
		self.freqMap = {}
		self.key = {}
		self.key_n2l = {}

		self.initFrequencies()
		self.initKey()


	def initFrequencies(self):
		self.freqMap["a"] = 8
		self.freqMap["b"] = 1
		self.freqMap["c"] = 3
		self.freqMap["d"] = 4
		self.freqMap["e"] = 13
		self.freqMap["f"] = 2
		self.freqMap["g"] = 2
		self.freqMap["h"] = 6
		self.freqMap["i"] = 7
		self.freqMap["j"] = 1
		self.freqMap["k"] = 1
		self.freqMap["l"] = 4
		self.freqMap["m"] = 2
		self.freqMap["n"] = 7
		self.freqMap["o"] = 8
		self.freqMap["p"] = 2
		self.freqMap["q"] = 1
		self.freqMap["r"] = 6
		self.freqMap["s"] = 6
		self.freqMap["t"] = 9
		self.freqMap["u"] = 3
		self.freqMap["v"] = 1
		self.freqMap["w"] = 2
		self.freqMap["x"] = 1
		self.freqMap["y"] = 2
		self.freqMap["z"] = 1


	def initKey(self):
		for k in self.freqMap:
			kc = []
			self.key[k] = kc

		for i in range(gCIPHER_MIN, gCIPHER_MAX):
			self.key_n2l[i] = ""

	
	def printKey(self, type=0):
		for kp in self.key:
			print kp, ":", self.key[kp]

		print 
		for kp in self.key_n2l:
			print kp, ":", self.key_n2l[kp]


	def setCipher(self, letter, num):
		if len(self.key[letter]) == self.freqMap[letter]:
			print "Error: cipher size exceeded!"
			return

		self.key[letter].append(num)
		self.key_n2l[num] = letter


	def isKeyKnown(self):
		for kp in self.key_n2l:
			if self.key_n2l[kp] == "":
				return False
		return True


	def clearKey(self):
		for kp in self.key:
			self.key[kp] = []

		for kp in self.key_n2l:
			self.key_n2l[kp] = ""


	def decrypt(self, ctext):
		#Ciphertext Ex: 33,45,65 56,32,55,77 54,34
		cwords = ctext.split(" ")
		cletters = []
		ptext = ""

		for cw in cwords:
			clbuf = cw.split(",")
			for clt in clbuf:
				cletters.append(clt)
			cletters.append(" ")

		for cl in cletters:
			if cl == " ":
				ptext = ptext[:-1] + " "
			elif self.key_n2l[int(cl)] == "":
				ptext += cl + ","
			else:
				ptext += self.key_n2l[int(cl)] + ","

		return ptext



		

ces = CEncryptionScheme()
ces.setCipher("a", 33)
ces.setCipher("a", 56)

print ces.decrypt("33,45,65 56,32,55,77 54,34")

print ces.isKeyKnown()
ces.clearKey()




