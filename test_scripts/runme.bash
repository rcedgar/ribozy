#!/bin/bash

input_fasta=../test_data/HDV.fa

rm -rf ../test_output
mkdir -p ../test_output
cd ../test_output

echo "Running RNAfold..."
RNAfold -i $input_fasta \
  --jobs=1 \
  --noPS \
  --outfile=HDV.fold \
  --id-prefix=HDV \
  --circ

../py/rnafold_rodness.py HDV.fold \
  | tee HDV.rodness.txt

ls -lh ../test_output/HDV.fold ../test_output/HDV.rodness.txt
