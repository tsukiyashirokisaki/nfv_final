import multiprocessing
import string
import os
from pathlib import Path
from multiprocessing import Process, Manager
import itertools
import collections
from utils import hash2code

def file_to_words(filename):
    TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    # print (multiprocessing.current_process().name, 'reading', filename)
    key = set()
    output = []
    with open(filename, 'r',encoding='iso-8859-1') as f:
        for line in f:
            if line.lstrip().startswith('..'): # Skip rst comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha():
                    if word not in key:
                        output.append( (word, filename) )
                        key.add(word)
    return output
def to_invert_index(partitioned_data):
    reduce_data = collections.defaultdict(list)
    for (key,value) in partitioned_data:
        reduce_data[key].append(value)
    return list(reduce_data.items())

class InvertMapReduce(object):
    
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.num_workers = num_workers
        self.pool = multiprocessing.Pool(self.num_workers)
    
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
    import sys
    s = time.time()
    root = sys.argv[1]
    out_folder = sys.argv[2]
    cores = int(sys.argv[3])
    f = open("%s/mapreduce_%d.txt"%(out_folder,cores),"a")
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    mapper = InvertMapReduce(file_to_words, to_invert_index, cores)
    invert_index = mapper(input_files)
    # print(len(invert_index))
    # for word in invert_index[:10]:
    #     print(word,"\n")
    # print(time.time()-s)
    f.write("%.5f\n"%(time.time()-s))
    f.close()    