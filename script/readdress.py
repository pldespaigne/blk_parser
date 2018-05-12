# Bitcoin blk_parser
# 
# A Python tool for parsing the blk files of the Bitcoin blockchain
# Wrote for a college project at UCBL (University Lyon 1)
#
# Author : Pierre-Louis DESPAIGNE
# 
# Copyright (C) 2018  DESPAIGNE Pierre-Louis
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import Cli

import shutil
import sys
import os
import time
import getopt

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import *



# print license info
Cli.printLegal()

# parsing script args
try:
	opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['help', 'input=', 'output='])

except getopt.GetoptError: # if an arg is unknonwn, print help and quit
	print()
	print('Unknonwn option', opt)
	Cli.readdressHelp()
	quit()



# iterate over all the args
for opt, arg in opts:
	if opt in ('-h', '--help'):
		Cli.readdressHelp()
		quit()
	elif opt in ('-i', '--input'):
		logFile = arg
	elif opt in ('-o', '--output'):
		folder = arg



# if logFile and folder aren't set by the user they takes the defaults values
if 'logFile' not in locals():
	# input json files path
	# logFile = "./../result/tx00000.json" # only one file
	logFile = "./../result" # every file in the folder

if 'folder' not in locals():
	# output readdressed json files's folder
	folder = './../readdressed/'



# checking if the folder exist, let a chance to the user to stop the script otherwise the folder and its content are deleted
# we use time.sleep() because input() doesn't work inside of pySpark
if os.path.exists(folder):
	print()
	print('\t/!\\ WARNING /!\\')
	print('\tThe folder', folder, 'already exists !')
	print('\tIt will be deleted in 60s . . .')
	print('\tIf you dont want to delete it, kill the script (Ctrl-C), rename the folder and re run the script')
	time.sleep(30)
	print()
	print('\t30s')
	time.sleep(20)
	print()
	print('\t10s')
	time.sleep(20)
	shutil.rmtree(folder)

print()
print('\tReaddressing . . .')
print()
time_start = time.time()


# creating spark dataFrames
sc = SparkContext("local", "Readdressing Transaction of the Bitcoin Blockchain")

sqlContext = SQLContext(sc)

# original dataFrame with all the tx
df = sqlContext.read.json(logFile)
#
# >>> df.printSchema()
# root
#  |-- exchange_rate: string (nullable = true)
#  |-- timestamp: long (nullable = true)
#  |-- total_value: long (nullable = true)
#  |-- tx_ins: array (nullable = true)
#  |    |-- element: struct (containsNull = true)
#  |    |    |-- address: string (nullable = true)
#  |    |    |-- hashPrevOut: string (nullable = true)
#  |    |    |-- indexPrevOut: long (nullable = true)
#  |    |    |-- value: string (nullable = true)
#  |-- tx_outs: array (nullable = true)
#  |    |-- element: struct (containsNull = true)
#  |    |    |-- address: string (nullable = true)
#  |    |    |-- indexOut: long (nullable = true)
#  |    |    |-- value: long (nullable = true)
#  |-- txid: string (nullable = true)
#
# >>> df.show()
# +-------------+----------+-----------+--------------------+--------------------+--------------------+
# |exchange_rate| timestamp|total_value|              tx_ins|             tx_outs|                txid|
# +-------------+----------+-----------+--------------------+--------------------+--------------------+
# |    NO_X_RATE|1231006505| 5000000000|[[MINING_REWARD, ...|[[1A1zP1eP5QGefi2...|0x4a5e1e4baab89f3...|


# explode the tx_ins array into multiple row for an easiest manipulation
exploded = df.withColumn("tx_ins", explode(df.tx_ins))


# create a shaort dataFrames with only the txid and the tx_outs info
short = df.select("txid", "tx_outs").withColumnRenamed("txid", "rtxid").withColumnRenamed("tx_outs", "rtx_outs")
# 
# >>> short.show()
# +--------------------+--------------------+
# |               rtxid|            rtx_outs|
# +--------------------+--------------------+
# |0x4a5e1e4baab89f3...|[[1A1zP1eP5QGefi2...|


# joining the table short and exploded to readdress tx
joined = short.join(exploded, exploded.tx_ins.hashPrevOut == short.rtxid)
#
# >>> joined.show()
# +--------------------+--------------------+-------------+----------+-----------+--------------------+--------------------+--------------------+
# |               rtxid|            rtx_outs|exchange_rate| timestamp|total_value|              tx_ins|             tx_outs|                txid|
# +--------------------+--------------------+-------------+----------+-----------+--------------------+--------------------+--------------------+
# |0x00083e04038eea5...|[[1EkVuWifSLEnxS7...|    NO_X_RATE|1316502031|17617000000|[NO_ADDRESS, 0x00...|[[1Legi535gu12N2S...|0x6e1ca82b9c5b15a...|



# Now all the tx have been readdressed but we need to rebuild the original dataFrame


# Getting all the tx that fails to be readdressed because of missing data
no_add = exploded.filter(exploded.tx_ins.address == "NO_ADDRESS")

cl = joined.drop("rtxid", "rtx_outs")

err = no_add.subtract(cl)



# Working on the readdressed dataFrames to rebuild the original schema
# extract address and value in new column
readd = joined.withColumn("readd", joined.rtx_outs.address[joined.tx_ins.indexPrevOut]).withColumn("reval", lit(joined.rtx_outs.value[joined.tx_ins.indexPrevOut]).cast("string"))

# recreate tx_ins structure with readdressed values
readd = readd.withColumn("new_tx_ins", struct(readd.readd.alias("address"), readd.tx_ins.hashPrevOut.alias("hashPrevOut"), readd.tx_ins.indexPrevOut.alias("indexPrevOut"), readd.reval.alias("value")))

# drop unnecesary column
readd = readd.drop("readd", "reval", "rtxid", "rtx_outs", "tx_ins")

# rename new_tx_ins => tx_ins
readd = readd.withColumnRenamed("new_tx_ins", "tx_ins")

# reorder column 
readd = readd.select("exchange_rate", "timestamp", "total_value", "tx_ins", "tx_outs", "txid")
#
# >>> readd.show()
# +-------------+----------+-----------+--------------------+--------------------+--------------------+
# |exchange_rate| timestamp|total_value|              tx_ins|             tx_outs|                txid|
# +-------------+----------+-----------+--------------------+--------------------+--------------------+
# |    NO_X_RATE|1316502031|17617000000|[1BP5tU5p91j82mmn...|[[1Legi535gu12N2S...|0x6e1ca82b9c5b15a...|

# adding all the "error" row
readd = readd.unionAll(err)


# now we need to revert the explode

# reaggregate tx_ins
reagg = readd.groupBy("txid").agg(collect_set("tx_ins").alias("tx_ins")).withColumnRenamed("txid", "rtxid").withColumnRenamed("tx_ins", "rtx_ins")

reagg = df.join(reagg, reagg.rtxid == df.txid)

reagg = reagg.drop("rtxid", "tx_ins").withColumnRenamed("rtx_ins", "tx_ins").select("exchange_rate", "timestamp", "total_value", "tx_ins", "tx_outs", "txid")
# 
# >>> reagg.show()                     # tx_ins is an array again !
# +-------------+----------+-----------+--------------------+--------------------+--------------------+
# |exchange_rate| timestamp|total_value|              tx_ins|             tx_outs|                txid|
# +-------------+----------+-----------+--------------------+--------------------+--------------------+
# |    NO_X_RATE|1316452759|17583924273|[[1QEg7mQovXmcPUb...|[[1EkVuWifSLEnxS7...|0x00083e04038eea5...|



# we collect all the mining reward tx of the original dataFrame
onlyadd = df.filter(~array_contains(df.tx_ins.address, "NO_ADDRESS"))

# unionAll
final = reagg.unionAll(onlyadd)

# the readdressing process is now over, df.count() == final.count()

# calculating the total number of failed tx
err_count = final.filter(array_contains(final.tx_ins.address, "NO_ADDRESS")).count()

# saving the final dataFrame into multiple json files in the output folder
final.write.format("json").save("./../readdressed") # saving result in many small json file



# display info
time_end = time.time()
print()
print('\tEnd of Readdressing : ', time_end - time_start, 's')
print('\tFailed to readdress', err_count, 'transactions, probably because previous transactions were not yet included, be sure to fully synchronise the Blockchain and try again.')
print()



# deleting all the spark files and renaming the json files
print('Cleaning Folder and renaming files . . .')
os.remove(os.path.join(folder, "_SUCCESS"))
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.crc')]
for i in range(0, len(files)):
		filepath = os.path.join(folder, files[i])
		os.remove(filepath)
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.json')]
for i in range(0, len(files)):
		filepath = os.path.join(folder, files[i])
		os.rename(filepath, os.path.join(folder, "readd_"+str(i)+".json"))