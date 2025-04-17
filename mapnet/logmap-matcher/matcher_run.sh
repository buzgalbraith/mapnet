#!/bin/bash 

# download ontologies
# echo "16g" | python3 -c 'from mapnet.bertmap.example import data_setup; data_setup()'

## build image 
docker build -f mapnet/logmap-matcher/Dockerfile ./ -t logmap:0.01

## run matching.
echo "running matching" 
docker run --rm -v ./mapnet/logmap-matcher/output:/package/output logmap:0.01 sh run.sh

## quality check matches and write the results 
# python3 mapnet/logmap-matcher/matching_qc.py