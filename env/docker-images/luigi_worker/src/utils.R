


obtain_data<-function(dFile) {
  l<-vector()
  fl<-list()
  names<-list()
  names<-c(names,dFile)

  nperiod<-1
  dat <- read.csv(dFile, header = FALSE)
  len <- dim(dat)[1]
  inicio<-1
  for(p in 1:nperiod){
    info<-dat[inicio:((p*len)/nperiod),]
    for (j in c(1,2,5 )){
      x<-split(info[,j],info[,4])
      x1<-mean(x$`1`,na.rm = TRUE) 
      x2<-mean(x$`2`,na.rm = TRUE) 
      l<-c(l,x1,x2)
    }
    
  }
  #print(l[[1]],l[[2]])
  l<-c(l, sum(info$`V1`+info$`V5`*1000,na.rm = TRUE))
  fl<-as.list(l)
}


#Prueba unitaria
utest<-obtain_data("~/ssd/datalake/data/1.dat")
#utest

read_distance<-function(dfile){
  con <- file(dfile,"r")
  first_line <- readLines(con,n=1)
  close(con)
  
  distance<-regmatches(first_line, regexpr('.[0-9]+', first_line))
}

#Prueba unitaria
#utest<-read_distance("~/ssd/data/Audios/3996-3831.dist")
#utest

