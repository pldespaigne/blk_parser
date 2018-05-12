# Bitcoin blk_parser
# 
# A Python tool for parsing the blk files of the Bitcoin blockchain
# Wrote for college project at UCBL (University Lyon 1)
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

def unknownCommand(command):
		print('Unknown command :', command)
		printHelp()

def printLegal():
	print()
	print('blk_parser  Copyright (C) 2018  DESPAIGNE Pierre-Louis')
	print('This software aimed to parse raw Bitcoin blockchain data into JSON files')
	print()
	print('This program comes with ABSOLUTELY NO WARRANTY.')
	print('This is free software, and you are welcome to redistribute it under certain conditions.')
	print('For details read the LICENSE.txt file or visit <http://www.gnu.org/licenses/>')
	print()

def printHelp():
	print()
	print('-- blk_parser Help Message --')
	print()
	print('examples :')
	print('\t> python blk_parser.py -i ./../data -o ./../result -n *')
	print('\tparse all the .dat files in ./../data to JSON files in ./../result')
	print()
	print('\t> python blk_parser.py -i ./../data -o ./../result -n 4')
	print('\tparse only the 5th (1st file is #0) .dat file in ./../data to a single JSON file in ./../result')
	print()
	print('script arguments :')
	print('\t-h / --help   : show this message')
	print('\t-c / --cli    : run blk_parser in cli mode (see command list below)')
	print('\t-i / --input  : specify the path of the blkXXXXX.dat files')
	print('\t-o / --output : specify the path where the result JSON files will be stored')
	print('\t-n / --num    : specify which blk input file to parse, to parse all the blk files type \'*\'')
	print()
	print('cli mode command :')
	print('\th / help / man  : show this message')
	print('\tq / quit / exit : quit blk_parser')
	print('\tinput <PATH>    : specify the path to a blkXXXXX.dat file, if no path is specified this command show the actual input path')
	print('\toutput <PATH>   : specify the path to save the JSON file, if no path is specified this command show the actual output path')
	print('\tparse           : parse the blkXXXXX.dat file specified in input to the JSON file specified in output')
	print('\treaddress       : the readdressing step needs to be performed with pySpark, this command will print a short help message about readdressing')
	print('\tblock <NUMBER>  : print a block, <NUMBER> has to be a number between [0 - Block Index]')
	print('\ttx <NUMBER>     : print a tx, <NUMBER> has to be a number between [0 - Tx Index]')
	print()

def readdress():
	print()
	print('\tThe raw blockchain data avoid redundancy, thus the input address of transaction is not stored because they already')
	print('\texist elsewhere as an output transaction address. That is why after parsing blkXXXXX.dat files into JSON')
	print('\tyou can see field like this -> address:"NO_ADDRESS". If you want to re-address the transactions you will need')
	print('\tto run a second tool. First be sure to have Apache Spark and pySpark running on your computer.')
	print('\tMore info here : <https://spark.apache.org/>')
	print()
	print('\tThen you need to run this command : $> spark-submit readdress.py -i <PATH TO JSON FILES> -o <PATH TO OUTPUT FOLDER>')
	print()
	print('\t/!\\ WARNING /!\\')
	print('\tIf not specified in arguments (-i and -o) the readdress.py script use predefined folders by default.')
	print('\tThe script takes all the JSON files of the folder ./../result')
	print('\tThen the script save the output in the folder ./../readdressed')
	print('\tIf this output folder already exist it will be deleted along with all the files in it.')
	print('\tTo avoid this you need to rename or move the folder.')
	print()

def readdressHelp():
	print()
	print('-- blk_parser Readdress Help Message --')
	print()
	print('examples :')
	print('\t> spark-submit readdress.py -i ./../result -o ./../readdressed')
	print('\treaddress all the tx of folder ./../result into the folder ./../readdressed')
	print()
	print('script arguments :')
	print('\t-h / --help   : show this message')
	print('\t-i / --input  : specify the path of the folder containing the json files of the transactions to readdress')
	print('\t                if not specified the default input folder is ./../result')
	print('\t-o / --output : specify the path of the folder where the readdressed transactions will be stored')
	print('\t                if not specified the default output folder is ./../readdressed')
	print()

