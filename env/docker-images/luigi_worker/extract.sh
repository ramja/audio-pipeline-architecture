#!/usr/bin/env Rscript

##########################################################################################
## Script para convertir una lista de grafos en formato graphml a datos en una tabla
## extensión .dat 
##
## Use:  extract.sh <lista de archivos>
##########################################################################################
Rscript --vanilla extract.R $1 /datalake/graph/ /datalake/data/ 
