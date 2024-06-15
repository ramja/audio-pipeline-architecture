#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)
# 
# # test if there is at least one argument: if not, return an error
# 
# # check if necessary libraries installed. If not install them
igraphInstalled = require("jsonlite")
if(!igraphInstalled){ install.packages("jsonlite") }
igraphInstalled = require("dplyr")
if(!igraphInstalled){ install.packages("dplyr") }
igraphInstalled = require("seqHMM")
if(!igraphInstalled){ install.packages("seqHMM") }
# 
# ## Local Base Directory. Change to the one you'll use to store your audios
InDirectory1 = "/datalake/diar/"
InDirectory2 = "/datalake/data/"
InDirectory3 = "/datalake/clas/"
OutDirectory = "/datalake/plot/"
folio = args[1]
#test
#folio = 87

##read diar from a .diar format
d_file=paste(paste(InDirectory1,folio,sep=""),".diar", sep="")
#test
#dfile="data/105.diar"
dat_file=paste(paste(InDirectory2,folio,sep=""),".dat", sep="")
#dat_file="data/105.dat"
sem_file=paste(paste(InDirectory3,folio,sep=""),".clas", sep="")
#sem_file="data/105.clas"
## output file 
plotFileName1=paste(paste(OutDirectory,folio,sep=""),".png", sep="")
plotFileName2=paste(paste(OutDirectory,folio,sep=""),"_10.png", sep="")
diar <-readChar(d_file, file.info(d_file)$size-1)
diar <- gsub("'", "\"", diar)

jdiar <- fromJSON(diar)
##read data from a .dat format
df <- read.csv(dat_file, sep = " ")
cols <- c("participant", "sentiment", "confidence", "segment")
sdf <- read.csv(sem_file, sep = ",", header = FALSE, col.names = cols)
for (j  in 1:nrow(jdiar) ) {
  for ( i  in 1:nrow(df) ) {
    
    if ( df[i,"Duration"]/100  > jdiar[j,"start"] & df[i,"Duration"]/100 < jdiar[j,"end"] ) {
      df[i,"participant"] = jdiar[j,"label"]
      df[i,"segment"] = j
    } else if (df[i,"Duration"]/100  <= jdiar[j,"start"]) {
      next
    } else {
      break
    }
  }
}


agData <- df %>% group_by(segment) %>%
  summarize(WMean = mean(Weight, na.rm=TRUE),PMean = mean(Pitch, na.rm=TRUE),PMode = median(participant, na.rm=TRUE))

agData <- merge(x = agData, y= sdf, by = "segment" , all=TRUE)

agData$cat_pitch <- cut(agData$PMean,
                        breaks=c(-Inf, 50, 1006, Inf),
                        labels=c("low","middle","high"))
agData$cat_weight <- cut(agData$WMean,
                         breaks=c(-Inf, 2000, 4000, Inf),
                         labels=c("low","middle","high"))
pitch_m = matrix(agData$cat_pitch,ncol=5,byrow=TRUE)
weight_m = matrix(agData$cat_weight,ncol=5,byrow=TRUE)
group_m = matrix(agData$PMode,ncol=5,byrow=TRUE)
sentiment_m = matrix(agData$sentiment, ncol=5, byrow=TRUE)
rownames(pitch_m) <- seq(length(pitch_m)/5)
rownames(weight_m) <- seq(length(pitch_m)/5)
rownames(group_m) <- seq(length(pitch_m)/5)
rownames(sentiment_m) <- seq(length(pitch_m)/5)
pitch.seq <- seqdef(pitch_m)#,weights = FALSE)
#alphabet = c("low","middle","high"))
weight.seq <- seqdef(weight_m) #, start = 15, weights = FALSE,
#  alphabet = c("low","middle","high"))
part.seq <- seqdef(group_m) #, start = 15,weights =  c(0, 1,2))

sentiment.seq <- seqdef(sentiment_m)



attr(pitch.seq, "cpal") <- c("gray0", "gray8",
                             "gray16")
attr(weight.seq, "cpal") <- c("gray24","gray32", "gray40")
attr(part.seq, "cpal") <- c("gray48", "gray56", "gray64")
attr(sentiment.seq, "cpal") <- c("gray72", "gray80", "gray88")
png(filename=plotFileName1)
p1 <- ssplot(
  x = list("Pitch" = pitch.seq, "Weight" = weight.seq,
           "Participant" = part.seq, "Sentiment" = sentiment.seq), tlim = 0, with.legend = FALSE,
  xaxis = FALSE, ylab = FALSE, title.n = FALSE)
dev.off()

png(filename=plotFileName2)
p1 <- ssplot(
  x = list("Pitch" = pitch.seq, "Weight" = weight.seq,
           "Participant" = part.seq, "Sentiment" = sentiment.seq ), tlim = 1:10, with.legend = FALSE,
  xaxis = FALSE, ylab = FALSE, title.n = FALSE)
dev.off()

