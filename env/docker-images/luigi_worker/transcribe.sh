#!/bin/bash 
##########################################################################################
## Script para transcribir un autdio y obtiene un alista de palabras en 
## extensión .trans 
##
## Use:  transcribe.sh <lista de archivos>
##########################################################################################
./Transcribe.py $1 >> /datalake/trans/$1.tra
