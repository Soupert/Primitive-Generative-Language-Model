from random import choice, choices
import re
import pickle


weights = [7 , 25 , 15]

# Read bundle
with open('bundle.pkl', 'rb') as file:
    bundle = pickle.load(file)

# Punctuation banks
punctuation_symbols = ('.', '!', '?')
honorifics = {
    'mr.', 'ms.', 'mrs.', 'mx.', 'dr.', 'prof.', 'capt.', 'gen.', 'gov.',
    'sen.', 'st.', 'rev.', 'hon.', 'jr.', 'sr.', 'ph.d.', 'phd.', 'm.d.',
    'b.a.', 'm.a.', 'd.d.s.'
}
other_abbreviations = {
    'etc.', 'a.m.', 'p.m.', 'vol.', 'inc.', 'co.', 'corp.', 'ltd.', 'www.'
}
repeating_symbols = {'.' : 2, ',' : 2}                              # Number is the minimum number of repetitions

# [!] Always place pairs that contain another punctuation first
homo_punc = (
    '"', '\'', '\\*', '**', '*', '`', '~~', '__'                    # Homogenous pairs have identical opens and closes
)
hetero_punc = (
    ('(<', '>)'), ('(', ')'), ('[', ']'), ('{', '}'), ('«', '»')    # Heterogenous pairs have different opens and closes
)
any_text = fr'(?<=[A-Za-z0-9{0}])[A-Za-z0-9{0}]'.format(punctuation_symbols)


# Check for sentence-ending punctuation
def end_punc_check(text):
    # Trim trailing quotes/brackets
    word = text.strip().rstrip('"\')]}').casefold()

    # Check honorifics and common abbreviations
    if word in honorifics or word in other_abbreviations:
        return False
    
    # Check for repeating symbols
    for symbol, min_count in repeating_symbols.items():
        if symbol * min_count in word:
            return False

    # True only if the cleaned word ends in . ! or ?
    return word.endswith(punctuation_symbols)


# Filter paired punctuation
def paired_punc_filter(text, w):    
    prospective = text + f' {w}'
    
    # Homogenous pairs
    for i in homo_punc:
        punc_ends = fr'({any_text}{re.escape(i)})'
        if prospective.count(i) % 2 != 0:
            if re.search(punc_ends, w):
                w = re.sub(punc_ends, '', w)   # Removes only the punctuation character
    
    # Heterogenous pairs
    for open_char, close_char in hetero_punc:
        open_count = prospective.count(open_char)
        close_count = prospective.count(close_char)
        
        if open_count > close_count + 1:        # Excess opens
            punc_start = fr'({any_text}){re.escape(open_char)}'
            if re.search(punc_start, w):
                w = re.sub(punc_start, '', w)   # Removes only the punctuation character
                
        elif close_count > open_count:          # Excess closes
            punc_end = fr'{re.escape(close_char)}({any_text})'
            if re.search(punc_end, w):
                w = re.sub(punc_end, '', w)     # Removes only the punctuation character
    
    return w


# End with closed punctuation pairs
def paired_punc_close(text):
    for i in homo_punc:
        if text.count(i) % 2 != 0:
            text += i
            
    for i in hetero_punc:
        for j in range(text.count(i[0]) - text.count(i[1])):
            text += i[1]
            
    return text


#-------------------------


# Generate text
def generatetext(weights, soft_max):
    text = 'Line::'
        
    for i in range(1000):
        thread = []
        words = text.split()

        # Build the wordbank
        wordbank = choices(    
                range(len(bundle)),
                weights
            )[0]
        
        for i in range(wordbank + 1, 0, -1):
            if len(words) >= i:
                memory = tuple(words[-i:])
                if memory in bundle[i - 1]:
                    thread = (bundle[i - 1][memory])
                    break
            
        #Reset on failure
        if not thread:
            text = 'Line::'
            continue
        
        w = paired_punc_filter(text, choice(thread))
        text += f' {w}'
                
        # Break
        if text.count('Line::') > 1 or (len(text.split()) > soft_max + 1 and end_punc_check(w)):
            text = text.replace('Line:: ', '').replace('Line::', '')
            text = paired_punc_close(text)
            break
    
    return text


#-------------------------


# Main execution
print("\t--[Generator Online]--")

while True:
    prompt = input('')
    
    # Index search
    if prompt != '':
        index = tuple(prompt.split())
        chain = len(index) - 1

        if index in bundle[chain]:
            print(f'\t{index} -> {bundle[chain][index]}')
        else:
            print('\tIndex not found')

    else:
        print(generatetext(weights, 10))