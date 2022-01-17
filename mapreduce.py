import multiprocessing
import string
import os
from pathlib import Path
from utils import hash2code
import collections
import itertools
import sys
def file_to_words(filename):
    TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    # print (multiprocessing.current_process().name, 'reading', filename)
    key = set()
    output = collections.defaultdict(int)
    with open(filename, 'r',encoding='iso-8859-1') as f:
        for line in f:
            if line.lstrip().startswith('..'): # Skip rst comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha():
                    output[word] += 1
                    # if word not in key:
                        # output.append( (word, filename) )
                        # key.add(word)
    return list(output.items())
def count_words(partitioned_data):
    reduce_data = collections.defaultdict(int)
    for (key,value) in partitioned_data:
        reduce_data[key] += value
    return list(reduce_data.items())
class MapReduce(object):
    
    def __init__(self, map_func, reduce_func, num_workers=None):
        
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.num_workers = num_workers
        self.pool = multiprocessing.Pool(num_workers)
    
    def partition(self, mapped_values):
        partitioned_data = [[] for i in range(self.num_workers)]
        for key, value in mapped_values:
            partitioned_data[hash2code(key) % self.num_workers].append((key,value))
        return partitioned_data
    
    def __call__(self, inputs, chunksize=1):
        
        map_responses = self.pool.map(self.map_func, inputs, chunksize=chunksize)
        partitioned_data = self.partition(itertools.chain(*map_responses))
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        ret = []
        for i in range(self.num_workers):
            ret += reduced_values[i]
        return ret

if __name__ == '__main__':
    import operator
    import glob
    import time
    
    root = sys.argv[1]
    cores = int(sys.argv[3])
    out_folder = sys.argv[2]
    f = open("%s/mapreduce_%d.txt"%(out_folder,cores),"a")
    s = time.time()
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    mapper = MapReduce(file_to_words, count_words, cores)
    word_counts = mapper(input_files)
    # word_counts.sort(key=operator.itemgetter(1))
    # word_counts.reverse()
    
    # print ('\nTOP 20 WORDS BY FREQUENCY\n')
    # top20 = word_counts[:20]
    # longest = max(len(word) for word, count in top20)
    # for word, count in top20:
    #     print ('%-*s: %5s' % (longest+1, word, count))
    # print(time.time()-s)
    f.write("%.5f\n"%(time.time()-s))
    f.close()    