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

from Block import Block

class BlockIndex:

	def __init__(self, _path):
		self.path = _path
		self.size = 0
		self.byte_index = [] # starting byte of a block
		self.block_size = [] # size (in bytes) of the coresponding block
		self.buildBlockIndexFromFile()

	def buildBlockIndexFromFile(self):

		print('indexing BLOCKS . . .')
		time_start = time.time()

		with open(self.path, 'rb') as block_file: # open file in read binary mode
			
			stat = os.stat(self.path) # getting the total size of the file
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

				self.appendBlock(start, total_size) # building the block index

				block_num += 1 # increment for the next iteration of loop
				read_size += total_size

			# end of the reading looop
		block_file.closed # close the file
		time_end = time.time()
		print('end of indexing in', time_end - time_start, 's')
		print('Block Index : [ 0 -', self.size - 1, ']')

	def appendBlock(self, _byte_index, _block_size):
		self.byte_index.append(_byte_index)
		self.block_size.append(_block_size)
		self.size += 1

	def parseBlock(self, index):
		print('parsing block', index, '. . .')
		# time_start = time.time()

		with open(self.path, 'rb') as block_file: # open file in read binary mode
			block_file.seek(self.byte_index[index])
			bytes_block = block_file.read(self.block_size[index])
		block_file.closed # close the file

		block = Block(bytes_block, index)

		# time_end = time.time()
		# print('end of parsing block in', time_end - time_start, 's')

		return block

	def print(self):
		for i in range(0, self.size):
			print('block', i, 'starting at', self.byte_index[i], 'with a size of', self.block_size[i], 'byte(s)')
		print('Block Index : [ 0 -', self.size - 1, ']')