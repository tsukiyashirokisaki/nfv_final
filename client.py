import grequests
import os
import multiprocessing 
import itertools
import collections
import time
import json
import operator
from pathlib import Path
from utils import partition
if __name__ == '__main__':
    start = time.time()
    root = "data"
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    print(input_files)
    ports = [5000,8000]
    num_ports = len(ports)
    n = len(input_files)
    rs = grequests.map([grequests.post('http://127.0.0.2:%d/map'%(ports[i%num_ports]),
    json={"value":input_files[slice(i,n,num_ports)]}) for i in range(num_ports)])
    map_responses = [rs[i].json()["value"][0] for i in range(num_ports)]
    partitioned_data = partition(itertools.chain(*map_responses))
    # n = len(partitioned_data)
    # rs = []
    # for i in range(num_ports):
    #     rs.append(grequests.post('http://127.0.0.2:%d/reduce'%(ports[i%num_ports]),
    #     json={"value":partitioned_data[slice(i,n,num_ports)]}))
    # reduce_response = grequests.map(rs)
    # word_counts = []
    # for i in range(num_ports):
    #     word_counts += reduce_response[i].json()["value"]
    word_counts = collections.defaultdict(int)
    
    for key, value in itertools.chain(*map_responses):
        word_counts[key] += 1
    word_counts = list(word_counts.items())
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print ('%-*s: %5s' % (longest+1, word, count))
    print(time.time()-start)