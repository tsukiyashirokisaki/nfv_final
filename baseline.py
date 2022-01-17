import multiprocessing
import string
import os
from pathlib import Path
from mapreduce import SimpleMapReduce
import collections
from utils import count_words,file_to_words
import sys

if __name__ == '__main__':
    import operator
    import glob
    import time
    root = sys.argv[1]
    times = sys.argv[2]
    f = open("dump/baseline.txt","w")
        
    for _ in range(int(times)):
        s = time.time()
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
        # for word, count in top20:
        #     print ('%-*s: %5s' % (longest+1, word, count))
        # print ('\nTOP 20 WORDS BY FREQUENCY\n')
        f.write("%.5f\n"%(time.time()-s))
    f.close()    