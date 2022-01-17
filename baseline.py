import multiprocessing
import string
import os
from pathlib import Path
from mapreduce import SimpleMapReduce
import collections
def file_to_words(filename):
    """Read a file and return a sequence of (word, occurances) values.
    """
    STOP_WORDS = set([
            'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 
            'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
            ])
    TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    print (multiprocessing.current_process().name, 'reading', filename)
    output = []
    with open(filename, 'rt',encoding='iso-8859-1') as f:
        for line in f:
            if line.lstrip().startswith('..'): # Skip rst comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append( (word, 1) )
    return output


def count_words(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    word, occurances = item
    return (word, sum(occurances))

if __name__ == '__main__':
    import operator
    import glob
    import time
    s = time.time()
    root = "data"
    input_files = [Path(os.path.join(root,ele)) for ele in os.listdir(root)]
    # print(input_files)
    map_responses = []
    for name in input_files:
        map_responses += file_to_words(name)
    word_counts = collections.defaultdict(int)
    for key, value in map_responses:
        word_counts[key] += 1
    word_counts = list(word_counts.items())
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print ('%-*s: %5s' % (longest+1, word, count))
    print ('\nTOP 20 WORDS BY FREQUENCY\n')
    print(time.time()-s)
    