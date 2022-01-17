for i in {1..30};
do
     python3 baseline.py $1 &
     for j in {1..8};
     do
          python3 mapreduce.py $1 $j 
     done
done
