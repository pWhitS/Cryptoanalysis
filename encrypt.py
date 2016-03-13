key = {}
key["a"] = [0,1,2,3,4,5,6,7]
key["b"] = [8]
key["c"] = [9,10,11]
key["d"] = [12,13,14,15]
key["e"] = [16,17,18,19,20,21,22,23,24,25,26,27,28]
key["f"] = [29,30]
key["g"] = [31,32]
key["h"] = [33,34,35,36,37,38]
key["i"] = [39,40,41,42,43,44,45]
key["j"] = [46]
key["k"] = [47]
key["l"] = [48,49,50,51]
key["m"] = [52,53]
key["n"] = [54,55,56,57,58,59,60]
key["o"] = [61,62,63,64,65,66,67,68]
key["p"] = [69,70]
key["q"] = [71]
key["r"] = [72,73,74,75,76,77]
key["s"] = [78,79,80,81,82,83]
key["t"] = [84,85,86,87,88,89,90,91,92]
key["u"] = [93,94,95]
key["v"] = [96]
key["w"] = [97,98]
key["x"] = [99]
key["y"] = [100,101]
key["z"] = [102]

f = open("english_words.txt")
maxlen = 0
maxword = None
for line in f:
	word = line.strip()
	len_word = len(word)
	if len_word > maxlen:
		maxword = word
		maxlen = len_word
f.close()

ct = ""
print maxword
i = 0
for char in maxword:
	ct += str(key[char][i % len(key[char])]) + ","
	i += 2
# ct.strip(",")
print ct[:len(ct)-1]