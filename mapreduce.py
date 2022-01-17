import multiprocessing
import string
import os
from pathlib import Path
from utils import count_words,file_to_words
import collections
import itertools
import sys
class MapReduce(object):
    
    def __init__(self, map_func, reduce_func, num_workers=None):
        
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)
    
    def partition(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()
    
    def __call__(self, inputs, chunksize=1):
        
        map_responses = self.pool.map(self.map_func, inputs, chunksize=chunksize)
        partitioned_data = self.partition(itertools.chain(*map_responses))
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values

if __name__ == '__main__':
    import operator
    import glob
    import time
    
    root = sys.argv[1]
    cores = int(sys.argv[2])
    f = open("dump/mapreduce_%d.txt"%(cores),"a")
    s = time.time()
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    mapper = MapReduce(file_to_words, count_words, cores)
    word_counts = mapper(input_files)
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()
    
    # print ('\nTOP 20 WORDS BY FREQUENCY\n')
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    # for word, count in top20:
    #     print ('%-*s: %5s' % (longest+1, word, count))
    # print(time.time()-s)
    f.write("%.5f\n"%(time.time()-s))
    f.close()    