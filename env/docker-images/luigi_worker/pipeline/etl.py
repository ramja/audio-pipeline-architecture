# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import os

import json

import datetime

import logging
logging.config.fileConfig('dpa_logging.conf')
logger = logging.getLogger('dpa.pipeline.etl')

import luigi
from luigi import configuration, LocalTarget
from luigi.s3 import S3Target, S3Client, S3FlagTarget, ReadableS3File
#from luigi.contrib.spark import SparkSubmitTask, PySparkTask
import luigi.postgres
from luigi.contrib.external_program import ExternalProgramTask
import os




#from pyspark import SparkContext
#from pyspark.sql import HiveContext
#from pyspark.sql import Row
#from pyspark.conf import SparkConf

from test import HolaMundoTask
import test_spark

class AllTasks(luigi.WrapperTask):
    """
    Las WrapperTask ahorran el método output()
    Si se usa una clase normal, el pipeline siempre marcará error
    """
    def requires(self):
        #yield test.HolaMundoTask()
        #yield test_spark.TestPySparkTask()
        yield TopStatesToDatabase(date = self.date)


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

class FileInput(ExternalProgramTask):

    def output(self):
        return luigi.LocalTarget("/datalake/0.dat")

    def program_args(self):
        args = ["bash", "prueba.sh"]
        return args

    def requires(self):
        return FileList(listing = self.listing)

class RegisterFile(luigi.postgres.CopyToTable):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())

    host = 'postgres'
    database = 'dpa'
    user = 'dpa-user'
    password = 'dpa-test'
    table = 'file_register'

    columns = [('nombre', 'TEXT')]

    def requires(self):
        return FileList(listing = self.listing)

class FileList(luigi.Task):
    listing = luigi.DateMinuteParameter(default=datetime.date.today())
    def output(self):
        return luigi.LocalTarget('/datalake/list/{}_{}_{}T{}{}.lst'.format(self.listing.day, self.listing.month, self.listing.year,
					self.listing.hour,self.listing.minute))


    def run(self):
	with self.output().open("w") as output_file:
		for filename in os.listdir("/datalake/raw"):
			output_file.write("{}\n".format(filename))




if __name__ == '__main__':
    luigi.run()
