import multiprocessing
import string
import os
from pathlib import Path
import collections
from mapreduce import file_to_words
import sys

if __name__ == '__main__':
    import operator
    import glob
    import time
    root = sys.argv[1]
    out_folder = sys.argv[2]
    f = open("%s/baseline.txt"%(out_folder),"a")
        
    s = time.time()
    input_files = [Path(os.path.join(root,ele)) for ele in os.listdir(root)]
    # print(input_files)
    word_list = []
    for name in input_files:
        word_list += file_to_words(name)
    word_counts = collections.defaultdict(int)
    for key, value in word_list:
        word_counts[key] += value
    # word_counts = list(word_counts.items())
    # word_counts.sort(key=operator.itemgetter(1))
    # word_counts.reverse()
    # top20 = word_counts[:20]
    # longest = max(len(word) for word, count in top20)
    # for word, count in top20:
    #     print ('%-*s: %5s' % (longest+1, word, count))
    # print ('\nTOP 20 WORDS BY FREQUENCY\n')
    f.write("%.5f\n"%(time.time()-s))
    f.close()    