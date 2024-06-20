#!/bin/bash

CMD="java -Xmx24g -Xms24g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml"

sample_size=0

run_reg() {
  dataset=$2
  start=$(date +%s%N)
  sudo perf stat -x \; -o "./perf_output/ml/$1 $dataset $M $subcentroids $sample_size $sep" -d -d -d \
   $CMD -f logistic_regression.dml \
   -nvargs dataset="$dataset" M=$M centroids=$subcentroids pq=$pq sep=$sep \
   -exec singlenode -stats
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  sed -i s/$/,"$time"/ "./output/ml/$1 $dataset $M $subcentroids 0 $sep"
}

pq=FALSE
M=0
subcentroids=0
sep=FALSE
#run_reg Baseline Adult
#run_reg Baseline Covtype
run_reg Baseline KDD98

pq=TRUE
for M in 1 2 4; do
  for centroids in 4 8 16 32; do
    subcentroids=$((centroids / M))
    for sep in FALSE TRUE; do
      run_reg PQ Adult
    done
  done
done

for M in 1 2 4; do
  for centroids in 8 16 32 64 128; do
    subcentroids=$((centroids / M))
    for sep in FALSE TRUE; do
      run_reg PQ Covtype
    done
  done
done
for M in 1 2 4; do
  for centroids in 8 16 32 64 128; do
    subcentroids=$((centroids / M))
    for sep in FALSE TRUE; do
      run_reg PQ KDD98
    done
  done
done


rm -f output/ml/*.mtd
python3 parse_outputs.py  reg
