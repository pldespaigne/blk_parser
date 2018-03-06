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

import hashlib

import Util

from TxInput import TxInput
from TxOutput import TxOutput

class Transactions:
	def __init__(self, bytes_tx_data, tx_count):
		self.transactions = []
		bytes_rest = bytes_tx_data
		for i in range(0, tx_count):
			bytes_version = bytes_rest[:4]
			bytes_rest = bytes_rest[4:]

			bytes_in_count = bytes_rest[:1]#get varInt prefix
			bytes_rest = bytes_rest[1:]

			#check if varInt is on 1, 2, 4, or 8 bytes
			if(bytes_in_count[0] == 253):#varInt is on 2 bytes AFTER the prefix
				bytes_in_count = bytes_rest[:2]
				bytes_rest = bytes_rest[2:]
			elif(bytes_in_count[0] == 254):#varInt is on 4 bytes AFTER the prefix
				bytes_in_count = bytes_rest[:4]
				bytes_rest = bytes_rest[4:]
			elif(bytes_in_count[0] == 255):#varInt is on 8 bytes AFTER the prefix
				bytes_in_count = bytes_rest[:8]
				bytes_rest = bytes_rest[8:]
			#else varInt was on 1 bytes, nothing to do

			in_count = int.from_bytes(bytes_in_count, byteorder='little')

			isCoinbase = False
			if(i == 0) : isCoinbase = True
			tx_input = TxInput(bytes_rest, in_count, isCoinbase)
			bytes_rest = bytes_rest[tx_input.size_bytes:]

			bytes_out_count = bytes_rest[:1]#get varInt prefix
			bytes_rest = bytes_rest[1:]

			#check if varInt is on 1, 2, 4, or 8 bytes
			if(bytes_out_count[0] == 253):#varInt is on 2 bytes AFTER the prefix
				bytes_out_count = bytes_rest[:2]
				bytes_rest = bytes_rest[2:]
			elif(bytes_out_count[0] == 254):#varInt is on 4 bytes AFTER the prefix
				bytes_out_count = bytes_rest[:4]
				bytes_rest = bytes_rest[4:]
			elif(bytes_out_count[0] == 255):#varInt is on 8 bytes AFTER the prefix
				bytes_out_count = bytes_rest[:8]
				bytes_rest = bytes_rest[8:]
			#else varInt was on 1 bytes, nothing to do

			out_count = int.from_bytes(bytes_out_count, byteorder='little')

			tx_output = TxOutput(bytes_rest, out_count)
			bytes_rest = bytes_rest[tx_output.size_bytes:]

			bytes_lock_time = bytes_rest[:4]
			bytes_rest = bytes_rest[4:]

			h_sha256 = hashlib.sha256()
			h_sha256.update(bytes_tx_data)
			h_bytes = h_sha256.digest()
			h_sha256 = hashlib.sha256()
			h_sha256.update(h_bytes)
			tx_hash = h_sha256.hexdigest()
			tx_hash = Util.formatHashString(tx_hash, True, True)

			version = int.from_bytes(bytes_out_count, byteorder='little')
			#in_count
			#tx_input
			#out_count
			#tx_output
			lock_time = int.from_bytes(bytes_lock_time, byteorder='little')
			self.transactions.append(Transaction(i, tx_hash, version, in_count, tx_input, out_count, tx_output, lock_time))



	def print(self):
		print('Transactions :')
		for tx in self.transactions:
			tx.print()

class Transaction:
	def __init__(self, _tx_index_in_block, _tx_hash, _version, _in_count, _tx_input, _out_count, _tx_output, _lock_time):
		self.tx_index_in_block = _tx_index_in_block
		self.tx_hash = _tx_hash
		self.version = _version
		self.in_count = _in_count
		self.tx_input = _tx_input
		self.out_count = _out_count
		self.tx_output = _tx_output
		self.lock_time = _lock_time

	def print(self):
		padding = '      '
		if(self.tx_index_in_block == 0) : print(padding, '|', self.tx_index_in_block, 'MINING TX')
		else : print(padding, '|', self.tx_index_in_block)
		print(padding, 'hash', self.tx_hash)
		print(padding, 'version', self.version)
		print(padding, self.in_count, 'input(s)')
		self.tx_input.print()
		print(padding, self.out_count, 'output(s)')
		self.tx_output.print()
		print(padding, 'lock_time', self.lock_time)