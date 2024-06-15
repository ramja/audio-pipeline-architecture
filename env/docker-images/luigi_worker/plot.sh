#!/usr/bin/env Rscript

##########################################################################################
## Script para convertir una lista de grafos en formato graphml a datos en una tabla
## extensión .dat 
##
## Use:  extract.sh <lista de archivos>
##########################################################################################
Rscript --vanilla plot.R $1 /datalake/diadiar/ /datalake/data/ /datalake/plot/
