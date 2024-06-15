#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)
# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
}
folio = args[1]
InDirectory1="/datalake/diar/"
InDirectory2="/datalake/trans/"
OutDirectory="/datalake/sen/"

# check if necessary libraries installed. If not install them
ipcgkInstalled = require("jsonlite")
if(!ipcgkInstalled){ install.packages("jsonlite") }
ipcgkInstalled = require("dplyr")
if(!ipcgkInstalled){ install.packages("dplyr") }
ipcgkInstalled = require("tidyr")
if(!ipcgkInstalled){ install.packages("tidyr") }
ipcgkInstalled = require("stringr")
if(!ipcgkInstalled){ install.packages("stringr") }
##read diar from a .diar format
d_file=paste(paste(InDirectory1,folio,sep=""),".diar", sep="")
w_file=paste(paste(InDirectory2,folio,sep=""),".tra", sep="")
#lapses<-read.table(text = gsub(",", ":", readLines("data/77.diar")),sep =":")
words <- read.delim(w_file, header = FALSE)
## output file 
outFileName=paste(paste(OutDirectory,folio,sep=""),".sen", sep="")
diar <-readChar(d_file, file.info(d_file)$size-1)
diar <- gsub("'", "\"", diar)

lapses <- fromJSON(diar)
  

words <- words %>%
  filter(grepl('^Word', V1)) %>%
  mutate(V2 = gsub(",", ":",V1)) %>%
  separate(V2, c("A", "Word","B", "Start", "C", "End"), sep = ":")
words$Start <- as.numeric(as.character(words$Start))
words$End <- as.numeric(as.character(words$End))


sentences <- c() # data.frame(Participant=1, Sentence="", stringsAsFactors=FALSE)
#sentences <- sentences[-1,]
participants <- c()
segments <- c()

for (j  in 1:nrow(lapses) ) {
  sentence <- c()
  participant=""
  for ( i  in 1:nrow(words) ) {
    if (is.na( words[i,"Start"] ) | is.na(lapses[j,"start"]) | is.na(words[i,"End"]) | is.na(lapses[j,"end"])){
      next
    }
    if (( words[i,"Start"]  > lapses[j,"start"]) &( words[i,"End"]  < lapses[j,"end"] )) {
      sentence <- c(sentence, " ", words[i,"Word"])
      participant = lapses[j,"label"]
    } else if (words[i,"Start"]  <= lapses[j,"start"]) {
      next
    } else {
      segments <- c(segments,j) #lapses[j,"end"])
      participants <- c(participants,participant)
      sentences <- c(sentences,str_flatten(sentence))
      break
    }
  }
} 
segments <- c(segments,j) #lapses[j,"end"])
participants <- c(participants,participant)
sentences <- c(sentences,str_flatten(sentence))


resDf <- data.frame(Participant=participants, Sentences=sentences, Segments=segments)

write.table(resDf,row.names = FALSE,col.names = FALSE,sep=",",outFileName)


