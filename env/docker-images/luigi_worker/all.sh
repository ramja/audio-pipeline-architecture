export GOOGLE_APPLICATION_CREDENTIALS="./application_default_credentials.json"
./resample.sh $1
./diarize.sh $1
Rscript --vanilla main.R $1.wav /datalake/resample/ /datalake/graph/
Rscript --vanilla extract.R $1 /datalake/graph/ /datalake/data/ 
./transcribe.sh $1
Rscript --vanilla getSentences.R $1 /datalake/trans/ /datalake/diar/
./sentiment.sh $1
Rscript --vanilla plot.R $1 /datalake/diadiar/ /datalake/data/ /datalake/plot/
