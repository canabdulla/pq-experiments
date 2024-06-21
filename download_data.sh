#!/bin/bash

#Part of the code is taken from: https://github.com/damslab/reproducibility/blob/master/sigmod2021-sliceline-p218/run3DownloadData.sh
#Be sure to install unzip

mkdir -p data;
chmod 755 data;

mkdir -p ./data/ann
mkdir -p ./data/ml

mkdir -p ./output/distortion
mkdir -p ./output/ml

mkdir -p ./results/distortion
mkdir -p ./results/ml

mkdir -p ./perf_output/ml
mkdir -p ./perf_output/distortion

mkdir -p ./plots/distortion/line/perf
mkdir -p ./plots/distortion/bar/perf
mkdir -p ./plots/ml/bar/perf
mkdir -p ./plots/ml/line/perf

## Adult
#curl https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data -o data/ml/Adult.csv;
#sed -i '$d' data/ml/Adult.csv; # fix empty line at end of file
#
## Covtype
#curl https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz -o data/covtype.data.gz;
#gzip -d data/covtype.data.gz;
#mv data/covtype.data data/ml/Covtype.csv;
#
## KDD'98
#curl https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup98-mld/epsilon_mirror/cup98lrn.zip -o data/cup98lrn.zip;
#unzip data/cup98lrn.zip -d data;
#mv data/cup98LRN.txt data/ml/KDD98.csv
#rm data/cup98lrn.zip;
#sed -i 's/-/ /g' data/ml/KDD98.csv; # fix suffix - at 5th column (numerical)

#SIFT1M
#wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
#tar -xf sift.tar.gz sift
#rm sift.tar.gz
#mv "sift" "data/ann/sift"
python3 fvecs_to_csv.py "data/ann/sift/sift_base.fvecs" "data/ann/sift_base_100k.csv" 100000

#SIFT10
#wget ftp://ftp.irisa.fr/local/texmex/corpus/siftsmall.tar.gz
#tar -xf siftsmall.tar.gz siftsmall
#rm siftsmall.tar.gz
#mv "siftsmall" "data/ann/siftsmall"
python3 fvecs_to_csv.py "data/ann/siftsmall/siftsmall_base.fvecs" "data/ann/siftsmall_base.csv" 10000

#GIST1M
#wget ftp://ftp.irisa.fr/local/texmex/corpus/gist.tar.gz
#tar -xf gist.tar.gz gist
#rm gist.tar.gz
#mv "gist" "data/ann/gist"
python3 fvecs_to_csv.py "data/ann/gist/gist_base.fvecs" "data/ann/gist_base_100k.csv" 100000
