#!/bin/bash

java -Xmx2048m -Xms256m -cp ./csv2graph-1.0.jar org.economygraph.Csv2graph -vectorfile ./test/vectors.csv 

#Ê-g: graphml output, default dot format