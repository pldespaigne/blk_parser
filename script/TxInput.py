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

class TxInput:
	def __init__(self, bytes_data, in_count, _isCoinbase):
		self.isCoinbase = _isCoinbase
		self.size_bytes = 0
		self.list = []
		bytes_rest = bytes_data
		for i in range(0, in_count):

			bytes_tx_hash = bytes_rest[:32]
			bytes_rest = bytes_rest[32:]
			self.size_bytes += 32

			bytes_out_index = bytes_rest[:4]
			bytes_rest = bytes_rest[4:]
			self.size_bytes += 4

			bytes_script_length = bytes_rest[:1]#get varInt prefix
			bytes_rest = bytes_rest[1:]
			self.size_bytes += 1

			#check if varInt is on 1, 2, 4, or 8 bytes
			if(bytes_script_length[0] == 253):#varInt is on 2 bytes AFTER the prefix
				bytes_script_length = bytes_rest[:2]
				bytes_rest = bytes_rest[2:]
				self.size_bytes += 2
			elif(bytes_script_length[0] == 254):#varInt is on 4 bytes AFTER the prefix
				bytes_script_length = bytes_rest[:4]
				bytes_rest = bytes_rest[4:]
				self.size_bytes += 4
			elif(bytes_script_length[0] == 255):#varInt is on 8 bytes AFTER the prefix
				bytes_script_length = bytes_rest[:8]
				bytes_rest = bytes_rest[8:]
				self.size_bytes += 8
			#else varInt was on 1 bytes, nothing to do

			script_length = int.from_bytes(bytes_script_length, byteorder='little')

			bytes_script = bytes_rest[:script_length]
			bytes_rest = bytes_rest[script_length:]
			self.size_bytes += script_length

			bytes_sequence = bytes_rest[:4]
			bytes_rest = bytes_rest[4:]
			self.size_bytes += 4

			tx_hash = hex(int.from_bytes(bytes_tx_hash, byteorder='big'))
			# tx_hash = hex(bytes_tx_hash)
			# h_sha256 = hashlib.sha256()
			# h_sha256.update(bytes_tx_hash)
			# h_bytes = h_sha256.digest()
			# h_sha256 = hashlib.sha256()
			# h_sha256.update(h_bytes)
			# tx_hash = h_sha256.hexdigest()
			tx_hash = Util.formatHashString(tx_hash[2:], True, True)

			out_index = int.from_bytes(bytes_out_index, byteorder='little')
			#script_length

			# script = int.from_bytes(bytes_script, byteorder='big')
			# script = int.from_bytes(bytes_script, byteorder='little')
			script = Util.intToHexString(int.from_bytes(bytes_script, byteorder='big'), False, False)

			sequence = int.from_bytes(bytes_sequence, byteorder='little')

			self.list.append(Input(i, tx_hash, out_index, script_length, script, sequence))

	def print(self):
		for inp in self.list:
			inp.print(self.isCoinbase)

class Input:
	def __init__(self, _input_index, _tx_hash, _out_index, _script_length, _script, _sequence):
		self.input_index = _input_index
		self.tx_hash = _tx_hash
		self.out_index = _out_index
		self.script_length = _script_length
		self.script = _script
		self.sequence = _sequence

	def print(self, isCoinbase):
		padding = '          '
		print(padding, '|', self.input_index)
		print(padding, 'tx hash', self.tx_hash)
		print(padding, 'output index', self.out_index)
		print(padding, 'taille du script', self.script_length, 'octet(s)')
		if(isCoinbase): print(padding, 'coinbase', self.script)
		else : print(padding, 'script', Util.printHexScript(self.script))
		print(padding, 'sequence', self.sequence)