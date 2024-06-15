#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error

# check if necessary libraries installed. If not install them
igraphInstalled = require("igraph") 
if(!igraphInstalled){ install.packages("igraph") } 

## Local Base Directory. Change to the one you'll use to store your audios
InDirectory = "/datalake/graph/"
OutDirectory = "/datalake/data/"
folio = args[1]


##write graph to a .graphml format
g_file=paste(paste(InDirectory,folio,sep=""),".graphml", sep="")

graph_data <- read.graph(g_file, format = "graphml")
take_duration <- function(l){
  as.numeric(l[2])
}
order <- strsplit(V(graph_data)$name," ")
duration<-unlist(lapply(order,take_duration))
silences <- c(E(graph_data)$weight, 0)
df <- data.frame(
      Weight = V(graph_data)$weight,
      Group =  V(graph_data)$group,
      Pitch = V(graph_data)$pitchr,
      Intensity = V(graph_data)$intensity,
      Duration = duration,
      Silence = silences
)
mat <- data.matrix(df)


outFile=paste(paste(OutDirectory,folio,sep=""),".dat", sep="")
write.table(mat, file=outFile, row.names=FALSE, col.names=TRUE)
