words = []  # list of tuples: (word, bitmap, neighbours)
words_that_contain_letter = {}
letters_frequency = {}
alphabet = "qwertyuiopasdfghjklzxcvbnm"

def get_bitmap(word):
	res = 0
	for l in word:
		res |= 1 << (ord(l)-ord("a"))
	return res

print('--- reading words file ---')
# words_alpha.txt from https://github.com/dwyl/english-words
anagrams = set()
with open('words_alpha.txt') as f:
	for word in f:
		word = word[:-1]
		if len(word) != 5:
			continue
		char_set = frozenset(word)
		if len(char_set) != 5:
			continue
		bitset = get_bitmap(word)
		if bitset in anagrams:
			continue
		anagrams.add(bitset)
		words.append((word, bitset, set()))


print('--- building neighborhoods ---')
for i in range(len(words)):
	for j in range(len(words)):
		if j >= i:
			break
		if words[i][1] & words[j][1] == 0:
			words[i][2].add(j)
			words[j][2].add(i)

print('--- filling words_that_contain_letter ---')
# fill words_that_contain_letter
for l in alphabet:
	words_that_contain_letter[l] = set()
	letters_frequency[l] = 0

for word in words:
	for l in word[0]:
		letters_frequency[l] += 1

# select order of letter by the frequency from lowest to highest
order = [k for k, v in sorted(letters_frequency.items(), key=lambda x: x[1])]
letter_index = {l: i for i, l in enumerate(order)}
for i, word in enumerate(words):
	min_letter = order[min(letter_index[l] for l in word[0])]
	words_that_contain_letter[min_letter].add(i)

def first_letter_unused(bitmap_of_letters):
	for l in order:
		if (1 << (ord(l)-ord("a"))) & bitmap_of_letters == 0:
			return l

print('--- start clique finding (this will not take that long ;-)) ---')
# start clique finding
results = []
def solve(word_remaining, letters_used, word_candidates, chosen_words, used_one_letter_word):
	if word_remaining == 0:
		results.append(chosen_words)
		return
	# choose from candidates only words that contain the most uncommon unused letter
	for i in word_candidates & words_that_contain_letter[first_letter_unused(letters_used)]:
		word_candidates2 = word_candidates & words[i][2]
		if len(word_candidates2) < word_remaining-1:
			continue
		letters_used2 = letters_used | words[i][1]
		solve(word_remaining-1, letters_used2, word_candidates2, chosen_words+[words[i][0]], used_one_letter_word)
	if not used_one_letter_word:
		letter = first_letter_unused(letters_used)
		letters_used2 = letters_used | (1<<(ord(letter)-ord("a")))
		for i in word_candidates & words_that_contain_letter[first_letter_unused(letters_used2)]:
			word_candidates2 = word_candidates & words[i][2]
			if len(word_candidates2) < word_remaining-1:
				continue
			letters_used3 = letters_used2 | words[i][1]
			solve(word_remaining-1, letters_used3, word_candidates2, chosen_words+[words[i][0]], True)

solve(5, 0, set(range(len(words))), [], False)

print('completed! Found %d results' % len(results))

for c in results:
	print(c)

print('completed! Found %d results' % len(results))