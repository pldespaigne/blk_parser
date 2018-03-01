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

import sys
import os
import time

import Util

from Block import Block
from BlockIndex import BlockIndex

def readAllBlockFile(path, pauseAtEach=True, printBlock=True):
	print('DEPRECATED FUNCTION : index blocks and parse blocks from index instead !')

	if(not pauseAtEach): # save starting time for benchmark
		time_start = time.time()
		# print('start', time_start)

	with open(path, 'rb') as block_file: # open file in read binary mode
		
		stat = os.stat(path) # getting the total size of the file
		file_size = stat.st_size

		# setting counters to 0
		read_size = 0 # bytes already read
		start = 0 # starting byte of a blok
		total_size = 0 # total size of a block
		block_num = 0 # number of current block

		while read_size < file_size: # loop through the file
			start += total_size
			block_file.seek(start + 4) # seek directly the size field of the block

			bytes_size = block_file.read(4) # get the size of block in binary
			size = int.from_bytes(bytes_size, byteorder='little') # convert the binary size to int

			total_size = size + 8 # total size of block = read size + 4 byte (magic number) + 4 byte (size)
			
			block_file.seek(start) # go back to the begining of the block

			# magic happens here !!!
			block_bytes_array = block_file.read(total_size) # save the binary data of the block
			block = Block(block_bytes_array, block_num) # parse this data into Block object

			if(printBlock) : block.print() # print the Block object

			if(pauseAtEach) : input("Press Enter to continue...") # pause before next iteration of loop

			block_num += 1 # increment for the next iteration of loop
			read_size += total_size

		# end of the reading looop
	block_file.closed # close the file

	if(not pauseAtEach): # save ending time for benchmark and print the result
		time_end = time.time()
		# print('end', time_end)
		print('reading', block_num-1, 'block(s) =', read_size,'byte(s) in', time_end - time_start, 'second(s)')


def buildBlockIndexFromFile(path, block_index):

	print('indexing . . .')
	time_start = time.time()

	with open(path, 'rb') as block_file: # open file in read binary mode
		
		stat = os.stat(path) # getting the total size of the file
		file_size = stat.st_size

		# setting counters to 0
		read_size = 0 # bytes already read
		start = 0 # starting byte of a blok
		total_size = 0 # total size of a block
		block_num = 0 # number of current block

		while read_size < file_size: # loop through the file
			start += total_size
			block_file.seek(start + 4) # seek directly the size field of the block

			bytes_size = block_file.read(4) # get the size of block in binary
			size = int.from_bytes(bytes_size, byteorder='little') # convert the binary size to int

			total_size = size + 8 # total size of block = read size + 4 byte (magic number) + 4 byte (size)
			
			block_file.seek(start) # go back to the begining of the block

			block_index.appendBlock(start, total_size) # building the block index

			block_num += 1 # increment for the next iteration of loop
			read_size += total_size

		# end of the reading looop
	block_file.closed # close the file
	time_end = time.time()
	print('end of indexing in', time_end - time_start, 's')

# main
# readAllBlockFile('..\data\\blk00000.dat', False, False)

Util.printLegal()

block_index = BlockIndex('..\data\\blk00000.dat')

buildBlockIndexFromFile('..\data\\blk00000.dat', block_index)

# block_index.print()