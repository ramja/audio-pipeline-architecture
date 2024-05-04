FROM rocker/r-ver:4.3

ENV LUIGI_HOME luigi/
ENV APP_HOME /usr/local/app1
#RUN  add-apt-repository ppa:boost-latest/ppa
RUN apt-get update
RUN apt-get -y install gnupg
RUN apt-get update
RUN apt-get install -y rng-tools
#RUN sed -i -e 's|#HRNGDEVICE=/dev/hwrng|HRNGDEVICE=/dev/urandom|' /etc/default/rng-tools
#RUN service rng-tools start
#RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
#RUN apt-key adv --keyserver pgp.skewed.de --recv-key 98507F25
#RUN echo 'deb http://downloads.skewed.de/apt/trusty trusty universe' | tee -a  /etc/apt/sources.list
#RUN echo 'deb-src http://downloads.skewed.de/apt/trusty trusty universe' | tee -a  /etc/apt/sources.list
#RUN echo  'deb http://ftp.us.debian.org/debian/ jessie/updates main contrib non-free' | tee -a  /etc/apt/sources.list
#ADD graph-tool.list /etc/apt/sources.list.d/graph-tool.list

#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get update && \
  apt-get install -yq --fix-missing --force-yes  build-essential wget ssh python3 libpq-dev python3.10-dev python3-pip curl libpulse-dev libasound2 sox libsox-fmt-mp3 lame
#RUN apt-get install -yq libboost-tools-dev libboost-graph-dev libboost-python-dev libboost-thread-dev libboost-system-dev libboost-regex-dev  libboost-iostreams-dev libcairomm-1.0-dev

RUN pip install --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#RUN apt-get update
#WORKDIR /usr
#RUN wget https://downloads.skewed.de/graph-tool/graph-tool-2.19.tar.bz2 
#ADD graph-tool-2.18.tar.bz2
#RUN bzip2 -d graph-tool-2.19.tar.bz2
#RUN tar -xvf graph-tool-2.19.tar
#WORKDIR /usr/graph-tool-2.19
#RUN pwd
#RUN ./configure --disable-cairo && make && make install
#RUN apt-get -y --force-yes install python-graph-tool 	
RUN mkdir  $LUIGI_HOME

## Variables de ambiente
#ENV JAVA_HOME /usr/jdk1.8.0_31
ENV PATH $PATH:$JAVA_HOME/bin
#ENV SPARK_VERSION 1.6.0
#ENV HADOOP_VERSION 2.6
#ENV PY4J_VERSION 0.9
#ENV SPARK_PACKAGE spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION
#ENV SPARK_HOME /usr/$SPARK_PACKAGE
#ENV PATH $PATH:$SPARK_HOME/bin
#ENV SPARK_CONF_DIR=/opt/conf/spark
#ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$SPARK_HOME/python/lib/py4j-$PY4J_VERSION-src.zip:$SPARK_HOME/libexec/python:$SPARK_HOME/libexec/python/build:$PYTHONPATH

## Descargamos Java8
#RUN curl -sL --retry 3 --insecure \
#  --header "Cookie: oraclelicense=accept-securebackup-cookie;" \
#  "http://download.oracle.com/otn-pub/java/jdk/8u31-b13/server-jre-8u31-linux-x64.tar.gz" \
#  | gunzip \
#  | tar x -C /usr/ \
#  && ln -s $JAVA_HOME /usr/java \
#  && rm -rf $JAVA_HOME/man

## Descargamos Apache Spark
#RUN curl -sL --retry 3 \
#  "http://d3kbcqa49mib13.cloudfront.net/$SPARK_PACKAGE.tgz" \
#  | gunzip \
#  | tar x -C /usr/ \
#  && ln -s $SPARK_HOME /usr/spark

WORKDIR /usr/bin

RUN Rscript -e "install.packages(c('igraph','dplyr','tidyr','seqHMM','igraph','cluster' ,'randomForest','lme4', 'BradleyTerry2', 'car', 'caret') )"
#RUN Rscript -e "install.packages('cluster')"
#RUN Rscript -e "install.packages('caret')"
RUN Rscript -e "install.packages('devtools')" -e "devtools:::install_github('usagi5886/PraatR')"
#ADD praat6410_linux-intel64-barren.tar.gz /usr/bin
#RUN wget http://ailab.wsu.edu/subdue/software/subdue-5.2.2.zip
#RUN unzip subdue-5.2.2.zip
#RUN cd subdue-5.2.2/src && make && make install
RUN wget https://www.fon.hum.uva.nl/praat/praat6410_linux-intel64-barren.tar.gz
#RUN wget http://www.fon.hum.uva.nl/praat/praat6019_linux64.tar.gz
#RUN pwd
#RUN ls -la praat*
#RUN cd /usr/bin
RUN tar -zxvf /usr/bin/praat6410_linux-intel64-barren.tar.gz
#praat6020_linux64barren.tar.gz

## Variables para el usuario
ENV DPA_USER dpa_worker
ENV DPA_UID 1010

## Creamos al usuario que ejecuta el worker en el grupo `users`
RUN useradd -m -s /bin/bash -N -u $DPA_UID $DPA_USER

ADD .boto /home/$DPA_USER/.boto
ADD .boto /etc/boto.cfg

RUN chown $DPA_USER:users /home/$DPA_USER/.boto

RUN mkdir /home/$DPA_USER/.ssh

## Agregamos la llave para que pueda descargar github
#ADD dpa_rsa /home/$DPA_USER/.ssh/id_rsa


RUN touch /home/$DPA_USER/.ssh/known_hosts

RUN ssh-keyscan -T 60 github.com >> /home/$DPA_USER/.ssh/known_hosts



## Ajustamos los permisos
RUN chown $DPA_USER:users -R /home/$DPA_USER


#WORKDIR /src/myscripts
#RUN wget http://github.com/ramja/praatMS/blob/master/main.R




WORKDIR /home/$DPA_USER
RUN chmod -R 777 .


#COPY pipeline/* /pipeline/

## Clonamos el repositorio
#RUN git clone https://ramjha:rama0000@bitbucket.org/ramjha/qamodel.git

WORKDIR /home/$DPA_USER/pipeline
RUN mkdir -p src


ADD pipeline/Makefile /home/$DPA_USER/pipeline/Makefile
ADD pipeline/dpa_logging.conf /home/$DPA_USER/pipeline/dpa_logging.conf
ADD pipeline/luigi.cfg  /home/$DPA_USER/pipeline/luigi.cfg
ADD pipeline/resample.sh /home/$DPA_USER/pipeline/resample.sh
ADD pipeline/README.md /home/$DPA_USER/pipeline/README.md
ADD pipeline/etl.py /home/$DPA_USER/pipeline/etl.py
ADD pipeline/etl2.py /home/$DPA_USER/pipeline/etl2.py
ADD pipeline/Extract.py /home/$DPA_USER/pipeline/Extract.py
ADD pipeline/Convert.py /home/$DPA_USER/pipeline/Convert.py
ADD pipeline/main.R /home/$DPA_USER/pipeline/main.R
ADD pipeline/listing.sh /home/$DPA_USER/pipeline/listing.sh
ADD pipeline/moveRegistered.sh /home/$DPA_USER/pipeline/moveRegistered.sh
ADD pipeline/graphize.sh /home/$DPA_USER/pipeline/graphize.sh
ADD pipeline/results.sh /home/$DPA_USER/pipeline/results.sh
ADD src/util.R /home/$DPA_USER/pipeline/src/util.R
ADD src/postFilter.R /home/$DPA_USER/pipeline/src/postFilter.R
ADD src/preProcFunctions.R /home/$DPA_USER/pipeline/src/preProcFunctions.R
ADD src/utils.R /home/$DPA_USER/pipeline/src/utils.R
ADD pipeline/my_model1.rda /home/$DPA_USER/pipeline/my_model1.rda
ADD pipeline/extract.sh /home/$DPA_USER/pipeline/extract.sh
ADD pipeline/distance.sh /home/$DPA_USER/pipeline/distance.sh
ADD pipeline/convert.sh /home/$DPA_USER/pipeline/convert.sh
ADD pipeline/results.sh /home/$DPA_USER/pipeline/results.sh

#USER $DPA_USER
CMD [ "/bin/sh",  "-c", "while true; do echo hello world; sleep 1; done"]
