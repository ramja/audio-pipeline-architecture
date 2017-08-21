FROM r-base:latest

ENV LUIGI_HOME /etc/luigi
ENV APP_HOME /usr/local/app1

ADD graph-tool.list /etc/apt/sources.list.d/graph-tool.list

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get update && \
  apt-get install -y  --force-yes  build-essential python python-dev python-pip git curl libpq-dev pkg-config libfreetype6-dev libssl-dev libcurl4-openssl-dev libgtk2.0-dev libpulse-dev libasound2 sox lame

RUN pip install --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#RUN apt-get update
#RUN apt-get install -y --force-yes python-graph-tool
RUN mkdir  $LUIGI_HOME

## Variables de ambiente
ENV JAVA_HOME /usr/jdk1.8.0_31
ENV PATH $PATH:$JAVA_HOME/bin
ENV SPARK_VERSION 1.6.0
ENV HADOOP_VERSION 2.6
ENV PY4J_VERSION 0.9
ENV SPARK_PACKAGE spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION
ENV SPARK_HOME /usr/$SPARK_PACKAGE
ENV PATH $PATH:$SPARK_HOME/bin
ENV SPARK_CONF_DIR=/opt/conf/spark
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$SPARK_HOME/python/lib/py4j-$PY4J_VERSION-src.zip:$SPARK_HOME/libexec/python:$SPARK_HOME/libexec/python/build:$PYTHONPATH

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

RUN Rscript -e "install.packages('igraph')"
RUN Rscript -e "install.packages('cluster')"
RUN Rscript -e "install.packages('devtools')" -e "devtools:::install_github('usagi5886/PraatR')"
RUN wget http://www.fon.hum.uva.nl/praat/praat6019_linux64.tar.gz
RUN tar -zxvf praat6019_linux64.tar.gz

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
ADD dpa_rsa /home/$DPA_USER/.ssh/id_rsa


RUN touch /home/$DPA_USER/.ssh/known_hosts

RUN ssh-keyscan -T 60 github.com >> /home/$DPA_USER/.ssh/known_hosts



## Ajustamos los permisos
RUN chown $DPA_USER:users -R /home/$DPA_USER


WORKDIR /src/myscripts
RUN wget http://github.com/ramja/praatMS/blob/master/main.R


USER $DPA_USER

WORKDIR /home/$DPA_USER

## Clonamos el repositorio
RUN git clone git@github.com:ramja/data-product-architecture.git


WORKDIR /home/$DPA_USER/data-product-architecture/producto/pipeline



CMD [ "/bin/sh",  "-c", "while true; do echo hello world; sleep 1; done"]
