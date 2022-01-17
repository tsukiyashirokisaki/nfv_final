import grequests
import os
import multiprocessing 
import itertools
import collections
import sys
import time
import json
import operator
from pathlib import Path
from utils import hash2code
if __name__ == '__main__':
    start = time.time()
    root = sys.argv[1]
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    # print(input_files)
    ports = [5000,5001]
    num_ports = len(ports)
    n = len(input_files)
    rs = grequests.map([grequests.post('http://127.0.0.2:%d/map'%(ports[i%num_ports]),
    json={"value":input_files[slice(i,n,num_ports)]}) for i in range(num_ports)])
    map_responses = []
    for i in range(num_ports):
        for j in range(len(rs[i].json()["value"])):
            map_responses += rs[i].json()["value"][j]
    
    partitioned_data = [[] for i in range(num_ports)]
    for key, value in map_responses:
        partitioned_data[hash2code(key) % num_ports].append((key,value))
    
    n = len(partitioned_data)
    rs = []
    for i in range(num_ports):
        rs.append(grequests.post('http://127.0.0.2:%d/reduce'%(ports[i%num_ports]),
        json={"value":partitioned_data[i]}))
    reduce_response = grequests.map(rs)
    word_counts = []
    for i in range(num_ports):
        word_counts += reduce_response[i].json()["value"]
    # word_counts.sort(key=operator.itemgetter(1))
    # word_counts.reverse()
    # top20 = word_counts[:20]
    # print(len(word_counts))
    # longest = max(len(word) for word, count in top20)
    # for word, count in top20:
    #     print ('%-*s: %5s' % (longest+1, word, count))
    print(time.time()-start)