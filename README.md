# NTUEE Network Virtualization and Security Final - MapReduce

## Running MapReduce

### Word Count

1. baseline

```python
python baseline.py [in_foler] [out_foler]
python baseline.py data/cornell wc/cornell
```
The result file will be dumped at `wc/cornell/baseline.txt`

2. mapreduce

```
python mapreduce.py [in_foler] [out_foler] [num_cores]
python mapreduce.py data/cornell wc/cornell 8
```

The result file will be dumped at `wc/cornell/mapreduce_8.txt`

3. Performance on Cornell Corpus Dataset

![wc_cornell](\plot\wc_cornell.png)

### Inverted Index

```python
python invert_baseline.py [in_foler] [out_foler]
python invert_baseline.py data/cornell wc/cornell
```
The result file will be dumped at `inv/cornell/baseline.txt`

2. mapreduce

```
python invert_index.py [in_foler] [out_foler] [num_cores]
python invert_index.py data/cornell wc/cornell 8
```

The result file will be dumped at `inv/cornell/mapreduce_8.txt`

3. Performance on Cornell Dataset

![inv_cornell](plot\inv_cornell.png)

## Distributed ONOS

1. Download [VM file](https://drive.google.com/file/d/1JcGUJJDTtbHNnbFzC7SUK52RmMDBVUry/view) from ONOS website, open the VM

2. Clone this github repo 

   ```
   git clone https://github.com/tsukiyashirokisaki/nfv_final
   ```

2. Put two files in `nfv_final/donos/bin/`  into `home/sdn/bin`

3. Booting ONOS by following the instruction in [ONOS tutorial website](https://wiki.onosproject.org/display/ONOS/Basic+ONOS+Tutorial)

4. Open  mininet through

   ```
   sudo python nfv_final/donos/topos/topo.py $OC1 $OC2 $OC3
   ```

5. You can restart the OSOS been shutdown by 

   ```
   bash home/sdn/bin/reboot.sh [i]
   ```

   where i is the index of the controller, e.g. 1,2,3,......

## Reference

1. [Implementing MapReduce with multiprocessing](https://pymotw.com/2/multiprocessing/mapreduce.html)
2. [Docker](https://www.docker.com/)
3. [ONOS Tutorial](https://wiki.onosproject.org/display/ONOS/Basic+ONOS+Tutorial)
4. [onos-byon](https://github.com/bocon13/onos-byon)

