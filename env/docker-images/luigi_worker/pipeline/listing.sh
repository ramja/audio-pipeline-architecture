#!/bin/bash
_now=$(date +"%m_%d_%Y")
_file="/datalake/list/$_now.lst"

ls *.wav > $_file    


