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

from Transactions import Transactions

# more info on data structure here :
# Block 		: <https://en.bitcoin.it/wiki/Block>
# Block Header 	: <https://en.bitcoin.it/wiki/Block_hashing_algorithm>
# Transaction	: <https://en.bitcoin.it/wiki/Transaction>

class TxIndex:
	def __init__(self, _block_index):
		self.path = _block_index.path
		self.size = 0
		self.block_num = []
		self.byte_index = []
		self.tx_size = []
		self.buildTxIndexFromBlockIndex(_block_index)

	def buildTxIndexFromBlockIndex(self, _block_index):

		print('indexing TX . . .')
		time_start = time.time()

		with open(_block_index.path, 'rb') as block_file: # open file in read binary mode

			start = 0 # starting byte of a tx
			size = 0 # size of current tx in bytes
			tx_count = 0 # number of tx in current block
			in_count = 0 # number of input of current tx
			out_count = 0 # number of output of current tx
			script_size = 0 # size of input or output script in bytes

			for i in range(_block_index.size): # for each block

				block_file.seek(_block_index.byte_index[i] + 88)
				
				byte_tx_count = block_file.read(1) # reading the TX COUNT.

				# check if varInt is on 1, 2, 4, or 8 bytes
				if(byte_tx_count[0] == 253): # varInt is on 2 bytes AFTER the prefix
					byte_tx_count = block_file.read(2)
					start = _block_index.byte_index[i] + 88 + 3

				elif(byte_tx_count[0] == 254): # varInt is on 4 bytes AFTER the prefix
					byte_tx_count = block_file.read(4)
					start = _block_index.byte_index[i] + 88 + 5

				elif(byte_tx_count[0] == 255): # varInt is on 8 bytes AFTER the prefix
					byte_tx_count = block_file.read(8)
					start = _block_index.byte_index[i] + 88 + 9

				else: # varInt was on 1 bytes, nothing to do
					start = _block_index.byte_index[i] + 88 + 1

				tx_count = int.from_bytes(byte_tx_count, byteorder='little')

				for j in range(tx_count): # for each tx in the block
					size = 4 # version field is on 4 bytes
					block_file.seek(start + size)

					byte_in_count = block_file.read(1) # reading the INPUT COUNT
					size += 1

					# check if varInt is on 1, 2, 4, or 8 bytes
					if(byte_in_count[0] == 253): # varInt is on 2 bytes AFTER the prefix
						byte_in_count = block_file.read(2)
						size += 2

					elif(byte_in_count[0] == 254): # varInt is on 4 bytes AFTER the prefix
						byte_in_count = block_file.read(4)
						size += 4

					elif(byte_in_count[0] == 255): # varInt is on 8 bytes AFTER the prefix
						byte_in_count = block_file.read(8)
						size += 8
					# else: # varInt was on 1 bytes, nothing to do

					in_count = int.from_bytes(byte_in_count, byteorder='little')

					for k in range(in_count): # for each input in tx
						size += 36 # previous tx hash is on 32 bytes and vout is on 4 bytes
						block_file.seek(start+size)

						byte_script_size = block_file.read(1) # reading the SCRIPT SIZE
						size += 1

						# check if varInt is on 1, 2, 4, or 8 bytes
						if(byte_script_size[0] == 253): # varInt is on 2 bytes AFTER the prefix
							byte_script_size = block_file.read(2)
							size += 2

						elif(byte_script_size[0] == 254): # varInt is on 4 bytes AFTER the prefix
							byte_script_size = block_file.read(4)
							size += 4

						elif(byte_script_size[0] == 255): # varInt is on 8 bytes AFTER the prefix
							byte_script_size = block_file.read(8)
							size += 8

						# else: # varInt was on 1 bytes, nothing to do

						script_size = int.from_bytes(byte_script_size, byteorder='little')
						size += script_size + 4 # script size and sequence field on 4 bytes
						block_file.seek(start + size) # end of current input

					# end of all current tx inputs				

					byte_out_count = block_file.read(1) # reading the OUTPUT COUNT
					size += 1

					# check if varInt is on 1, 2, 4, or 8 bytes
					if(byte_out_count[0] == 253): # varInt is on 2 bytes AFTER the prefix
						byte_out_count = block_file.read(2)
						size += 2

					elif(byte_out_count[0] == 254): # varInt is on 4 bytes AFTER the prefix
						byte_in_count = block_file.read(4)
						size += 4

					elif(byte_out_count[0] == 255): # varInt is on 8 bytes AFTER the prefix
						byte_out_count = block_file.read(8)
						size += 8

					# else: # varInt was on 1 bytes, nothing to do

					out_count = int.from_bytes(byte_out_count, byteorder='little')

					for k in range(out_count): # for each OUTPUT in tx
						size += 8 # value field is on 4 bytes
						block_file.seek(start+size)

						byte_script_size = block_file.read(1) # reading the SCRIPT SIZE
						size += 1

						# check if varInt is on 1, 2, 4, or 8 bytes
						if(byte_script_size[0] == 253): # varInt is on 2 bytes AFTER the prefix
							byte_script_size = block_file.read(2)
							size += 2
						elif(byte_script_size[0] == 254): # varInt is on 4 bytes AFTER the prefix
							byte_script_size = block_file.read(4)
							size += 4
						elif(byte_script_size[0] == 255): # varInt is on 8 bytes AFTER the prefix
							byte_script_size = block_file.read(8)
							size += 8
						# else: # varInt was on 1 bytes, nothing to do

						script_size = int.from_bytes(byte_script_size, byteorder='little')
						size += script_size # script size
						block_file.seek(start + size) # end of current input

					# end of all current tx outputs

					size += 4 # locktime field is on 4 bytes

					self.appendTx(start, size, i) # append tx to index
					start = start + size
				# end of all tx of the current block

		block_file.closed # close the file
		time_end = time.time()
		print('end of indexing in', time_end - time_start, 's')
		print('Tx Index : [ 0 -', self.size - 1, ']')

	def appendTx(self, _byte_index, _tx_size, _block_num):
		self.byte_index.append(_byte_index)
		self.tx_size.append(_tx_size)
		self.block_num.append(_block_num)
		self.size += 1

	def parseTx(self, index):
		print('parsing tx', index, '. . .')

		with open(self.path, 'rb') as block_file: # open file in read binary mode
			block_file.seek(self.byte_index[index])
			bytes_block = block_file.read(self.tx_size[index])
		block_file.closed # close the file

		tx = Transactions(bytes_block, 1)

		return tx

	def print(self):
		for i in range(0, self.size):
			print('tx', i, 'of block', self.block_num[i], 'starting at', self.byte_index[i], 'with a size of', self.tx_size[i], 'byte(s)')
		print('Tx Index : [ 0 -', self.size - 1, ']')