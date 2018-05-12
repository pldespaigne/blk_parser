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



from Header import Header
from Transactions import Transactions

# more info on data structure here :
# Block 		: <https://en.bitcoin.it/wiki/Block>
# Block Header 	: <https://en.bitcoin.it/wiki/Block_hashing_algorithm>
# Transaction	: <https://en.bitcoin.it/wiki/Transaction>

class Block:
	def __init__(self, block_bytes_array, _block_num):
		bytes_magic = block_bytes_array[:4]
		bytes_rest = block_bytes_array[4:]

		bytes_size = bytes_rest[:4]
		bytes_rest = bytes_rest[4:]

		bytes_header = bytes_rest[:80]
		bytes_rest = bytes_rest[80:]

		bytes_tx_count = bytes_rest[:1] # get varInt prefix
		bytes_rest = bytes_rest[1:]

		# check if varInt is on 1, 2, 4, or 8 bytes
		if(bytes_tx_count[0] == 253): # varInt is on 2 bytes AFTER the prefix
			bytes_tx_count = bytes_rest[:2]
			bytes_rest = bytes_rest[2:]

		elif(bytes_tx_count[0] == 254): # varInt is on 4 bytes AFTER the prefix
			bytes_tx_count = bytes_rest[:4]
			bytes_rest = bytes_rest[4:]

		elif(bytes_tx_count[0] == 255): # varInt is on 8 bytes AFTER the prefix
			bytes_tx_count = bytes_rest[:8]
			bytes_rest = bytes_rest[8:]
		# else varInt was on 1 bytes, nothing to do
			

		bytes_tx_data = bytes_rest

		self.block_num = _block_num
		self.magic = int.from_bytes(bytes_magic, byteorder='little')
		self.size = int.from_bytes(bytes_size, byteorder='little')
		self.tx_count = int.from_bytes(bytes_tx_count, byteorder='little')
		self.header = Header(bytes_header)
		self.transactions = Transactions(bytes_tx_data, self.tx_count)

	def getNet(self):
		if(self.magic == 3652501241): return 'main network'
		elif(self.magic == 3669344250): return 'test network'
		elif(self.magic == 118034699): return 'test network 3'
		elif(self.magic == 4273258233): return 'namecoin network'
		else: return 'unknown network'

	def print(self):
		print()
		print('Block :', self.block_num)
		print('      ', self.getNet())
		print('       block size :', self.size)
		print('      ', self.tx_count, 'transaction(s)')
		self.header.print()
		self.transactions.print()
		print()
		print('*** END OF BLOCK',self.block_num,'***')