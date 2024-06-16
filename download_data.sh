#!/bin/bash

#source: https://github.com/damslab/reproducibility/blob/master/sigmod2021-sliceline-p218/run3DownloadData.sh

# This script downloads all real datasets shown in Table 1 of the paper
# The remaining datasets are then created via replicating some of these datasets

mkdir -p data;
chmod 755 data;

mkdir -p ./data/ann
mkdir -p ./data/distortion
mkdir -p ./data/ml

mkdir -p ./output/distortion
mkdir -p ./output/ml

mkdir -p ./results/distortion
mkdir -p ./results/ml

mkdir -p ./perf_output/ml
mkdir -p ./perf_output/distortion

# Adult
curl https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data -o data/ml/Adult.csv;
sed -i '$d' data/ml/Adult.csv; # fix empty line at end of file

# Covtype
curl https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz -o data/covtype.data.gz;
gzip -d data/covtype.data.gz;
mv data/covtype.data data/ml/Covtype.csv;

# KDD'98
curl https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup98-mld/epsilon_mirror/cup98lrn.zip -o data/cup98lrn.zip;
unzip data/cup98lrn.zip -d data;
mv data/cup98LRN.txt data/ml/KDD98.csv
rm data/cup98lrn.zip;
sed -i 's/-/ /g' data/ml/KDD98.csv; # fix suffix - at 5th column (numerical)

#SIFT10
wget ftp://ftp.irisa.fr/local/texmex/corpus/siftsmall.tar.gz
tar -xf siftsmall.tar.gz data/distortion/siftsmall
python3 fvecs_to_hdf5.py "data/distortion/siftsmall/siftsmall_base.fvecs" "data/distortion/siftsmall_base.hdf5" 10000

#SIFT1M
wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
tar -xf sift.tar.gz data/distortion/sift
python3 fvecs_to_hdf5.py "data/distortion/sift/sift_base.fvecs" "data/distortion/sift_base_100k.hdf5" 100000

#GIST1M
wget ftp://ftp.irisa.fr/local/texmex/corpus/gist.tar.gz
tar -xf gist.tar.gz data/distortion/gist
python3 fvecs_to_hdf5.py "data/distortion/gist/gist_base.fvecs" "data/distortion/gist_base_100k.hdf5" 100000
