import grequests
import glob
import multiprocessing 
import itertools
import collections
import time
import json
import operator
    
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
    input_files = glob.glob('data/*.rst')
    ports = [5000,5001]
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
    print(word_counts)
    print(time.time()-start)