import multiprocessing
import string
import os
from pathlib import Path
from mapreduce import SimpleMapReduce
from utils import count_words,file_to_words


if __name__ == '__main__':
    import operator
    import glob
    import time
    s = time.time()

    root = "data"
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    mapper = SimpleMapReduce(file_to_words, count_words, 2)
    word_counts = mapper(input_files)
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()
    
    print ('\nTOP 20 WORDS BY FREQUENCY\n')
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print ('%-*s: %5s' % (longest+1, word, count))
    print(time.time()-s)