# Cryptoanalysis
Applied Cryptography Project

## Who worked on this project?

Patrick Whitsell (pdw236@nyu.edu) <br>
Casey McGinely (cmm771@nyu.edu) <br>
Fernando Maymi (fernando.maymi@nyu.edu) <br>

## Objective
1. Given a set of known plaintexts and a ciphertext, can we determine which plaintext was encrypted? (known plaintext attack) <br>
2. Given a set of random ciphertexts, can we reliably decrypt to the plaintext? (known ciphertext attack) <br>

The encryption algorithm for both tasks is known beforehand. Can we find a suffiecient vulnerability in the scheme, such that we can decrypt ciphertexts on demand? <br>

## Known Plaintext Attack
+ Ciphertexts are 500 characters each
+ Whitespace is unencrypted. Ciphertext whitespace == plaintext whitespace.
+ Sets of plaintexts are known

### Strategy
1. Compare number of words (Majority of plaintexts fail here)
2. Compare lengths of words 
3. For each known plaintext, create key mapping letter-by-letter until a contradiciton is found or the entire key mapping is complete. (Almost all plaintext are already eliminated)

### Basic Analysis
A little bit of quick statistics will show us that the most likely length (eight) consists of about 1/5 of words in the provided word list.  Assuming the plaintext is five words (L = 40, much less than the L=500 in the actual problem) we find that we have a 1/3125 chance of getting a plaintext that consists of five eight-letter words.  (It is important to note that this is the most likely result since eight-letter words are independently the most likely word length and the plaintext is randomly selected.)  This means that the chance of any random, five word ciphertext matching an unrelated plaintext in word length pattern is no more than 0.032%. This means very few ciphertexts will progress to the attempted key mapping stage. This makes the approach very efficient, since it quickly eliminates possible plaintexts with use of only integer comparisons and counting. Furthermore, the longer the ciphertext the larger the plaintext space needs to be to render this approach insufficient on its own. <br>

In general with this strategy, plaintexts with larger lengths is an easier problem than shorter plaintext lengths because of the lower probability of progressing to the key mapping stage. Likewise, a smaller set of plaintexts is an easier task than larger plaintext sets because less plaintexts will progress to the key mapping stage.<br>      

## Known Ciphertext Attack
+ Ciphertexts are 500 characters each
+ Whitespace is unencrypted. Ciphertext whitespace == plaintext whitespace.
+ Sets of plaintexts are unknown

### Strategy
+ Depth first search of an undirected acyclic graph, continuously pruned into a linked list as the search progresses.
+ Dictionary of english words sorted int 'buckets' by length. Word 'buckets' sorted by agrigate letter frequency
+ Longest words are guessed first. In general, fewer longer words are in the dictionary. Also longer words fill up more key mappings, reducing the next guess space more quickly. 

### Basic Analysis
A resonable decryption speed was acheived most of the time. Problem arose if there were no 'long' words to guess first. The longest word, which was actually fairly short, would be guessed first, fill in small key mapping, and would take a very long time to brute force the word space. <br>

Another issue was that the program would mistakenly decrypt very short words. This was happening because the key mapping coincidentally would not create a contradiction before the whole plaintext was guessed. Example: 'red' was guessed instead of 'req'. In this example our letter frequency sorting strategy was working against us. <br>

Despite a few problems, this strategy was very successful. In testing our program was able decrypted 94.5% of the ciphertexts' letters correctly.


