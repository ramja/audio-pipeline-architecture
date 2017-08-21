library(cluster)



## Local Base Directory. Change to the one you'll use to store your audios
PitchDirectory = "/home/ramja/ssd/data/Audios/"
# We stablish our local directory as work directory
setwd(PitchDirectory)

# List of wav files to be analized
CurrentFileNames = c(list.files(pattern = ".*dat$"))
l<-list()
names<-list()
for (dFile in CurrentFileNames){
  names<-c(names,dFile)
  for (j in 1:5 ){
  dat <- read.csv(dFile, header = FALSE)
  x<-arima(dat[,j], c(1,0,1))
  l<-c(l,as.list(x$coef))
  }
}
nombres<-list()
nombres$names<-names
m<-matrix(l, ncol = 15,  byrow = TRUE, dimnames = nombres)
n<-as.data.frame(m)
cl1 <- pam(n, 3)

dat = read.csv("3763.dat", header = FALSE)
dat = dat[1:143,]
plot(dat[,1])
hist(dat[,1])
acf(dat[,1])
pacf(dat[,4])
x=arima(dat[,4], c(1,0,1))
x$coef
