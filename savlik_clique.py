words = []  # list of tuples: (word, charset, neighbours)
words_that_contain_letter = {}

print('--- reading words file ---')
# words_alpha.txt from https://github.com/dwyl/english-words
with open('words_alpha.txt') as f:
	for word in f:
		word = word[:-1]
		if len(word) != 5:
			continue
		char_set = set(word)
		if len(char_set) != 5:
			continue
		words.append((word, char_set, set()))

# add single characters as valid words
for l in "qwertyuiopasdfghjklzxcvbnm":
	words.append((l, set([l]), set()))
	words_that_contain_letter[l] = set()

print('--- building neighborhoods ---')
for i in range(len(words)):
	for j in range(len(words)):
		if j >= i:
			break
		if len(words[i][1] & words[j][1]) == 0:
			words[i][2].add(j)
			words[j][2].add(i)

print('--- filling words_that_contain_letter ---')
# fill words_that_contain_letter
for i, word in enumerate(words):
	for l in word[0]:
		words_that_contain_letter[l].add(i)

# select order of letter by the frequency from lowest to highest
order = [k for k, v in sorted(words_that_contain_letter.items(), key=lambda x: len(x[1]))]
def first_letter_unused(set_of_letters):
	for l in order:
		if l not in set_of_letters:
			return l

print('--- start clique finding (this will not take that long ;-)) ---')
# start clique finding
results = []
def solve(word_remaining, letters_used, word_candidates, chosen_words):
	if word_remaining == 0:
		results.append(chosen_words)
		return
	# choose from candidates only words that contain the most uncommon unused letter
	for i in word_candidates & words_that_contain_letter[first_letter_unused(letters_used)]:
		word_candidates2 = word_candidates & words[i][2]
		if len(word_candidates2) < word_remaining-1:
			continue
		letters_used2 = letters_used | words[i][1]
		if len(letters_used2) % 5 >= 2:
			continue
		solve(word_remaining-1, letters_used2, word_candidates2, chosen_words+[words[i][0]])

solve(6, set(), set(range(len(words))), [])

print('completed! Found %d results' % len(results))

for c in results:
	print(c)

print('completed! Found %d results' % len(results))