import grequests
import os
import multiprocessing 
import itertools
import collections
import time
import json
import operator
from pathlib import Path
def partition( mapped_values):
    """Organize the mapped values by their key.
    Returns an unsorted sequence of tuples with a key and a sequence of values.
    """
    partitioned_data = collections.defaultdict(list)
    for key, value in mapped_values:
        partitioned_data[key].append(value)
    return list(partitioned_data.items())
if __name__ == '__main__':
    start = time.time()
    root = "corpus"
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    print(input_files)
    ports = [5000,8000]
    num_ports = len(ports)
    response = []
    n = len(input_files)
    rs = [grequests.post('http://127.0.0.1:%d/map'%(ports[i%num_ports]),
    json={"value":input_files[slice(i,n,num_ports)]}) for i in range(num_ports)]
    map_responses = [grequests.map(rs)[i].json()["value"][0] for i in range(num_ports)]
    partitioned_data = partition(itertools.chain(*map_responses))
    n = len(partitioned_data)
    rs = []
    for i in range(num_ports):
        rs.append(grequests.post('http://127.0.0.1:%d/reduce'%(ports[i%num_ports]),
        json={"value":partitioned_data[slice(i,n,num_ports)]}))
    word_counts = []
    for i in range(num_ports):
        word_counts += grequests.map(rs)[i].json()["value"]
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print ('%-*s: %5s' % (longest+1, word, count))
    print(time.time()-start)