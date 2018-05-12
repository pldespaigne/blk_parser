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

# more info on data structure here :
# Block 		: <https://en.bitcoin.it/wiki/Block>
# Block Header 	: <https://en.bitcoin.it/wiki/Block_hashing_algorithm>
# Transaction	: <https://en.bitcoin.it/wiki/Transaction>

class TxOutput:
	def __init__(self, bytes_data, in_count):
		self.size_bytes = 0
		self.list = []
		bytes_rest = bytes_data
		for i in range(0, in_count):

			bytes_value = bytes_rest[:8]
			bytes_rest = bytes_rest[8:]
			self.size_bytes += 8

			bytes_script_length = bytes_rest[:1] # get varInt prefix
			bytes_rest = bytes_rest[1:]
			self.size_bytes += 1

			# check if varInt is on 1, 2, 4, or 8 bytes
			if(bytes_script_length[0] == 253): # varInt is on 2 bytes AFTER the prefix
				bytes_script_length = bytes_rest[:2]
				bytes_rest = bytes_rest[2:]
				self.size_bytes += 2

			elif(bytes_script_length[0] == 254): # varInt is on 4 bytes AFTER the prefix
				bytes_script_length = bytes_rest[:4]
				bytes_rest = bytes_rest[4:]
				self.size_bytes += 4

			elif(bytes_script_length[0] == 255): # varInt is on 8 bytes AFTER the prefix
				bytes_script_length = bytes_rest[:8]
				bytes_rest = bytes_rest[8:]
				self.size_bytes += 8

			# else varInt was on 1 bytes, nothing to do

			script_length = int.from_bytes(bytes_script_length, byteorder='little')

			bytes_script = bytes_rest[:script_length]
			bytes_rest = bytes_rest[script_length:]
			self.size_bytes += script_length

			value = int.from_bytes(bytes_value, byteorder='little')
			
			#script_length
			script = Util.intToHexString(int.from_bytes(bytes_script, byteorder='big'), False, False)

			address_hex = Util.getDataFromHexStringScript(script)
			if(len(address_hex) == 130):
				address_hex = Util.pubKStringToAddress(address_hex)
			elif(len(address_hex) == 40):
				address_hex = Util.base58Check(address_hex)
			else:
				address_hex = 'UNABLE TO PARSE ADDRESS'


			self.list.append(Output(i, value, script_length, script, address_hex))

	def print(self):
		for out in self.list:
			out.print()

class Output:
	def __init__(self, _output_index, _value, _script_length, _script, _address):
		self.output_index = _output_index
		self.value = _value
		self.script_length = _script_length
		self.script = _script
		self.address = _address

	def print(self):
		padding = '          '
		print(padding, '|', self.output_index)
		print(padding, 'valeur', self.value, 'satoshi(s)')
		print(padding, 'taille du script', self.script_length, 'octet(s)')
		print(padding, 'script', Util.printHexScript(self.script))
		print(padding, 'address', self.address)
