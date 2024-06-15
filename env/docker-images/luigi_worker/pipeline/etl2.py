# encoding=utf8  
import sys  



import os

import json

import datetime

import logging
logging.config.fileConfig('dpa_logging.conf')
logger = logging.getLogger('dpa.pipeline.etl2')

import luigi
from luigi import configuration, LocalTarget

#from luigi.contrib.spark import SparkSubmitTask, PySparkTask
import luigi.contrib.postgres
from luigi.contrib.external_program import ExternalProgramTask
import os
from luigi.contrib.postgres import PostgresQuery
import psycopg2
from pathlib import Path



 ## Global variables
#luigi.register_global('idReg', IntegerParameter(default=5))
#luigi.register_global('fileName', IntegerParameter(default=5)) 

class AllTasks(luigi.WrapperTask):
    """
    Las WrapperTask ahorran el método output()
    Si se usa una clase normal, el pipeline siempre marcará error
    """
    def requires(self):
        #yield test.HolaMundoTask()
        #yield test_spark.TestPySparkTask()
        yield TopStatesToDatabase(date = self.date)
        


        
        
class UpdatePrediction(luigi.Task):

    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)
    fileName = luigi.Parameter(default="error")
    def output(self):
        return luigi.LocalTarget('/datalake/logs/{}_{}_{}T{}{}.log'.format(self.listing.day, self.listing.month, self.listing.year,
                    self.listing.hour,self.listing.minute))


    def run(self):

        with self.requires().open('r') as in_file:
            for line in in_file:
                node, self.proba1, proba2 = line.strip().split()
                
        try:
            conn = psycopg2.connect("dbname='dpa' user='dpa-user' host='postgres' password='dpa-test'")
        except:
           print("I am unable to connect to the database")
        cur = conn.cursor()
        query = "update file_register set  prediction = {},  where id = {}".format(self.proba1,self.requires().idReg)
        cur.execute(query)
        conn.commit()
        cur.close ()
    
    def requires(self):
        return ExtractData(listing = self.listing, idReg=-1)
        
class ReadPrediction(luigi.Task):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("data/artist_streams_%s.tsv" % self.date_interval)

    def requires(self):
        return [Streams(date) for date in self.date_interval]

    def run(self):
        artist_count = defaultdict(int)

        for input in self.input():
            with input.open('r') as in_file:
                for line in in_file:
                    node, proba1, proba2 = line.strip().split()


        with self.output().open('w') as out_file:
            for artist, count in artist_count.iteritems():
                print >> out_file, artist, count


class GetDistance(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/dist/{}-3838.dist".format(self.requires().idReg))

    def program_args(self):
        self.idReg=self.requires().idReg
        self.prediction=0.10
        args = ["bash", "distance.sh", self.requires().idReg]
        return args

    def requires(self):
        return ConverGraph  (listing = self.listing, idReg=-1)
  


class ConverGraph(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/graph/{}.graphml.g".format(self.requires().idReg))

    def program_args(self):
        self.idReg=self.requires().idReg
        self.prediction=0.10
        args = ["bash", "convert.sh", self.requires().idReg]
        return args

    def requires(self):
        return ExtractData(listing = self.listing, idReg=-1)
  

class Plot(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/plot/{}.dat".format(self.requires().idReg))

    def program_args(self):
        self.idReg=self.requires().idReg
        self.prediction=0.10
        args = ["bash", "plot.sh", self.requires().idReg]
        return args

    def requires(self):
        return ExtractData(listing = self.listing, idReg=-1)
    


class ExtractData(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/data/{}.dat".format(self.requires().idReg))

    def program_args(self):
        self.idReg=self.requires().idReg
        self.prediction=0.10
        args = ["bash", "extract.sh", self.requires().idReg]
        return args

    def requires(self):
        return Diarize(listing = self.listing, idReg=-1)
    

class Diarize(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/diar/{}.diar".format(self.requires().idReg))

    def program_args(self):
        self.idReg=self.requires().idReg
        args = ["bash", "diarize.sh", self.requires().idReg]
        return args

    def requires(self):
        return MakeGraph(listing = self.listing, idReg=-1)

class MakeGraph(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/graph/{}.graphml".format(self.requires().idReg))

    def program_args(self):
        self.idReg=self.requires().idReg
        args = ["bash", "graphize.sh", self.requires().idReg]
        return args

    def requires(self):
        return Resample(listing = self.listing, idReg=-1)

class Resample(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.datetime.now())
    idReg = luigi.IntParameter(default=0)

    def output(self):
        return luigi.LocalTarget("/datalake/resample/{}.wav".format(self.idReg))

    def program_args(self):
        self.idReg=Path(self.input().path).stem
        args = ["bash", "resample.sh", self.idReg]
        return args

    def requires(self):
        return ReadId(listing = self.listing, idReg=-1)
    
class ReadFiles(ExternalProgramTask):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    def output(self):
        return luigi.LocalTarget('/datalake/regs/list/{}_{}_{}T{}{}.lst'.format(self.listing.day, self.listing.month, self.listing.year,
                    self.listing.hour,self.listing.minute))

    def program_args(self):
        args = ["bash", "moveRegistered.sh", '/datalake/list/{}_{}_{}T{}{}.lst'.format(self.listing.day, self.listing.month, self.listing.year,
                    self.listing.hour,self.listing.minute)]
        return args

    def requires(self):
        return RegisterFile(listing = self.listing)    

class QueryId(luigi.contrib.postgres.PostgresQuery):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)

    host = 'postgres'
    database = 'dpa'
    user = 'dpa-user'
    password = 'dpa-test'
    table = 'file_register'

    query = "update file_register set  estado = 'I' where id = 14"

    def requires(self):
        return ReadId(listing = self.listing )



class MarkId(luigi.Task):

    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    idReg = luigi.IntParameter(default=0)
    fileName = luigi.Parameter(default="error")
    def output(self):
        return luigi.LocalTarget('/datalake/regs/{}'.format(self.idReg))


    def run(self):

        connection = self.output().connect()
        cursor = connection.cursor()
        sql = self.query

        cursor.execute(sql)

        for row in cursor.fetchall():
            self.rows.append(row)

        self.output().touch(connection)

        connection.commit()
        connection.close()
        try:
            conn = psycopg2.connect("dbname='dpa' user='dpa-user' host='postgres' password='dpa-test'")
        except:
           print("I am unable to connect to the database")

        cur = conn.cursor()

        query = "update file_register set  estado = 'I' where id = {}".format(self.requires().idReg)

        cur.execute(query)

        rows = cur.fetchall()

        with self.output().open('w') as out_file:
            for row in rows:
                self.idReg = row[0]
        self.fileName = row[1]
        os.rename("/datalake/regs/{}".format(row[1]),"/datalake/regs/{}.mp3".format(row[0]))
        out_file.write('{}\t{}\n'.format(
                        row[0],
                        row[1]
                ))
    # renaming directory ''tutorialsdir"

class ReadId(luigi.Task):
    listing = luigi.DateMinuteParameter(default=datetime.datetime.now())
    idReg = luigi.IntParameter(default=0)
    fileName = luigi.Parameter(default="error")

    def output(self):
        return luigi.LocalTarget("/datalake/regs/{}.mp3".format(self.idReg))


    def run(self):
        try:
            conn = psycopg2.connect("dbname='dpa' user='dpa-user' host='postgres' password='dpa-test'")
            cur = conn.cursor()
            cur.execute("""select * from  file_register  where estado = 'R' LIMIT 1""")
            rows = cur.fetchall()
            for row in rows:
                self.idReg = row[0]
                self.fileName = row[1]
            #print(self.fileName)
            os.rename("/datalake/regs/{}".format(self.fileName),"/datalake/regs/{}.mp3".format(self.idReg))
            #with self.output().open("w") as out_file:
            #    out_file.write('{}\t{}\n'.format(self.idReg, self.fileName))
            new_query = "update file_register set  estado = 'I' where id = {}".format(self.idReg)
            cur.execute(new_query)

            conn.commit()
            cur.close ()
        except Exception as e:
            with self.output().open("w") as out_file:
                out_file.write("I am unable to connect to the database" + str(e))
            raise Exception("Error al actualizar registro")



if __name__ == '__main__':
    luigi.run()
