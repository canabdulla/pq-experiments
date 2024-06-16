#!/bin/bash
#file="input/sift_base_100k.hdf5"
#dataset=$(echo $file | sed -r "s/.+\/(.+)\..+/\1/")
dataset="sift_base_100k"
sample_size=100000
calc_dist=TRUE

CMD="java -Xmx24g -Xms24g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml" #just for faster training (~7x)


sudo rm output/distortion/*
sudo rm perf_output/distortion/*

run_perf() {
  local pq=${2}
  start=$(date +%s%N)
  sudo perf stat -x \; -o "./perf_output/distortion/$1 $dataset $M $centroids $sample_size $sep" -d -d -d $CMD -f distortion_test.dml -exec singlenode -stats \
      -nvargs dataset=$dataset M=$M calc_dist=$calc_dist sample_size=$sample_size centroids=$centroids pq=$pq sep=$sep
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  sed -i s/$/,"$time"/ "./output/distortion/$1 $dataset $M $centroids $sample_size $sep"
}

#only works on Ryzen 7 5800X3D
run_perf-l3() {
  local pq=${2}
  sudo perf stat -x \; -o "./perf_output/distortion/$1 $dataset $M $centroids $sample_size TRUE" --append \
       -e r0300C0000040FF04 -e r0300C00000400104 -e r430729 $CMD distortion_test.dml  \
       -nvargs dataset=$dataset M=$M calc_dist=$calc_dist sample_size=$sample_size centroids=$centroids pq=$pq sep=TRUE
}

for centroids in 8 16 32 64 128 256; do
  #pq
  for M in 1 2 4 8; do
    for sep in FALSE TRUE ; do
      run_perf PQ TRUE
      #run_perf-l3 pq $dataset $M $centroids $sample_size TRUE
    done
  done
  #kmeans as reference
  M=1
  run_perf K-Means FALSE
done


sudo rm output/distortion/*.mtd
python3 parse_outputs.py dist
#python3 plot.py
#sudo rm output/*
#sudo rm perf_output/*