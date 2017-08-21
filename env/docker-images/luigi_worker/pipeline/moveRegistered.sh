awk '{print "mv /datalake/raw/\"" $0 "\" /datalake/regs"}' $1 >> /datalake/regs/mv.sh
#move registered files to regs directory
bash /datalake/regs/mv.sh
#move list to /regs/list
mv $1 /datalake/regs/list
rm /datalake/regs/mv.sh
