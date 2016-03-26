f = open("english_words.txt")
count = [0]
for line in f:
	word = line.strip()
	len_word = len(word)
	if len_word > (len(count) - 1):
		for i in range(len(count), len_word+1):
			count.append(0)
	count[len_word] += 1
f.close()

l = []
print "Word length count:\n"
for i in range(1,len(count)):
	print "{0}: {1}".format(i,count[i])
	l.append((i,count[i]))

print "\n"
sort_l = sorted(l,key=lambda pair: pair[1])
print "Sorted word lengths (low to high): \n"
for length,num in sort_l:
	print "{0}: {1}".format(length,num)