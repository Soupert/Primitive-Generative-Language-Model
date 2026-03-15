from urllib.request import urlopen
from collections import defaultdict
from time import time
import pickle


url = 'https://raw.githubusercontent.com/ryanmcdermott/trump-speeches/master/speeches.txt'
max_len = 3

print("Processing...")
start_time = time()

# Fetch and process the corpus data
text = urlopen(url)
corpus = []
lines = 0

# Processes the data line-by-line
for line in text:
    line = line.decode('utf-8').replace('\r', ' ').replace('\n', ' ')
    
    if not line.strip():                                          # Skips empty lines
        continue
    
    line = ['Line::'] + [w for w in line.split() if w.strip()]    # Adds sentinel, removes whitespace
    corpus.extend(line)
    lines += 1

# Build the chain(s)
bundle = []

for memory in range(1, max_len + 1):        # Creates chains of every length up to the cap
    chain = defaultdict(list)
    
    for i in range(len(corpus) - memory):
        key = tuple(corpus[i:i + memory])
        word = corpus[i + memory].strip()
        if word:
            chain[key].append(word)

    bundle.append(chain)
    
# Save bundle
with open('bundle.pkl', 'wb') as file:
    pickle.dump(bundle, file)

# Header
print("Done!\n")

print('{0} ms'.format(round((time() - start_time) * 1000)))
print('Lines: {0}'.format(lines))
print('Corpus: {0}'.format(len(corpus)))