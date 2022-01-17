# for i in {1..10};
# do
#      python3 invert_baseline.py $1 $2&
#      for j in {1..8};
#      do
#           python3 invert_index.py $1 $2 $j
#      done
# done
for i in {1..10};
do
     python3 baseline.py $1 $2&
     for j in {1..8};
     do
          python3 mapreduce.py $1 $2 $j
     done
done
