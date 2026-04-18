from urllib.request import urlopen
from collections import defaultdict
from time import time
import pickle


# Inputs
data_source = input('\nImport: ')
max_len = int(input('Max chain length: '))

weights = []
for i in range(max_len):
    weights.append(int(input('\tWeight {0}: '.format(i+1))))
    if weights[i] <= 0:
        weights[i] = 0.1
    
#soft_max = int(input('Character curb: '))
soft_max = 10

if(input('Line delimited (y/n): ').casefold() == 'n'):
    lined = False
else:
    lined = True


# Fetch and process the corpus data
print("\nProcessing...")
start_time = time()

if(data_source.startswith('http://') or data_source.startswith('https://')):
    text = urlopen(data_source)
    data_is_url = True
else:
    data_source = 'data/{0}.txt'.format(data_source)
    text = open(data_source, encoding='utf-8', errors='replace')
    data_is_url = False


# Processes the data line-by-line
corpus = []
line_count = 0

for line in text:
    if(data_is_url):
        line = line.decode('utf-8')
    line = line.replace('\r', ' ').replace('\n', ' ')
    
    if not line.strip():                                # Skips empty lines
        continue
    
    line = [w for w in line.split() if w.strip()]       # Removes whitespace
    
    if lined:
        line = ['Line::'] + line                        # Adds sentinel (lined)
    
    else:
        if line[len(line) - 1].endswith(('.', '!', '?')):
            line = line + ['Line::']                    # Adds sentinel (nonlined)
            
    corpus.extend(line)
    line_count += 1


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
with open('dataset.pkl', 'wb') as f:
    pickle.dump([bundle, weights, soft_max, lined], f)


# Display
print("Done!\n")

print('{0} ms'.format(round((time() - start_time) * 1000)))
print('Lines: {0}'.format(line_count))
print('Corpus: {0}'.format(len(corpus)))
print()