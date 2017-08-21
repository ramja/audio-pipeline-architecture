#!/bin/bash 

##########################################################################################
## Script para convertir una lista de grafos en formato graphml a datos en una tabla
## extensión .dat 
##
## Use:  extract.sh <lista de archivos>
##########################################################################################
./Extract.py /datalake/graph/$1.graphml
mv /datalake/graph/$1.dat -t /datalake/data
