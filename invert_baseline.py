if __name__ == '__main__':
    import operator
    import glob
    import time
    import sys
    from invert_index import file_to_words
    from collections import defaultdict
    import os
    from pathlib import Path
    s = time.time()
    root = sys.argv[1]
    out_folder = sys.argv[2]
    f = open("%s/baseline.txt"%(out_folder),"a")
    input_files = [Path(os.path.join(root,ele)).as_posix() for ele in os.listdir(root)]
    word_list = []
    for p in input_files:
        word_list += file_to_words(p)
    out = defaultdict(list)
    for (key,value) in word_list:
        out[key].append(value)
    # print(out)
    # print(time.time()-s)
    f.write("%.5f\n"%(time.time()-s))
    f.close()  
    