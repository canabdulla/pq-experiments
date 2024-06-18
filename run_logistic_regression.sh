#!/bin/bash

CMD="java -Xmx24g -Xms24g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml"

pq=TRUE
sep=TRUE

run_reg() {
  dataset=$2
  start=$(date +%s%N)
  sudo perf stat -x \; -o "./perf_output/ml/$1 $dataset $M $centroids $sample_size $sep" -d -d -d \
   $CMD -f logistic_regression.dml \
   -nvargs dataset="$dataset" M=$M centroids=$centroids pq=$pq sep=$sep \
   -exec singlenode -stats
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  sed -i s/$/,"$time"/ "./output/ml/$1 $dataset $M $centroids 0 $sep"
}

for M in 1 2 4; do
  for centroids in 4 8 16 32 64 128; do
    for sep in FALSE; do
      run_reg PQ Adult
    done
  done
done

for M in 1 2 4 8; do
  for centroids in 4 8 16 32 64 128 256; do
    for sep in FALSE; do
      run_reg PQ Covtype
    done
  done
done

pq=FALSE
M=0
centroids=0
sep=TRUE

run_reg Baseline Adult
run_reg Baseline Covtype

rm output/ml/*.mtd
python3 parse_outputs.py  reg
