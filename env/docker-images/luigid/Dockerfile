FROM python:3.10

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


RUN mkdir /var/log/luigid
ADD logrotate.cfg /etc/logrotate.d/luigid
VOLUME /var/log/luigid

RUN mkdir /var/run/luigid
VOLUME /var/run/luigid

EXPOSE 8082

RUN mkdir /etc/luigi
ADD luigi.cfg /etc/luigi/luigi.cfg
ADD scripts/wait-for-postgres.sh /tmp/wait-for-postgress.sh 

RUN  apt-get install -q -y --no-install-recommends \
        sudo cron python-dev libpq-dev build-essential \
        postgresql-client \
    && \
     echo "dpa-user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
USER dpa-user
