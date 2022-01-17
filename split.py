import sys
in_file = sys.argv[1] #movie_lines.txt
out_folder = sys.argv[2] #data
f = open(in_file,"r",encoding='iso-8859-1')
lines = f.read().split("\n")
f.close()
seg = 8
seg_block = len(lines)//8
for i in range(seg):
	with open("data1/%d.txt"%(i),"w",encoding='iso-8859-1') as f:
		if i == seg-1:
			f.write("\n".join(line for line in lines[seg_block*(seg-1):]))
		else:
			f.write("\n".join(line for line in lines[seg_block*i:seg_block*(i+1)]))
		f.close()
