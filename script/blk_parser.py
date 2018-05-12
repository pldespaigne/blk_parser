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

import sys
import os
import time
import getopt

import Cli
import Util
import FastParsing

from BlockIndex import BlockIndex
from TxIndex import TxIndex

# print license info
Cli.printLegal()

block_index = None
tx_index = None
block = None
tx = None
cli_mode = False



# parsing script args
try:
	opts, args = getopt.getopt(sys.argv[1:], 'hci:o:n:', ['help', 'cli', 'input=', 'output=', 'num='])

except getopt.GetoptError: # if an arg is unknonwn, print help and quit
	Cli.unknownCommand(opt)
	sys.exit(2)



# iterate over all the args
for opt, arg in opts:
	if opt in ('-h', '--help'):
		Cli.printHelp()
		sys.exit()
	elif opt in ('-c', '--cli'):
		cli_mode = True
	elif opt in ('-i', '--input'):
		input_folder = arg
	elif opt in ('-o', '--output'):
		output_folder = arg
	elif opt in ('-n', '--num'):
		ans = arg	



# simple parsing mode
if cli_mode == False:
	range_min = 0
	range_max = 0

	# if input and/or output folder are not defined yet, ask the user
	if 'input_folder' not in locals():
		print('Enter the path to the input folder (location of all the blkXXXXX.dat files)')
		input_folder = input('input folder ? :')
		print()
	if 'output_folder' not in locals():
		print('Enter the path to the output folder (location where the json files will be saved)')
		output_folder = input('output folder ? :')
		print()

	# get all the files that end with '.dat' in the input folder
	blk_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f.endswith('.dat')]
	
	# if the num of file to parse is not defined yet, ask the user
	if 'ans' not in locals():
		print('The input folder contains :', len(blk_files), '. Wich files do you want to parse ?')
		print('Please type the file number [ 0 -', len(blk_files) - 1, '], if you want to parse all the files type \'*\'')
		ans = input('file to parse ? :')

	# check if the num answer is either an '*' or a number in the correct range
	if ans.isnumeric():
		file_num = int(ans)
		if file_num < 0 or file_num >= len(blk_files):
			print('ERROR file number out of bounds !')
			quit()
		else:
			range_min = file_num
			range_max = file_num + 1
	else:
		range_max = len(blk_files)

	# parsing all the .dat files requested by the user
	for i in range(range_min, range_max):
			filepath = os.path.join(input_folder, blk_files[i]) # getting the full path of the .dat file

			out_name = blk_files[i]
			out_name = out_name[3:]
			out_name = out_name[:5]
			out_name = "tx" + out_name + ".json" # create the output file name : blk00005.dat -> tx00005.json

			out_filepath = os.path.join(output_folder, out_name) # create the full path of the json file

			# check if the output file already exist and ask the user if he wants to overwrite it
			if os.path.isfile(out_filepath):
				ans = input('The file will be overwritten, are you sure (Y/n) ?')
				if ans != 'Y': quit()

			block_index = BlockIndex(filepath) # create the block index
			tx_index = TxIndex(block_index) # create the tx index

			FastParsing.parse(out_filepath, block_index, tx_index) # parse the file


# cli mode
else:

	# default values
	input_file = '../data/blk00000.dat'
	output_file = '../result/tx00000.json'
	running = True

	while running:
		command = input('blk_parser > ')
		command = command.split(' ')

		############################################ simple command
		if len(command) == 1:

			# quit the script
			if command[0] == 'quit' or command[0] == 'quit()' or command[0] == 'q' or command[0] == 'exit' or command[0] == 'exit()':
				running = False

			# display help
			elif command[0] == 'help' or command[0] == 'h' or command[0] == 'man':
				Cli.printHelp()

			# parse input file to output file
			elif command[0] == 'parse':

				# check if the output file already exist and ask the user if he wants to overwrite it
				if os.path.isfile(output_file):
					ans = input('The file will be overwritten, are you sure (Y/n) ?')
					if ans != 'Y': continue

				# if the indexes doesn't exist create them
				if block_index == None or block_index.path != input_file: block_index = BlockIndex(input_file)
				if tx_index == None or tx_index.path != input_file: tx_index = TxIndex(block_index)

				FastParsing.parse(output_file, block_index, tx_index) # parse the file

			# show input file path
			elif command[0] == 'input':
				print('input file :', input_file)

			# show output file path
			elif command[0] == 'output':
				print('output file :', input_file)

			# display readdress help
			elif command[0] == 'readdress':
				Cli.readdress()

			# display help
			else:
				Cli.unknownCommand(command)

		############################################ command with arg
		elif len(command) == 2:

			# set the input file path
			if command[0] == 'input':
				input_file = command[1]

			# set the output file path
			elif command[0] == 'output':
				output_file = command[1]

			# print a block
			elif command[0] == 'block':
				# if the indexes doesn't exist create them
				if block_index == None or block_index.path != input_file: block_index = BlockIndex(input_file)

				i = int(command[2])
				block = block_index.parseBlock(i)
				block.print()

			# print a tx
			elif command[0] == 'tx':
				# if the indexes doesn't exist create them
				if block_index == None or block_index.path != input_file: block_index = BlockIndex(input_file)
				if tx_index == None or tx_index.path != input_file: tx_index = TxIndex(block_index)
				
				i = int(command[2])
				print('Block :', tx_index.block_num[i])
				tx = tx_index.parseTx(i)
				tx.print()

			# display help
			else:
				Cli.unknownCommand(command)


		# display help
		else:
			Cli.unknownCommand(command)
		